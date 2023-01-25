from expander.shared.vo.DateTime import DateTime


class Date(DateTime):
    def format(self):
        return 'MMMM Do YYYY'
