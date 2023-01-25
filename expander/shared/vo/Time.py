from expander.shared.vo.DateTime import DateTime


class Time(DateTime):
    def format(self):
        return 'hh:mm:ss'
