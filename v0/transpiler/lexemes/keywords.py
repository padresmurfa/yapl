from .base.dynamic_symbol import DynamicSymbolLexeme
from .identifier import IdentifierLexeme


class KeywordSymbolLexeme(DynamicSymbolLexeme):

    lexeme_id = "keywords.keyword"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


KeywordSymbolLexeme.register([

    # undecided, or not yet dealt with
    "_",

    "reentrant", "threadsafe", "recursive",

    "module", "class", "interface", "abstract", "protocol",
    "ducktype", "duck",
    "this", "args", "superclass",
    "structure", "type", "alias",
    "composite", "component", "composer",
    "private", "public", "protected",
    "overridable", "override",
    "is", "as",
    "singleton",
    "constructor", "disowned",
    "extends", "implements",
    "trait", "mixin", "sealed",
    "identifier",

    "new",
    "let", "constant",

    "import", "from", "package", "export",

    "scope",
    "static",
    "lazy",
    "enumeration",
    "shared",

    "assert", "validate",
    "logger", "metrics"
    "test", "testing", "mock",

    "serialise", "deserialise",

    "modulo", "**", "pow",
    "collection", "array", "map", "set", "iterator", "list", "tuple", "queue", "hashtable", "bag", "heap", "stack",
    "mutable", "immutable",

    "transaction", "commit", "rollback",
    "dataset", "index", "foreignkey", "unique",

    "using", "lock",
    "heap", "stack",
    "implicit",
    "property",
    "async", "await", "run",
    "generic",
    "actor", "select",
    "channel", "send", "receive",
    "consumer", "producer",
    "message",
    "thread", "fiber",

    "getbit", "setbit", "getbyte", "setbyte",
    "bitwise_and"
    "ffs", "ctz", "ntz", "popcount", "shift",

    "process", "service"

])
