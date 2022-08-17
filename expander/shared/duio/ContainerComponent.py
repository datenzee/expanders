from expander.shared.duio.Component import Component


class ContainerComponent(Component):
    def __init__(self, name, is_block, children):
        super().__init__(name, is_block)
        self.children = children

    def __str__(self):
        children_str = ','.join([c.name for c in self.children])
        return f'{self.name}(ContainerComponent) / children = {children_str}'

    def template_data(self):
        return super().template_data() | {'children': [c.name for c in self.children]}
