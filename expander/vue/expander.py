import pathlib
import shutil
import subprocess
from os import path

from expander.shared.loader import Loader
from expander.vue.templates import load_component_template


class VueExpander:
    def __init__(self, output_dir, input_source=None, input_data=None):
        self.output_dir = output_dir
        self.components_output_dir = path.join(output_dir, 'src', 'components', 'gen')
        self.loader = Loader(source=input_source, data=input_data)

    def expand(self):
        self._clean_output_dir()
        self._copy_template_project()
        self._expand_components()

    def _clean_output_dir(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def _copy_template_project(self):
        template_dir = path.join(path.dirname(__file__), '..', '..', 'project-templates', 'vue')
        shutil.copytree(template_dir, self.output_dir)

    def _expand_components(self):
        self.loader.load()
        pathlib.Path(self.components_output_dir).mkdir(parents=True, exist_ok=True)

        for component in self.loader.components:
            self._expand_component(component)

    def _expand_component(self, component):
        template = load_component_template(component.template())
        file_name = path.join(self.components_output_dir, f'{component.name}.vue')

        with open(file_name, mode='w') as file:
            file.write(template.render(**component.template_data()))

    def post_expand(self, dev=False):
        subprocess.check_call('npm install', shell=True, cwd=self.output_dir)
        if dev:
            subprocess.check_call('npm run dev', shell=True, cwd=self.output_dir)
        else:
            subprocess.check_call('npm run build', shell=True, cwd=self.output_dir)
