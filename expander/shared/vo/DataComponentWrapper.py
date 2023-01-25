from expander.shared.vo.Leaf import Leaf


class DataComponentWrapper(Leaf):
    def __init__(self, name, order, predicate, data_component):
        super().__init__(name, order)

        self.predicate = predicate
        self.data_component = data_component

    def template_data(self):
        return super().template_data() | {
            'predicate': self.predicate,
            'dataComponent': self.data_component.split('#')[-1]
        }