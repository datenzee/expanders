from expander.shared.vo.Node import Node


class Strong(Node):
    def elem(self):
        return 'strong'

    def force_block(self):
        return True
