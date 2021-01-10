from queue import Queue

from exceptions.exceptions import CryptException


class CustomQueue(Queue):
    def __init__(self):
        super().__init__()

    def clear_queue(self):
        while not self.empty():
            self.get()


class CaesarCipher:
    """
    Simple implementation of Caesar Cipher encryption and decryption
    shift value is set as a class variable and the number of characters supported are from `!` to `}` i.e ascii values
    from 33 to 125
    As of now, no need for decryption, implement if needed in future

    """

    shift_value = 10  # by how much length we need to shift ascii value
    total_length_supported = 93
    min_ascii = 33
    max_ascii = 125

    @classmethod
    def validate_string(cls, string: str):
        """
        Validate string whether it's all characters are inside desirable ascii limits

        :return: list of all invalid characters
        """

        invalid_characters = []

        for char in string:
            if not cls.min_ascii <= ord(char) <= cls.max_ascii:
                invalid_characters.append(char)

        return ', '.join(invalid_characters)

    @classmethod
    def encrypt(cls, string: str):
        """
        ~ Validate first whether string to be encrypted fits in with ascii values window
        ~ Encrypt a message of string format with caesar cipher encryption

        :return: return string type encrypted message
        """

        invalid_characters = cls.validate_string(string)
        if invalid_characters:
            raise CryptException(f'Invalid characters while encryption: {invalid_characters}')
        encrypted = []  # As '+' operation is not preferred on strings, set this as list and typecast it later
        for char in string:
            ascii_value = ord(char) + cls.shift_value
            if ascii_value > cls.max_ascii:
                ascii_value = ascii_value - cls.max_ascii + cls.min_ascii
            encrypted.append(chr(ascii_value))

        return ''.join(encrypted)
