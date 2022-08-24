from expander.shared.duio.ContentComponent import ContentComponent


class UrlComponent(ContentComponent):
    def __init__(self, name, is_block, predicate=None, text=None, url_label_predicate=None, url_label_text=None):
        super().__init__(name, is_block, predicate, text)
        self.url_label_predicate = url_label_predicate
        self.url_label_text = url_label_text

    def template(self):
        return 'UrlComponent'

    def template_data(self):
        return super().template_data() | {
            'url_label_predicate': self.url_label_predicate,
            'url_label_text': self.url_label_text,
        }

    def element(self):
        return ''
