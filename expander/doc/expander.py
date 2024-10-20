import pathlib
import shutil
import subprocess
from os import path

from expander.doc.templates import load_component_template
from expander.shared.loader import Loader


class DocExpander:
    def __init__(self, root_component, output_dir, harvested_data, input_source=None, input_data=None,
                 dt_template_id="datenzee:horizon-europe-expanded-template:1.0.0"):
        self.output_dir = output_dir
        self.harvested_data = harvested_data
        self.src_output_dir = path.join(output_dir, 'src')
        self.components_output_dir = path.join(output_dir, 'src', 'components', 'gen')
        self.loader = Loader(root_component, source=input_source, data=input_data)
        self.dt_template_id = dt_template_id

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

        with (open(file_name, mode='w') as file):
            harvested_before = self.harvested_data.get(component.name + "_before", '')
            harvested_after = self.harvested_data.get(component.name + "_after", '')
            data = component.template_data() | {'harvested_before': harvested_before,
                                                'harvested_after': harvested_after}
            file.write(template.render(**data))

    def _expand_component(self, component):
        template = load_component_template(component.template())
        file_name = path.join(self.components_output_dir, f'{component.name}.html.jinja2')

        with (open(file_name, mode='w') as file):
            harvested_before = self.harvested_data.get(component.name + "_before", '')
            harvested_after = self.harvested_data.get(component.name + "_after", '')
            data = component.template_data() | {'harvested_before': harvested_before,
                                                'harvested_after': harvested_after}
            file.write(template.render(**data))
            print(f'{file_name}: Writing file')
        print(f'{file_name}: Success')

    def post_expand(self, dev=False):
        parts = self.dt_template_id.split(':')
        organization_id = parts[0]
        template_id = parts[1]
        version = parts[2]
        replace_string_in_file(path.join(self.output_dir, 'template.json'), 'datenzee', organization_id)
        replace_string_in_file(path.join(self.output_dir, 'template.json'), 'horizon-europe-expanded-template',
                               template_id)
        replace_string_in_file(path.join(self.output_dir, 'template.json'), '1.0.0', version)
        replace_string_in_file(path.join(self.output_dir, 'template.json'), 'Horizon Europe Expanded Template',
                               self.dt_template_id)
        subprocess.check_call('dsw-tdk put', shell=True, cwd=self.output_dir)


def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path) as f:
        s = f.read()
    s = s.replace(old_string, new_string)
    with open(file_path, "w") as f:
        f.write(s)
