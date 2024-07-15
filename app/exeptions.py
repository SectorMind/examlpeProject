class BaseException(Exception):

    def __init__(self, message="This is my own base exception"):
        self.message = message
        super().__init__(self.message)
