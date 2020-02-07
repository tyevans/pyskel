import jinja2

import pyskel

PLUGIN_NAME = 'python_base'


@pyskel.hookimpl
def register_plugin_templates(app_templates):
    app_templates[PLUGIN_NAME] = jinja2.PackageLoader('pyskel.plugins.python_base')


@pyskel.hookimpl
def register_project(projects_avail):
    projects_avail.append({
        "name": PLUGIN_NAME,
        "manifest": [
            # Files to write into new projects
            'tests/conftest.py',
            '.coveragerc',
            '.flake8',
            'requirements.txt',
        ],
        "dependencies": [
            # Other plugins that are required for this one to work.
        ],
        "python": {
            "requirements": [
                'coverage',
                'pytest',
                'pytest-cov'
            ]
        }
    })


@pyskel.hookimpl
def get_context(context):
    return context
