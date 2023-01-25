class Tree:
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __str__(self):
        return self.name

    def to_string_full(self, indent=0):
        return '  ' * indent + '└ ' + self.name + ' (' + self.__class__.__name__ + ')\n'

    def template(self):
        return self.__class__.__name__

    def template_data(self):
        return {'componentName': self.name}
