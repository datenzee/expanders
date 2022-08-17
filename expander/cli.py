import sys

import click

from expander.doc.expander import DocExpander
from expander.vue.expander import VueExpander


@click.command()
@click.argument('type')
@click.argument('input_file')
@click.argument('output_dir')
@click.option('-d', '--dev', is_flag=True)
@click.option('-e', '--expand-only', is_flag=True)
def main(type, input_file, output_dir, dev, expand_only):
    print(f'Expanding {input_file} into {output_dir}')
    if type == 'vue':
        expander = VueExpander(output_dir, input_source=input_file)
        expander.expand()
        if not expand_only:
            expander.post_expand(dev)
    elif type == 'doc':
        expander = DocExpander(output_dir, input_source=input_file)
        expander.expand()
        if not expand_only:
            expander.post_expand(dev)
    else:
        sys.exit("Not a valid expander type. Allowed types are: vue, doc")


if __name__ == '__main__':
    main()
