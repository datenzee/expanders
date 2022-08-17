from os import path

from expander.shared.loader import Loader


class DocExpander:
    def __init__(self, output_dir, input_source=None, input_data=None):
        self.output_dir = output_dir
        self.components_output_dir = path.join(output_dir, 'src', 'components', 'gen')
        self.loader = Loader(source=input_source, data=input_data)

    def expand(self):
        print("Running doc expander")

    def post_expand(self, dev=False):
        print("Running post doc expand")
