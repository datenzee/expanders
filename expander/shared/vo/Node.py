from expander.shared.vo.Tree import Tree


class Node(Tree):
    def __init__(self, name, order, is_block, contains):
        super().__init__(name, order)
        self.is_block = is_block
        self.contains = sorted(contains, key=lambda x: x.order)

    def to_string_full(self, indent=0):
        string_full = super().to_string_full(indent)

        for child in self.contains:
            string_full += child.to_string_full(indent + 1)

        return string_full

    def elem(self):
        return 'div' if self.is_block else 'span'

    def force_block(self):
        return False

    def template(self):
        return 'Node'

    def template_data(self):
        return super().template_data() | {
            'elem': self.elem(),
            'force_block': self.force_block(),
            'is_block': self.is_block,
            'contains': self.contains
        }
