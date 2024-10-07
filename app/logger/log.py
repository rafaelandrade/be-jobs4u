
class Log:

    def __init__(self):
        ...

    def send_log(self, message: str):
        return print(message)

    def send_error(self, message: str):
        ...


logger = Log()