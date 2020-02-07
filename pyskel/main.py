import argparse
import os

import jinja2
import pluggy

from pyskel import hookspecs


def get_plugin_manager():
    pm = pluggy.PluginManager("pyskel")
    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints("pyskel")
    return pm


def get_options(plugin_manager):
    parser = argparse.ArgumentParser(description='PySkel - Project Generator')
    parser.add_argument('output_dir')
    plugin_manager.hook.setup_options(parser=parser)
    return parser.parse_args()


def get_template_loader(plugin_manager):
    app_templates = {}
    plugin_manager.hook.register_plugin_templates(app_templates=app_templates)
    return jinja2.Environment(
        loader=jinja2.PrefixLoader(app_templates, delimiter=':')
    )


def get_available_projects(plugin_manager):
    projects_avail = []
    plugin_manager.hook.register_project(projects_avail=projects_avail)
    return projects_avail


def prompt_for_project_type(projects_avail):
    print("Select Project Type:")
    print('=' * 40)
    for i, project in enumerate(projects_avail, 1):
        print(f'{i}: {project["name"]}')
    print('=' * 40)
    project_id = int(input(f'> (1-{i}) ')) - 1
    return projects_avail[project_id]


def gather_tmpl_context(plugin_manager):
    context = {}
    plugin_manager.hook.get_context(context=context)
    return context


def resolve_python_requirements(selected_project, projects_avail):
    p_by_name = {p['name']: p for p in projects_avail}
    requirements = selected_project.get('python', {}).get('requirements', [])
    for p_name in selected_project.get('dependencies', []):
        requirements.extend(p_by_name[p_name].get('dependencies'))
    return requirements


def get_dependency_order(project, all_projects):
    projects_by_name = {p['name']: p for p in all_projects}

    dependencies = [project]
    known_deps = set()
    dep_stack = project.get('dependencies', [])
    while dep_stack:
        dep_name = dep_stack.pop(0)
        if dep_name not in known_deps:
            known_deps.add(dep_name)
            dep_project = projects_by_name[dep_name]
            dependencies.append(dep_project)
            for _dep_name in dep_project.get('dependencies', []):
                if _dep_name not in known_deps:
                    dep_stack.append(_dep_name)
    return dependencies[::-1]


def resolve_templates(project, all_projects):
    output_files = {}
    dependencies = get_dependency_order(project, all_projects)
    for p in dependencies:
        for entry in p.get('manifest', []):
            if ':' not in entry:  # file wasn't namespaced, assume current project
                rel_path = entry
                entry = f'{p["name"]}:{entry}'
            else:
                rel_path = entry.split(':')[-1]
            output_files[rel_path] = entry
    return output_files


def main():
    plugin_manager = get_plugin_manager()

    args = get_options(plugin_manager)

    if os.path.exists(args.output_dir):
        if os.listdir(args.output_dir):
            raise RuntimeError(f'{args.output_dir} exists and is not empty')
    else:
        os.makedirs(args.output_dir)

    template_loader = get_template_loader(plugin_manager)
    projects_avail = get_available_projects(plugin_manager)
    selected_project = prompt_for_project_type(projects_avail)

    context = gather_tmpl_context(plugin_manager)
    context['python_requirements'] = resolve_python_requirements(selected_project, projects_avail)

    output_files = resolve_templates(selected_project, projects_avail)

    for rel_path, entry in output_files.items():
        output_path = os.path.join(args.output_dir, rel_path)
        base_path = os.path.split(output_path)[0]
        os.makedirs(base_path, exist_ok=True)
        template = template_loader.get_template(entry)
        content = template.render(**context)
        with open(output_path, 'w') as fd:
            fd.write(content)
