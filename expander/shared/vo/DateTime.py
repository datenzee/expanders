from expander.shared.vo.Content import Content


class DateTime(Content):
    def format(self):
        return 'MMMM Do YYYY, hh:mm:ss'

    def template(self):
        return 'DateTime'

    def template_data(self):
        return super().template_data() | {
            'format': self.format()
        }
