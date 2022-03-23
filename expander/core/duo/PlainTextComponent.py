from expander.core.duo.Component import Component


class PlainTextComponent(Component):
    def __init__(self, name, content):
        super().__init__(name)
        self.content = content

    def template_data(self):
        return {'content': self.content}
