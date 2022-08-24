class Component:
    def __init__(self, name, is_block):
        self.name = name
        self.is_block = is_block

    def template(self):
        return self.__class__.__name__

    def template_data(self):
        return {'componentName': self.name, 'is_block': self.is_block}
