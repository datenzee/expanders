from expander.shared.vo.Node import Node


class Emphasis(Node):
    def elem(self):
        return 'em'

    def force_block(self):
        return True
