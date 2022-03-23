from expander.core.duo.Component import Component


class TitleComponent(Component):
    def __init__(self, name, predicate):
        super().__init__(name)
        self.predicate = predicate

    def __str__(self):
        return f'{self.name}(TitleComponent) / title = {self.predicate}'

    def template_data(self):
        return {'predicate': self.predicate}
