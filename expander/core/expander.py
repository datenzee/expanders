import pathlib
import shutil
from os import path

from expander.core.templates import load_component_template
from .loader import Loader


class Expander:
    def __init__(self, input_file, output_dir):
        self.output_dir = output_dir
        self.components_output_dir = path.join(output_dir, 'src', 'components', 'gen')
        self.loader = Loader(input_file)

    def expand(self):
        self.clean_output_dir()
        self.copy_template_project()
        self.expand_components()

    def clean_output_dir(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def copy_template_project(self):
        template_dir = path.join(path.dirname(__file__), '..', '..', 'vue-project-template')
        shutil.copytree(template_dir, self.output_dir)

    def expand_components(self):
        self.loader.load()
        pathlib.Path(self.components_output_dir).mkdir(parents=True, exist_ok=True)

        for component in self.loader.components:
            self.expand_component(component)

    def expand_component(self, component):
        template = load_component_template(component.template())
        file_name = path.join(self.components_output_dir, f'{component.name}.vue')

        with open(file_name, mode='w') as file:
            file.write(template.render(**component.template_data()))
