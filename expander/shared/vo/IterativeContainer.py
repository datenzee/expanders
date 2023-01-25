from expander.shared.vo.Node import Node


class IterativeContainer(Node):
    def __init__(self, name, order, is_block, contains, predicate):
        super().__init__(name, order, is_block, contains)
        self.predicate = predicate

    def template(self):
        return 'IterativeContainer'

    def template_data(self):
        return super().template_data() | {
            'predicate': self.predicate
        }
