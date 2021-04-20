import collections
import os
import io
import yaml
import base64

from yapl.v4.lexer.shared.tokenized_lines.base import ManifestBase

TokenizedLine = collections.namedtuple(
    "TokenizedLine", [
        "logical_line_sha256",
        "logical_line_contents",
        "tokens"
    ]
)


def encode(content_string):
    content_binary = content_string.encode("utf-8")
    base64_encoded = base64.b64encode(content_binary)
    hex_encoded = base64_encoded.hex()
    return hex_encoded


def leading_multi_line_comment(logical_line_contents, tokens):
    if logical_line_contents.startswith("---"):
        sublines = logical_line_contents.strip().split("\n")
        comment_contents = [l[3:] for l in sublines[1:-2]]
        encoded_comment_contents = encode("\n".join(comment_contents))
        tokens.append({
            "token": "LEADING_MULTI_LINE_COMMENT",
            "value": encoded_comment_contents
        })
        return sublines[-1]
    return logical_line_contents


def leading_single_line_comment(logical_line_contents, tokens):
    if logical_line_contents.startswith("--") and "\n" in logical_line_contents:
        sublines = logical_line_contents.strip().split("\n")
        comment_contents = [l[2:] for l in sublines[:-1]]
        encoded_comment_contents = encode("\n".join(comment_contents))
        token = "LEADING_MULTI_LINE_COMMENT" if len(sublines) > 2 else "LEADING_SINGLE_LINE_COMMENT"
        tokens.append({
            "token": token,
            "value": encoded_comment_contents
        })
        return sublines[-1]
    return logical_line_contents


def inline_comment(logical_line_contents, tokens):
    if logical_line_contents.startswith("--"):
        comment_contents = logical_line_contents[2:]
        encoded_comment_contents = encode(comment_contents)
        tokens.append({
            "token": "INLINE_COMMENT",
            "value": encoded_comment_contents
        })
        return ""
    return logical_line_contents


def remainder(logical_line_contents, tokens):
    if logical_line_contents:
        tokens.append({
            "token": "REMAINDER",
            "value": logical_line_contents
        })
        return ""
    return logical_line_contents


class NotAnIdentifier(Exception):

    @staticmethod
    def assume(condition, message):
        if condition:
            return
        raise NotAnIdentifier(message)


def extract_string_literal(from_string):
    c = from_string[0]
    if c == "\"":
        # xcxc todo escape (\"), and perhaps other string symbols (""", ')
        for i in range(1, len(from_string) + 1):
            assert (i != len(from_string)), "string literals should be terminated by a quote ({})".format(from_string)
            c = from_string[i]
            if c == "\"":
                result = from_string[1:i]
                _remainder = from_string[i+1:]
                return result, _remainder
    return None, from_string


def extract_integer_literal(from_string):
    # may have leading unary +/-
    c = from_string[0]
    if c.isdigit() or (c in ("+", "-") and len(from_string)>1 and from_string[1].isdigit()):
        for i in range(1, len(from_string) + 1):
            if i == len(from_string):
                return from_string, ""
            c = from_string[i]
            if not c.isdigit():
                if c not in (" ", "]", "}", ")", ","):
                    return None, from_string
                result = from_string[:i]
                _remainder = from_string[i:]
                return result, _remainder
    return None, from_string


def extract_boolean_literal(from_string):
    from_string = from_string.strip()
    for l in ("true", "false"):
        if from_string.startswith(l):
            t = from_string[len(l):]
            if not t:
                return l, ""
            c = t[0]
            if c in (" ", "]", "}", ")", ","):
                return l, t
    return None, from_string


def literal(logical_line_contents, tokens):
    try:
        # xcxc todo "float", "character", "bytes"
        literal, r = extract_boolean_literal(logical_line_contents)
        if literal is not None:
            tokens.append({
                "token": "BOOLEAN_LITERAL",
                "value": literal
            })
            return r
        literal, r = extract_integer_literal(logical_line_contents)
        if literal is not None:
            tokens.append({
                "token": "INTEGER_LITERAL",
                "value": literal
            })
            return r
        literal, r = extract_string_literal(logical_line_contents)
        if literal is not None:
            tokens.append({
                "token": "STRING_LITERAL",
                "value": encode(literal)
            })
            return r
    except NotAnIdentifier:
        pass
    return logical_line_contents


def extract_first_identifier(from_string):
    # `anything`
    l = from_string.lstrip()
    NotAnIdentifier.assume(len(l), "identifers cannot be empty")
    if l.startswith("`"):
        r = l.index("`", 1)
        NotAnIdentifier.assume(r != -1, "identifiers starting with ` must also end with `")
        result = l[1:r]
        remainder = l[r+1:]
        return result, remainder
    NotAnIdentifier.assume(l[0].isalpha() or l[0] == "_", "identifiers must start with a letter or an underscore, not {}, in {}".format(l[0], from_string))
    for i in range(1, len(l) + 1):
        if i == len(l):
            return l, ""
        c = l[i]
        if not (c.isalnum() or c in ("_", ".")):
            result = l[:i]
            remainder = l[i:]
            return result, remainder
    return None, from_string


def _create_identifier_token(identifier):
    return {
        "token": "IDENTIFIER",
        "value": identifier
    }


def identifier(logical_line_contents, tokens):
    try:
        i, r = extract_first_identifier(logical_line_contents)
        if i is not None:
            tokens.append(_create_identifier_token(i))
            return r
    except NotAnIdentifier:
        pass
    return logical_line_contents


def _specific_keyword(k, logical_line_contents, tokens):
    kw = k + " "
    if logical_line_contents == k or logical_line_contents.startswith(kw):
        logical_line_contents = logical_line_contents[len(kw):]
        tokens.append({
            "token": "KEYWORD",
            "value": k.upper()
        })
    return logical_line_contents


def keyword(logical_line_contents, tokens):
    for k in (
        "not",
        "empty", "none",
        "module", "class",
        "initializers", "initialize", "new",
        "closure", "closes", "over",
        "functions", "export", "function",
        "returns", "return",
        "generator",
        "yields", "yield",
        "methods", "method",
        "accepts",
        "body",
        "fake", "unit", "test", "suite",
        "for", "repeat", "while", "until", "in",
        "given", "that", "when", "then",
        "if", "then", "else",
        "scenario", "discard",
        "private", "instance", "public", "class", "initializers", "state", "properties",
        "compound", "value", "type",
        "property", "getter", "setter",
        "import", "from"
    ):
        before = logical_line_contents
        after = _specific_keyword(k, logical_line_contents, tokens)
        if before != after:
            logical_line_contents = after
            break
    return logical_line_contents


def basic_type(logical_line_contents, tokens):
    for k in (
            "string", "boolean", "integer", "float", "character", "bytes"
    ):
        before = logical_line_contents
        after = _specific_keyword(k, logical_line_contents, tokens)
        if before != after:
            tokens[-1]["token"] = "BASIC_TYPE"
            logical_line_contents = after
            break
    return logical_line_contents


def _specific_symbol(o, logical_line_contents, tokens, token_name):
    if logical_line_contents.startswith(o):
        logical_line_contents = logical_line_contents[len(o):]
        tokens.append({
            "token": token_name,
            "value": o
        })
    return logical_line_contents


def infix_comparison_operator(logical_line_contents, tokens):
    for o in (
        "==", ">=", "!=", "<=", "<", ">"
    ):
        before = logical_line_contents
        after = _specific_symbol(o, logical_line_contents, tokens, "INFIX_COMPARISON_OPERATOR")
        if before != after:
            return after
    return logical_line_contents


def infix_logical_operator(logical_line_contents, tokens):
    for o in (
            "and", "or", "xor",
    ):
        before = logical_line_contents
        after = _specific_symbol(o, logical_line_contents, tokens, "INFIX_LOGICAL_OPERATOR")
        if before != after:
            return after
    return logical_line_contents


def infix_mathematical_operator(logical_line_contents, tokens):
    for o in (
            "+", "-", "/", "*",
    ):
        before = logical_line_contents
        after = _specific_symbol(o, logical_line_contents, tokens, "INFIX_MATHEMATICAL_OPERATOR")
        if before != after:
            return after
    return logical_line_contents


def symbol(logical_line_contents, tokens):
    for o in (
            "~=", "=", ":", ",",
            "!", "=", "(", ")", "[", "]",
    ):
        before = logical_line_contents
        after = _specific_symbol(o, logical_line_contents, tokens, "SYMBOL")
        if before != after:
            return after
    return logical_line_contents


def constraint(logical_line_contents, tokens):
    if logical_line_contents.startswith("{") and len(logical_line_contents) > 1:
        for i in range(1, len(logical_line_contents) + 1):
            assert (i != len(logical_line_contents)), "constraints should be terminated by a }"
            if logical_line_contents[i] == "}":
                constraint_declaration = logical_line_contents[1:i]
                tokens.append({
                    "token": "CONSTRAINT",
                    "value": constraint_declaration
                })
                logical_line_contents = logical_line_contents[i+1:]
                break
    return logical_line_contents


TOKENIZERS = [
    leading_multi_line_comment,
    leading_single_line_comment,
    keyword,
    basic_type,
    literal,
    identifier,
    inline_comment,
    infix_logical_operator,
    infix_comparison_operator,
    infix_mathematical_operator,
    symbol,
    constraint,
    remainder
]


def tokenize(logical_line_contents):
    tokens = []
    while logical_line_contents:
        for tokenizer in TOKENIZERS:
            if tokenizer is keyword:
                if tokens:
                    last_token = tokens[-1]["token"]
                    last_value = tokens[-1]["value"]
                    if last_token == "SYMBOL" and last_value == ".":
                        continue
            logical_line_contents = logical_line_contents.lstrip()
            if not logical_line_contents:
                break
            new_logical_line_contents = tokenizer(logical_line_contents, tokens)
            if new_logical_line_contents != logical_line_contents:
                logical_line_contents = new_logical_line_contents
                break
    assert not logical_line_contents
    return tokens


class ManifestBuilder(ManifestBase):

    def __init__(self, transpilation_directory, sha256):
        super().__init__(transpilation_directory, sha256)
        self._tokenized_lines = []

    def tokenize_logical_line(self, logical_line_sha256, logical_line_contents):
        tokens = tokenize(logical_line_contents)
        self._tokenized_lines.append(TokenizedLine(
            logical_line_sha256,
            logical_line_contents,
            tokens
        ))

    def save(self):
        os.makedirs(self._tokenized_lines_directory, mode=0o777, exist_ok=True)
        manifest = {
            "module": {
                "sha256": self._module_sha256
            },
            "tokenized_lines": [l.logical_line_sha256 for l in self._tokenized_lines]
        }
        with io.open(self._tokenized_lines_manifest, 'w') as manifest_file:
            yaml.safe_dump(manifest, manifest_file)
        for l in self._tokenized_lines:
            filename = os.path.join(
                self._tokenized_lines_directory,
                l.logical_line_sha256 + ".yaml"
            )
            with io.open(filename, 'w') as tokenlized_line_file:
                yaml.safe_dump({
                    "sha256": l.logical_line_sha256,
                    "tokens": l.tokens
                }, tokenlized_line_file)
