from expander.shared.vo.Node import Node


class Condition(Node):
    def __init__(self, name, order, is_block, predicate, value, contains_positive, contains_negative):
        super().__init__(name, order, is_block, [])
        self.predicate = predicate
        self.value = value
        self.contains_positive = contains_positive
        self.contains_negative = contains_negative

    def to_string_full(self, indent=0):
        string_full = super().to_string_full(indent)

        string_full += '  ' * (indent + 1) + '└ <POSITIVE>\n'
        for child in self.contains_positive:
            string_full += child.to_string_full(indent + 2)

        string_full += '  ' * indent + '└ <NEGATIVE>\n'
        for child in self.contains_negative:
            string_full += child.to_string_full(indent + 2)

        return string_full

    def template(self):
        return 'Condition'

    def template_data(self):
        return super().template_data() | {
            'contains_positive': self.contains_positive,
            'contains_negative': self.contains_negative,
            'predicate': self.predicate,
        }
