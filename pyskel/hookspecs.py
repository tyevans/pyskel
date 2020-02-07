import pluggy

hookspec = pluggy.HookspecMarker("pyskel")


@hookspec
def setup_options(parser):
    pass


@hookspec
def register_plugin_templates(app_templates):
    pass


@hookspec
def register_project(projects_avail):
    pass


@hookspec
def get_context(context):
    pass
