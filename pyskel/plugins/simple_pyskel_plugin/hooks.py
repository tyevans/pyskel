import jinja2

import pyskel

options = {
    "name": "simple_pyskel_plugin",
    "template_module": "pyskel.plugins.simple_pyskel_plugin",
    "dependencies": [
        # Other plugins that are required for this one to work.
        "python_library",
    ],
    "manifest": [
        # Files to write into new projects
        "hooks.py",
    ],
}


@pyskel.hookimpl
def register_plugin_templates(app_templates):
    template_module = options.get('template_module')
    if template_module:
        app_templates[options['name']] = jinja2.PackageLoader(template_module)
    return app_templates


@pyskel.hookimpl
def register_project(projects_avail):
    projects_avail.append(options)
