import click

from expander.core.expander import Expander


@click.command()
@click.argument('input_file')
@click.argument('output_dir')
def main(input_file, output_dir):
    print(f'Expanding {input_file} into {output_dir}')
    expander = Expander(input_file, output_dir)
    expander.expand()
    expander.post_expand()


if __name__ == '__main__':
    main()
