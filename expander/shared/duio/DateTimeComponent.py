from expander.shared.duio.ContentComponent import ContentComponent


class DateTimeComponent(ContentComponent):
    def format(self):
        return 'MMMM Do YYYY, hh:mm:ss'

    def template(self):
        return 'DateTimeComponent'

    def template_data(self):
        return super().template_data() | {
            'format': self.format()
        }

    def element(self):
        return 'p' if self.is_block else 'span'
