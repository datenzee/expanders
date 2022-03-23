class Component:
    def __init__(self, name):
        self.name = name

    def template(self):
        return self.__class__.__name__

    def template_data(self):
        return {}
