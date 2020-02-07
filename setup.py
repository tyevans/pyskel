from setuptools import setup, find_packages

setup(
    name="pyskel",
    version='0.0.4',
    install_requires=["pluggy>=0.3,<1.0", "jinja2"],
    entry_points={
        "console_scripts": ["pyskel=pyskel.main:main"],
        "pyskel": [
            "python_base = pyskel.plugins.python_base.hooks",
            "python_serverless_lambda = pyskel.plugins.python_serverless_lambda.hooks",
            "python_terraform_ecs = pyskel.plugins.python_terraform_ecs.hooks",
            "python_library = pyskel.plugins.python_library.hooks",
            "simple_pyskel_plugin = pyskel.plugins.simple_pyskel_plugin.hooks",
        ]
    },
    packages=find_packages(),
)
