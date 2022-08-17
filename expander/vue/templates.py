import pkgutil

from jinja2 import Template


def load_component_template(name):
    template_data = pkgutil.get_data(__name__, f'../../templates/vue/{name}.vue.jinja2').decode()
    return Template(template_data)
