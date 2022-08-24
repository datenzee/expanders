from expander.shared.duio.Component import Component


class ConditionComponent(Component):
    def __init__(self, name, is_block, predicate, value, positive_content_component, negative_content_component):
        super().__init__(name, is_block)
        self.predicate = predicate
        self.value = value
        self.positive_content_component = positive_content_component
        self.negative_content_component = negative_content_component

    def __str__(self):
        return f'{self.name}(Condition) / predicate = {self.predicate}, value = {self.value}, positive_content = {self.positive_content_component.name}, negative_content = {self.negative_content_component.name}'

    def template_data(self):
        return super().template_data() | {
            'predicate': self.predicate,
            'value': self.value,
            'positive_content_component': self.positive_content_component.name,
            'negative_content_component': self.negative_content_component.name,
        }
