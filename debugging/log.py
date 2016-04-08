class Log:
    def __init__(self, printing=True):
        self._printing = printing
        self._lines = []

    def log(self, msg, *args):
        if not isinstance(msg, str):
            msg = str(msg).replace('{', '{{').replace('}', '}}')
        if self._printing:
            print(msg.format(*args))
        self._lines.append(msg.format(*args))

    def __str__(self):
        return '\n'.join(self._lines)
