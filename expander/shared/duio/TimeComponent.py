from expander.shared.duio.DateTimeComponent import DateTimeComponent


class TimeComponent(DateTimeComponent):
    def format(self):
        return 'hh:mm:ss'
