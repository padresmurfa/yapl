#!/usr/local/bin/python3

import os
import io
import base64
from abc import ABC, abstractmethod

from impl.sha256 import calculate_sha256_of_string
from impl.bundle import Bundle
from impl.source_file_line import SourceFileLine


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


class CommentBaseClass(StatementBaseClass):

    def __init__(self, statement_identifier, prefix, start_token, stop_token):
        super().__init__(prefix, start_token, stop_token)
        self.__statement_identifier = statement_identifier

    def combine(self):
        joined = "\n".join(self._lines)
        encoded = joined.encode("utf-8")
        return self._prefix + self.__statement_identifier + " " \
                            + base64.b64encode(encoded).hex()


class MultiLineCommentBaseClass(CommentBaseClass):

    def __init__(self, comment_identifier, prefix, start_token, stop_token):
        super().__init__(comment_identifier, prefix, start_token, stop_token)

    @classmethod
    def may_contain_text_in_first_line(cls):
        return False

    @classmethod
    def adjust_starting_line_number(cls, starting_line_number):
        return starting_line_number - 2

    def append(self, line):
        expected_prefix = self._prefix
        expected_prefix_with_leading_whitespace = expected_prefix + "    "
        if line.startswith(expected_prefix):
            if line.startswith(expected_prefix_with_leading_whitespace):
                line = self._prefix + line[len(expected_prefix_with_leading_whitespace):]
            else:
                assert False, "Expected multi-line comment to have 4 leading space characters"
        else:
            assert (not line.lstrip()), "Expected multi-line comment line to start with '" + \
                                        expected_prefix_with_leading_whitespace + "'"
        return super().append(line)


class SingleLineCommentBaseClass(CommentBaseClass):

    def __init__(self, comment_identifier, prefix, start_token):
        super().__init__(comment_identifier, prefix, start_token, None)

    @classmethod
    def may_contain_text_in_first_line(cls):
        return True

    @classmethod
    def adjust_ending_line_number(cls, ending_line_number):
        # the first line that doesn't have a single-line comment marker implies
        # that the previous line was the last line of the comment
        return ending_line_number - 1

    def append(self, line):
        expected_prefix = self._prefix + self.get_start_token()
        expected_prefix_with_leading_whitespace = expected_prefix + " "
        if line.startswith(expected_prefix):
            if line.startswith(expected_prefix_with_leading_whitespace):
                line = self._prefix + line[len(expected_prefix_with_leading_whitespace):]
            else:
                assert False, "Expected single-line comment to have a leading space"
        else:
            assert (not line.lstrip()), "Expected single-line comment to start with '" + \
                                        expected_prefix_with_leading_whitespace + "'"
        return super().append(line)


class MultiLineSemanticComment(MultiLineCommentBaseClass):
    def __init__(self, prefix):
        super().__init__("semantic_comment", prefix, "/*", "*/")

    @classmethod
    def get_start_token(cls):
        return "/*"


class MultiLineNonSemanticComment(MultiLineCommentBaseClass):
    def __init__(self, prefix):
        super().__init__("non_semantic_comment", prefix, "/#", "#/")

    @classmethod
    def get_start_token(cls):
        return "/#"


class SingleLineSemanticComment(SingleLineCommentBaseClass):
    def __init__(self, prefix):
        super().__init__("non_semantic_comment", prefix, "//")

    @classmethod
    def get_start_token(cls):
        return "//"


class SingleLineNonSemanticComment(SingleLineCommentBaseClass):
    def __init__(self, prefix):
        super().__init__("non_semantic_comment", prefix, "#")

    @classmethod
    def get_start_token(cls):
        return "#"


class MultiLineStatement(StatementBaseClass):
    # note that this class is rather illogical, but it should do the job,
    # and this is a code-reuse scenario
    def __init__(self, prefix):
        super().__init__("", prefix, None)

    @classmethod
    def get_start_token(cls):
        # e.g. this is a case of wat??? but it allows us to reuse the 'create'
        # method
        return ""

    @classmethod
    def has_start_token(cls, line):
        # e.g. this is weird, as the start token for a multi-line statament is in fact
        # the line-continuation character at the end of the line.
        return line.rstrip().endswith("\\")

    def has_stop_token(self, line):
        # e.g. this is weird, in that the stop token is a lack of line-continuation
        return not self.has_start_token(line)

    @classmethod
    def may_contain_text_in_first_line(cls):
        return True

    @classmethod
    def adjust_ending_line_number(cls, ending_line_number):
        # the first line without a line-continuation character terminates the
        # multi-line statement
        return ending_line_number

    def combine(self):
        array_of_line_segments = []
        for current_line in self._lines:
            found = False
            if array_of_line_segments:
                previous_segments = array_of_line_segments[-1]
                last_previous_line_segment = previous_segments[-1]
                for quotation_mark in ['"""', "'''", "'", '"']:
                    if current_line.startswith(quotation_mark):
                        if last_previous_line_segment.endswith(quotation_mark):
                            l = len(quotation_mark)
                            last_previous_line_segment = last_previous_line_segment[:-l]
                            current_line = current_line[l:]
                            previous_segments[-1] = last_previous_line_segment
                            previous_segments.append(current_line)
                            found = True
                            break
            if not found:
                array_of_line_segments.append([current_line])
        lines = [" ".join(line_segments) for line_segments in array_of_line_segments]
        combined = "".join(lines)
        return self._prefix + combined

    def append(self, line):
        line = line.rstrip()
        last_line_in_multiline_statement = self.has_stop_token(line)
        if not last_line_in_multiline_statement:
            line = line[:-1]
            line = line.rstrip()
        super().append(line)
        return last_line_in_multiline_statement


class SourceFileLines(object):

    def __init__(self, bundle_directory):
        self.__bundle_directory = bundle_directory
        self.__root_directory = os.path.join(self.__bundle_directory, "source_file_lines")
        self.__input_line_number = None
        self.__output_line_number = None
        self.__statement = None

    def __reset(self):
        self.__input_line_number = 1
        self.__output_line_number = 1
        self.__statement = None

    def process_file(self, source_file_ref):
        self.__reset()
        output_filename = os.path.join(self.__root_directory, source_file_ref.relative_pathname)
        output_dirname = os.path.dirname(output_filename)
        os.makedirs(output_dirname, mode=0o777, exist_ok=True)
        print("processing file: " + source_file_ref.relative_pathname)
        with io.open(source_file_ref.absolute_pathname, "r") as i:
            with io.open(output_filename, "w") as output_file:
                line = i.readline()
                while line:
                    input_line_number = self.__input_line_number
                    self.__input_line_number = self.__input_line_number + 1
                    line = line.replace("\t", "    ").rstrip()
                    for output_line in self.__process_line_of_input(
                            input_line_number, self.__output_line_number, line):
                        self.__output_line_number = self.__output_line_number + 1
                        output_line.write_line_to(output_file)
                    line = i.readline()

    def __process_line_of_input(self, current_input_line_number, output_line_number, input_line):
        delta = 0
        for starting_input_line_number, ending_input_line_number, processed_line in \
                self.__process_line_of_input_with_continuations(
                    current_input_line_number, input_line
                ):
            indent_level = len(processed_line)
            processed_line = processed_line.lstrip()
            indent_level = indent_level - len(processed_line)
            sha256 = calculate_sha256_of_string(processed_line)
            yield SourceFileLine(
                output_line_number + delta,
                sha256,
                starting_input_line_number,
                ending_input_line_number,
                indent_level,
                processed_line
            )
            delta = delta + 1

    def __process_line_of_input_with_continuations(self, current_input_line_number, input_line):
        try:
            if self.__statement is not None:
                if not self.__statement.append(input_line):
                    starting_input_line_number, ending_input_line_number = \
                        self.__statement.calculate_starting_and_ending_line_number(\
                            current_input_line_number)
                    combined_statement = self.__statement.combine()
                    self.__statement = None
                    yield starting_input_line_number, ending_input_line_number, combined_statement
            elif SingleLineSemanticComment.has_start_token(input_line):
                self.__statement = SingleLineSemanticComment.create(input_line)
            elif SingleLineNonSemanticComment.has_start_token(input_line):
                self.__statement = SingleLineNonSemanticComment.create(input_line)
            elif MultiLineSemanticComment.has_start_token(input_line):
                self.__statement = MultiLineSemanticComment.create(input_line)
            elif MultiLineNonSemanticComment.has_start_token(input_line):
                self.__statement = MultiLineNonSemanticComment.create(input_line)
            elif MultiLineStatement.has_start_token(input_line):
                self.__statement = MultiLineStatement.create(input_line)
            else:
                if input_line.strip():
                    yield current_input_line_number, current_input_line_number, input_line
        except:
            print("error in line {}: \"{}\"".format(current_input_line_number, input_line))
            raise

def main(args):
    bundle = Bundle(args.bundle_directory)
    bundle.load()
    lines = SourceFileLines(args.bundle_directory)
    manifest = bundle.load()
    for source_file_ref in manifest.get_source_file_refs():
        lines.process_file(source_file_ref)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process the bundle source lines')
    parser.add_argument('-b', '--bundle', dest='bundle_directory', required=True,
                        help='The directory to create the bundle in')
    args = parser.parse_args()

    main(args)
