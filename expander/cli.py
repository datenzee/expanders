import click

from expander.core.expander import Expander


@click.command()
@click.argument('input_file')
@click.argument('output_dir')
@click.option('-d', '--dev', is_flag=True)
@click.option('-e', '--expand-only', is_flag=True)
def main(input_file, output_dir, dev, expand_only):
    print(f'Expanding {input_file} into {output_dir}')
    expander = Expander(output_dir, input_source=input_file)
    expander.expand()
    if not expand_only:
        expander.post_expand(dev)


if __name__ == '__main__':
    main()
