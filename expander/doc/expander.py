import pathlib
import shutil
import subprocess
from os import path

from expander.shared.loader import Loader
from expander.doc.templates import load_component_template


class DocExpander:
    def __init__(self, root_component, output_dir, input_source=None, input_data=None):
        self.output_dir = output_dir
        self.src_output_dir = path.join(output_dir, 'src')
        self.components_output_dir = path.join(output_dir, 'src', 'components', 'gen')
        self.loader = Loader(root_component, source=input_source, data=input_data)

    def expand(self):
        self.loader.load()
        self._clean_output_dir()
        self._copy_template_project()
        self._expand_app()
        self._expand_components()

    def _clean_output_dir(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def _copy_template_project(self):
        template_dir = path.join(path.dirname(__file__), '..', '..', 'project-templates', 'doc',
                                 'document_template')
        shutil.copytree(template_dir, self.output_dir)

    def _expand_app(self):
        template = load_component_template('App')
        file_name = path.join(self.src_output_dir, 'App.html.jinja2')

        with open(file_name, mode='w') as file:
            file.write(template.render(root_component=self.loader.root_component_name))

    def _expand_components(self):

        print('\n*** Data Components ***\n')
        for component in self.loader.data_components:
            print(component.to_string_full())

        pathlib.Path(self.components_output_dir).mkdir(parents=True, exist_ok=True)

        for component in self.loader.data_components:
            self._expand_data_component(component)

        for component in self.loader.components:
            self._expand_component(component)

    def _expand_data_component(self, component):
        template = load_component_template('DataComponent')
        file_name = path.join(self.components_output_dir, f'{component.name}.html.jinja2')

        with open(file_name, mode='w') as file:
            file.write(template.render(**component.template_data()))

    def _expand_component(self, component):
        template = load_component_template(component.template())
        file_name = path.join(self.components_output_dir, f'{component.name}.html.jinja2')

        with open(file_name, mode='w') as file:
            file.write(template.render(**component.template_data()))

    def post_expand(self, dev=False):
        orig_dir = path.join(path.dirname(__file__), '..', '..', 'project-templates', 'doc')
        tmp_dir = path.join(path.dirname(__file__), '..', '..', 'tmp-doc')
        # subprocess.check_call('. env/bin/activate', shell=True, cwd=orig_dir)
        command = f'cd {orig_dir} && . env/bin/activate && cd {tmp_dir} && dsw-tdk put'
        print(command)
        subprocess.check_call(command, shell=True, cwd=self.output_dir)
