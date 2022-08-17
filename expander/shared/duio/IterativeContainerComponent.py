from expander.shared.duio.Component import Component


class IterativeContainerComponent(Component):
    def __init__(self, name, is_block, content_component, predicate):
        super().__init__(name, is_block)
        self.content_component = content_component
        self.predicate = predicate

    def __str__(self):
        return f'{self.name}(IterativeContainer) / content = {self.content_component.name}, predicate = {self.predicate}'

    def template_data(self):
        return super().template_data() | {
            'content_component': self.content_component.name,
            'predicate': self.predicate,
        }
