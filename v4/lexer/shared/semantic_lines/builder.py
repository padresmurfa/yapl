import collections
import copy
import os
import io
import yaml
import base64

from yapl.v4.lexer.shared.semantic_lines.base import ManifestBase

SemanticLine = collections.namedtuple(
    "SemanticLine", [
        "logical_line_sha256",
        "semantic_tokens"
    ]
)


def peek(n, input_tokens):
    if len(input_tokens) < n:
        return None
    return input_tokens[:n]


def is_identifier(t):
    return t["token"] == "IDENTIFIER"


def is_keyword(t, s):
    return t["token"] == "KEYWORD" and t["value"] == s.upper()


def is_basic_type(t):
    return t["token"] == "BASIC_TYPE"


def is_symbol(t, s):
    return t["token"] == "SYMBOL" and t["value"] == s


def is_leading_multi_line_comment(t):
    return t["token"] == "LEADING_MULTI_LINE_COMMENT"


def is_leading_single_line_comment(t):
    return t["token"] == "LEADING_SINGLE_LINE_COMMENT"


def is_inline_comment(t):
    return t["token"] == "INLINE_COMMENT"


def is_literal(t):
    return t["token"] in ("STRING_LITERAL", "INTEGER_LITERAL", "BOOLEAN_LITERAL")


def is_identifier_or_boolean_literal(t):
    return is_identifier(t) or t["token"] == "BOOLEAN_LITERAL"


def is_identifier_or_literal(t):
    return is_identifier(t) or is_literal(t)


def is_infix_logical_operator(t):
    return t["token"] == "INFIX_LOGICAL_OPERATOR"


def is_infix_comparison_operator(t):
    return t["token"] == "INFIX_COMPARISON_OPERATOR"


def is_infix_mathematical_operator(t):
    return t["token"] == "INFIX_MATHEMATICAL_OPERATOR"


def is_infix_operator(t):
    return t["token"] in ("INFIX_LOGICAL_OPERATOR", "INFIX_COMPARISON_OPERATOR", "INFIX_MATHEMATICAL_OPERATOR")


def is_constraint(t):
    return t["token"] == "CONSTRAINT"


def is_trailing_comment(t):
    return t["token"] == "INLINE_COMMENT"


def semantic_peek(analysers, input_tokens):
    peeked_input_tokens = peek(len(analysers), input_tokens)
    if peeked_input_tokens is not None:
        values = []
        for i in range(len(analysers)):
            t = input_tokens[i]
            if not analysers[i](t):
                return None
            if "value" in t:
                values.append(t["value"])
            else:
                values.append(None)
        del input_tokens[:len(analysers)]
        return values
    return None


def leading_comment(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_single_line_comment,
    ], input_tokens)
    if peeked_values is not None:
        cv = peeked_values
        output_semantic_tokens.append({
            "token": "LEADING_COMMENT",
            "leading_docstring": cv
        })
    return input_tokens


def semantic_identifier(input_tokens, output_semantic_tokens):
    appended = None
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        is_identifier,
    ], input_tokens)
    if peeked_values is not None:
        cv, iv = peeked_values
        appended = {
            "token": "SEMANTIC_IDENTIFIER",
            "identifier": iv,
            "leading_docstring": cv
        }
    else:
        peeked_values = semantic_peek([
            is_identifier
        ], input_tokens)
        if peeked_values is not None:
            iv = peeked_values[0]
            appended = {
                "token": "SEMANTIC_IDENTIFIER",
                "identifier": iv
            }
    if appended is not None:
        output_semantic_tokens.append(appended)
        peeked_values = semantic_peek([
            lambda t: is_symbol(t, ":"),
            lambda t: is_one_of(t, [
                is_basic_type,
                is_identifier
            ])
        ], input_tokens)
        if peeked_values is not None:
            appended["type"] = peeked_values[1]
        if input_tokens:
            peeked_values = semantic_peek([
                is_constraint
            ], input_tokens)
            if peeked_values is not None:
                appended["constraint"] = peeked_values[0]
        if input_tokens:
            peeked_values = semantic_peek([
                is_trailing_comment
            ], input_tokens)
            if peeked_values is not None:
                appended["trailing_docstring"] = peeked_values[0]
    return input_tokens


def renamed_return_value(input_tokens, output_semantic_tokens):
    tmp = input_tokens[:4]
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "return"),
        is_identifier,
        lambda t: is_symbol(t, "="),
        lambda t: is_expression(input_tokens[3:])
    ], tmp)
    print("xcxc! " + str(input_tokens[3:]))
    print("      " + str(peeked_values))
    if peeked_values is not None:
        _, iv, _, _ = peeked_values
        del input_tokens[0]
        output_semantic_tokens.append({
            "token": "RENAMED_RETURN_VALUE",
            "name": iv
        })
        return expression(input_tokens, output_semantic_tokens)
    return input_tokens


def correctly_named_return_value(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "return"),
        is_identifier,
        lambda t: not (is_symbol(t, "=") or is_symbol(t, "~="))
    ], input_tokens + [{"token": "SYMBOL", "value": "asdf"}])
    if peeked_values is not None:
        _, iv, _ = peeked_values
        output_semantic_tokens.append({
            "token": "CORRECTLY_NAMED_RETURN_VALUE",
            "name": iv
        })
    return input_tokens


def named_yield(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "yield"),
        is_identifier,
        lambda t: is_symbol(t, "="),
        lambda t: is_expression(input_tokens[2:])
    ], input_tokens[:4])
    if peeked_values is not None:
        del input_tokens[:3]
        _, iv, _ = peeked_values
        output_semantic_tokens.append({
            "token": "NAMED_YIELD_VALUE",
            "name": iv
        })
        return expression(input_tokens, output_semantic_tokens)
    return input_tokens


def unit_test_suite_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "unit"),
        lambda t: is_keyword(t, "test"),
        lambda t: is_keyword(t, "suite"),
        lambda t: is_keyword(t, "for"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, _, _, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "UNIT_TEST_SUITE_DECLARATION",
            "for_identifier": iv,
            "leading_docstring": cv
        })
    return input_tokens


def function_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "function"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "FUNCTION_DECLARATION",
            "name": iv,
            "leading_docstring": cv
        })
    return input_tokens


def method_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "method"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "METHOD_DECLARATION",
            "name": iv,
            "leading_docstring": cv
        })
    return input_tokens


def generator_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "generator"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "GENERATOR_DECLARATION",
            "name": iv,
            "leading_docstring": cv
        })
    return input_tokens


def immutable_let(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_identifier,
        lambda t: is_symbol(t, "="),
        lambda t: is_expression(input_tokens[2:])
    ], input_tokens[:3])
    if peeked_values is not None:
        del input_tokens[:2]
        iv, _, _ = peeked_values
        output_semantic_tokens.append({
            "token": "IMMUTABLE_LET",
            "name": iv
        })
        return expression(input_tokens, output_semantic_tokens)
    return input_tokens


def mutable_let(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_identifier,
        lambda t: is_symbol(t, "~="),
        lambda t: is_expression(input_tokens[2:])
    ], input_tokens[:3])
    if peeked_values is not None:
        del input_tokens[:2]
        iv, _, _ = peeked_values
        output_semantic_tokens.append({
            "token": "MUTABLE_LET",
            "name": iv
        })
        return expression(input_tokens, output_semantic_tokens)
    return input_tokens


def is_one_of(t, patterns):
    for p in patterns:
        if p(t):
            return True
    return False


def structure_section(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "public"),
            lambda t: is_keyword(t, "private"),
            lambda t: is_keyword(t, "protected")
        ]),
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "instance"),
            lambda t: is_keyword(t, "class"),
        ]),
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "state"),
            lambda t: is_keyword(t, "methods"),
            lambda t: is_keyword(t, "properties"),
            lambda t: is_keyword(t, "initializers"),
        ]),
    ], input_tokens)
    if peeked_values is not None:
        av, sv, wv = peeked_values
        output_semantic_tokens.append({
            "token": "STRUCTURE_SECTION",
            "access": av.upper(),
            "level": sv.upper(),
            "section": wv.upper()
        })
    return input_tokens


def empty_check(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_identifier,
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "is"),
            lambda t: is_keyword(t, "are"),
        ]),
        lambda t: is_keyword(t, "empty")
    ], input_tokens)
    if peeked_values is not None:
        iv, _, _ = peeked_values
        output_semantic_tokens.append({
            "token": "CHECK_IF_EMPTY",
            "identifier": iv
        })
    return input_tokens


def if_then_else(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "if"),
            lambda t: is_keyword(t, "then"),
            lambda t: is_keyword(t, "else")
        ])
    ], input_tokens)
    if peeked_values is not None:
        v = peeked_values[0]
        output_semantic_tokens.append({
            "token": "IF_THEN_ELSE_BLOCK",
            "statement": v.upper()
        })
    return input_tokens


def property_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "property")
    ], input_tokens)
    if peeked_values is not None:
        cv = peeked_values[0]
        before = len(output_semantic_tokens)
        semantic_identifier(input_tokens, output_semantic_tokens)
        after = len(output_semantic_tokens)
        assert before != after, "expected a semantic identifier to follow a property statement"
        last_token = output_semantic_tokens[-1]
        last_token["leading_docstring"] = cv
        last_token["token"] = "PROPERTY_DECLARATION"
    return input_tokens


def repeat_loop(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "repeat"),
    ], input_tokens)
    if peeked_values is not None:
        v = peeked_values[0]
        output_semantic_tokens.append({
            "token": "LOOP",
            "statement": v.upper()
        })
    return input_tokens


def for_loop(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "for"),
        is_identifier,
        lambda t: is_keyword(t, "in"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        _, cv, _, wv = peeked_values
        output_semantic_tokens.append({
            "token": "LOOP",
            "statement": "FOR",
            "cursor": cv,
            "collection": wv
        })
    return input_tokens


def function_section(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "accepts"),
            lambda t: is_keyword(t, "yields"),
            lambda t: is_keyword(t, "returns"),
            lambda t: is_keyword(t, "body")
        ])
    ], input_tokens)
    if peeked_values is not None:
        v = peeked_values[0]
        output_semantic_tokens.append({
            "token": "FUNCTION_SECTION",
            "section": v.upper()
        })
    return input_tokens


def module_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "module"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "MODULE_DECLARATION",
            "module": iv,
            "leading_docstring": cv
        })
    return input_tokens


def infix_operator(input_tokens, output_semantic_tokens):
    before = input_tokens[:3]
    peeked_values = semantic_peek([
        is_identifier_or_literal,
        is_infix_operator,
        is_identifier_or_literal
    ], input_tokens)
    if peeked_values is not None:
        lv, ov, rv = peeked_values
        output_semantic_tokens.append({
            "token": "INFIX_OPERATOR",
            "left": before[0],
            "right": before[2],
            "operator": ov.upper()
        })
    return input_tokens


def discard_statement(input_tokens, output_semantic_tokens):
    t = input_tokens[0]
    if is_keyword(t, "discard"):
        output_semantic_tokens.append({
            "token": "DISCARD_EVALUATION_RESULTS"
        })
        del input_tokens[0]
    return input_tokens


def instantiate_object(input_tokens, output_semantic_tokens):
    tmp_tokens = input_tokens[:2]
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "new"),
        is_identifier
    ], tmp_tokens)
    if peeked_values is not None:
        output_semantic_tokens.append({
            "token": "INSTANTIATE_OBJECT"
        })
        del input_tokens[0]
    return input_tokens


def export_new_token(input_tokens, output_semantic_tokens):
    tmp_input_tokens = copy.deepcopy(input_tokens)
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "export"),
        lambda t: is_one_of(t, [
            lambda t: is_keyword(t, "function"),
            lambda t: is_keyword(t, "class"),
            lambda t: is_keyword(t, "type")
        ]),
        is_identifier
    ], tmp_input_tokens)
    if peeked_values is not None:
        _, _, wv, iv = peeked_values
        output_semantic_tokens.append({
            "token": "EXPORT_NEW_TOKEN",
            "what": wv,
            "identifier": iv
        })
        del input_tokens[1]
    else:
        peeked_values = semantic_peek([
            is_leading_multi_line_comment,
            lambda t: is_keyword(t, "export"),
            lambda t: is_keyword(t, "compound"),
            lambda t: is_keyword(t, "value"),
            lambda t: is_keyword(t, "type"),
            is_identifier
        ], tmp_input_tokens)
        if peeked_values is not None:
            _, _, _, _, _, iv = peeked_values
            output_semantic_tokens.append({
                "token": "EXPORT_NEW_TOKEN",
                "what": "COMPOUND_VALUE_TYPE",
                "identifier": iv
            })
            del input_tokens[1]
    return input_tokens


def compound_value_type_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "compound"),
        lambda t: is_keyword(t, "value"),
        lambda t: is_keyword(t, "type"),
        is_identifier
    ], input_tokens)
    if peeked_values is not None:
        cv, _, _, _, iv = peeked_values
        output_semantic_tokens.append({
            "token": "COMPOUND_VALUE_TYPE_DECLARATION",
            "identifier": iv,
            "leading_docstring": cv
        })
    return input_tokens


def simple_type_declaration(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        is_leading_multi_line_comment,
        lambda t: is_keyword(t, "type")
    ], input_tokens)
    if peeked_values is not None:
        cv, _ = peeked_values
        before = len(input_tokens)
        semantic_identifier(input_tokens, output_semantic_tokens)
        assert len(input_tokens) != before, "expected 'type' to be followed by a semantic identifier"
        output_semantic_tokens[-1]["token"] = "SIMPLE_TYPE_DECLARATION"
        output_semantic_tokens[-1]["leading_docstring"] = cv
    return input_tokens


def function_call(input_tokens, output_semantic_tokens):
    if output_semantic_tokens:
        last_token = output_semantic_tokens[-1]
        if last_token["token"] == "SEMANTIC_IDENTIFIER":
            peeked_values = semantic_peek([
                lambda t: is_symbol(t, "(")
            ], input_tokens)
            arguments = []
            if peeked_values is not None:
                while input_tokens:
                    peeked_values = semantic_peek([
                        lambda t: is_symbol(t, ")")
                    ], input_tokens)
                    if peeked_values is not None:
                        break
                    if arguments:
                        peeked_values = semantic_peek([
                            lambda t: is_symbol(t, ",")
                        ], input_tokens)
                        assert peeked_values is not None, "yapl function arguments must be comma-separated"
                    peeked_values = semantic_peek([
                        is_identifier
                    ], input_tokens)
                    assert peeked_values is not None, "yapl function arguments must always be named"
                    arg_name = peeked_values[0]
                    arg_value_identifier = arg_name
                    peeked_values = semantic_peek([
                        lambda t: is_symbol(t, "=")
                    ], input_tokens)
                    if peeked_values is not None:
                        peeked_values = semantic_peek([
                            is_identifier
                        ], input_tokens)
                        if peeked_values is not None:
                            arg_value_identifier = peeked_values[0]
                        else:
                            arg_value_literal = input_tokens[0]
                            peeked_values = semantic_peek([
                                is_literal
                            ], input_tokens)
                            assert peeked_values is not None, "yapl function arguments must be populated with identifiers or values"
                            arguments.append({
                                "name": arg_name,
                                "value": {
                                    "literal": arg_value_literal
                                }
                            })
                            continue
                    arguments.append({
                        "name": arg_name,
                        "value": {
                            "identifier": arg_value_identifier
                        }
                    })
                token = "FUNCTION_CALL"
                if len(output_semantic_tokens) > 1:
                    if output_semantic_tokens[-2]["token"] == "INSTANTIATE_OBJECT":
                        token = "CONSTRUCTOR_CALL"
                        del output_semantic_tokens[-2]
                last_token["token"] = token
                last_token["arguments"] = arguments
    return input_tokens


def import_statement(input_tokens, output_semantic_tokens):
    peeked_values = semantic_peek([
        lambda t: is_keyword(t, "from"),
        is_identifier,
        lambda t: is_keyword(t, "import"),
        is_identifier,
    ], input_tokens)
    if peeked_values is not None:
        _, mv, _, iv = peeked_values
        symbols = [ iv ]
        def more():
            peeked_values = semantic_peek([
                lambda t: is_symbol(t, ","),
                is_identifier,
            ], input_tokens)
            if peeked_values is None:
                return False
            else:
                _, iv = peeked_values
                symbols.append(iv)
                return True
        while more():
            pass
        output_semantic_tokens.append({
            "token": "IMPORT_SYMBOLS_FROM_MODULE",
            "module": mv,
            "symbols": symbols
        })
    return input_tokens


def semantic_literal(input_tokens, output_semantic_tokens):
    before = input_tokens[0]
    print("is this a literal? " + str(input_tokens))
    peeked_values = semantic_peek([
        is_literal
    ], input_tokens)
    if peeked_values is not None:
        print("xcxc sem lit")
        lv = peeked_values[0]
        output_semantic_tokens.append({
            "token": "SEMANTIC_" + before["token"],
            "literal": lv
        })
    return input_tokens


def logical_expression(input_tokens, output_semantic_tokens):
    before = input_tokens[:3]
    peeked_values = semantic_peek([
        is_identifier_or_boolean_literal,
        is_infix_logical_operator,
        is_identifier_or_boolean_literal
    ], input_tokens)
    if peeked_values is not None:
        lv, ov, rv = peeked_values
        output_semantic_tokens.append({
            "token": "LOGICAL_EXPRESSION",
            "left": before[0],
            "right": before[2],
            "operator": ov.upper()
        })
    return input_tokens


def is_expression(input_tokens):
    before = len(input_tokens)
    expression(input_tokens, [])
    after = len(input_tokens)
    return before != after


def expression(input_tokens, output_semantic_tokens):
    for e in [
        logical_expression, semantic_literal
    ]:
        before = len(input_tokens)
        e(input_tokens, output_semantic_tokens)
        after = len(input_tokens)
        if before != after:
            break
    return input_tokens


def remainder(input_tokens, output_semantic_tokens):
    if input_tokens:
        output_semantic_tokens.append({
            "token": "REMAINDER",
            "value": input_tokens
        })
    return []


SEMANTIC_ANALYZERS=[
    discard_statement,
    export_new_token,
    expression,
    infix_operator,
    repeat_loop,
    for_loop,
    empty_check,
    function_section,
    if_then_else,
    mutable_let,
    immutable_let,
    leading_comment,
    structure_section,
    instantiate_object,
    semantic_identifier,
    function_call,
    renamed_return_value,
    correctly_named_return_value,
    named_yield,
    simple_type_declaration,
    compound_value_type_declaration,
    method_declaration,
    property_declaration,
    generator_declaration,
    function_declaration,
    unit_test_suite_declaration,
    import_statement,
    module_declaration,
    remainder
]


def changed(l, r):
    if len(l) != len(r):
        return True
    for i in range(len(l)):
        lt = l[i]
        rt = r[i]
        if lt["token"] != rt["token"]:
            return True
        if lt["value"] != rt["value"]:
            return True
    return False


def perform_semantic_line_analysis(tokens):
    semantic_tokens = []
    while tokens:
        for analyzer in SEMANTIC_ANALYZERS:
            before = copy.deepcopy(tokens)
            after = analyzer(tokens, semantic_tokens)
            if changed(before, after):
                tokens = after
                break
    assert not tokens
    return semantic_tokens


class ManifestBuilder(ManifestBase):

    def __init__(self, transpilation_directory, sha256):
        super().__init__(transpilation_directory, sha256)
        self._lines = []

    def process_line(self, logical_line_sha256, tokens):
        before = copy.deepcopy(tokens)
        semantic_tokens = perform_semantic_line_analysis(tokens)
        if semantic_tokens[-1]["token"] == "REMAINDER":
            if logical_line_sha256 == "0ae365b24e4bcdc7486dda3ea3f6b394ae82e0eab0bbc048146496cdc1ad834b":
                print("----------------------------------------------------------------")
                print("{} REMAINDER:\n\tBEFORE: {}\n\tAFTER:{}\n\tPROCESSED:{}".format(
                    logical_line_sha256,
                    str(before),
                    str(tokens),
                    str(semantic_tokens[:-1])
                ))

        self._lines.append(SemanticLine(
            logical_line_sha256,
            semantic_tokens
        ))

    def save(self):
        os.makedirs(self._semantic_lines_directory, mode=0o777, exist_ok=True)
        manifest = {
            "module": {
                "sha256": self._module_sha256
            },
            "semantic_lines": [l.logical_line_sha256 for l in self._lines]
        }
        with io.open(self._semantic_lines_manifest, 'w') as f:
            yaml.safe_dump(manifest, f)
        for l in self._lines:
            filename = os.path.join(
                self._semantic_lines_directory,
                l.logical_line_sha256 + ".yaml"
            )
            with io.open(filename, 'w') as f:
                yaml.safe_dump({
                    "sha256": l.logical_line_sha256,
                    "semantic_tokens": l.semantic_tokens
                }, f)
