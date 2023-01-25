from expander.shared.vo.Leaf import Leaf


class Content(Leaf):
    def __init__(self, name, order, predicate=None, content=None):
        super().__init__(name, order)
        self.predicate = predicate
        self.content = content

    def template_data(self):
        return super().template_data() | {
            'predicate': self.predicate,
            'content': self.content
        }
