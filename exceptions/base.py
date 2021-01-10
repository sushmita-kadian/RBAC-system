class CustomExceptionBase(Exception):
    def __init__(self, error_message, *args):
        super(CustomExceptionBase, self).__init__(error_message, *args)
