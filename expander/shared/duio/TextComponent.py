from expander.shared.duio.ContentComponent import ContentComponent


class TextComponent(ContentComponent):
    def element(self):
        return 'p' if self.is_block else 'span'
