import sys

import click

from expander.doc.expander import DocExpander
from expander.doc.harvester import harvest
from expander.vue.expander import VueExpander


@click.command()
@click.argument('type')
@click.argument('root_component')
@click.argument('input_file')
@click.argument('output_dir')
@click.option('-h', '--harvest-dir', required=False)
@click.option('-d', '--dev', is_flag=True)
@click.option('-e', '--expand-only', is_flag=True)
def main(type, root_component, input_file, output_dir, harvest_dir, dev, expand_only):
    print(f'Expanding {input_file} into {output_dir}')
    if type == 'vue':
        expander = VueExpander(root_component, output_dir, input_source=input_file)
        expander.expand()
        if not expand_only:
            expander.post_expand(dev)
    elif type == 'doc':
        if harvest_dir is not None:
            harvested_data = harvest(harvest_dir)
        else:
            harvested_data = {}
        expander = DocExpander(root_component, output_dir, harvested_data, input_source=input_file)
        expander.expand()
        if not expand_only:
            expander.post_expand(dev)
    else:
        sys.exit("Not a valid expander type. Allowed types are: vue, doc")


if __name__ == '__main__':
    main()
