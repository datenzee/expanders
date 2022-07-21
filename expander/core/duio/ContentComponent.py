from abc import abstractmethod

from expander.core.duio.Component import Component


class ContentComponent(Component):
    def __init__(self, name, predicate=None, text=None):
        super().__init__(name)
        self.predicate = predicate
        self.text = text

    def __str__(self):
        content_str = f'predicate = {self.predicate}' if self.predicate else f'text = {self.text}'
        return f'{self.name}(ContentComponent) / {content_str}'

    def template(self):
        return 'ContentComponent'

    def template_data(self):
        return {
            'predicate': self.predicate,
            'text': self.text,
            'element': self.element()
        }

    @abstractmethod
    def element(self):
        ...
