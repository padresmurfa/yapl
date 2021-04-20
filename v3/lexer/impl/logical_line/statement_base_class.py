from abc import ABC, abstractmethod


class StatementBaseClass(ABC):
    def __init__(self, prefix, start_token, stop_token):
        self._lines = []
        self._prefix = prefix
        self.__start_token = start_token
        self.__stop_token = stop_token

    @classmethod
    @abstractmethod
    def get_start_token(cls):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def may_contain_text_in_first_line(cls):
        raise NotImplementedError()

    @classmethod
    def has_start_token(cls, line):
        return line.lstrip().startswith(cls.get_start_token())

    @classmethod
    def adjust_starting_line_number(cls, starting_line_number):
        return starting_line_number

    @classmethod
    def adjust_ending_line_number(cls, ending_line_number):
        return ending_line_number

    @classmethod
    def create(cls, line):
        start_token = cls.get_start_token()
        line_lstripped = line.lstrip()
        prefix = (" " * (len(line) - len(line_lstripped)))
        if start_token:
            line_lstripped = line_lstripped[len(start_token):]
        return_value = cls(prefix)
        if not cls.may_contain_text_in_first_line():
            assert not line_lstripped, "May not contain text in the first line"
        else:
            return_value.append(line)
        return return_value

    def append(self, line):
        if self.has_stop_token(line):
            return False
        if (not line.lstrip()) or (line.rstrip() == self._prefix):
            self._lines.append("")
        else:
            assert(line.startswith(self._prefix))
            lspace = len(self._prefix)
            self._lines.append(line[lspace:])
        return True

    def append_empty_line(self):
        self._lines.append(self._prefix)

    def has_stop_token(self, line):
        # a None stop-token works for cases that stop automatically in the absence of start
        # tokens, e.g. // and #
        if self.__stop_token is None:
            return not line.startswith(self._prefix + self.__start_token)
        else:
            return line.startswith(self._prefix + self.__stop_token)

    def calculate_starting_and_ending_line_number(self, ending_input_line_number):
        ending_input_line_number = self.adjust_ending_line_number(ending_input_line_number)
        starting_input_line_number = ending_input_line_number - len(self._lines) + 1
        starting_input_line_number = self.adjust_starting_line_number(starting_input_line_number)
        return starting_input_line_number, ending_input_line_number

    @abstractmethod
    def combine(self):
        raise NotImplementedError()
