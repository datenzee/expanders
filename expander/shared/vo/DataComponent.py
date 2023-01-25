class DataComponent:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return self.name

    def to_string_full(self):
        return self.name + '\n' + self.content.to_string_full()

    def template_data(self):
        return {
            'content': self.content
        }
