from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class TimeLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.time"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


TimeLexeme.register([
    "time", "date", "moment", "interval", "timezone",
    "year", "years", "month", "months", "day", "days", "hour", "hours", "minute", "minutes", "second", "seconds", "millisecond", "milliseconds", "nanosecond", "nanoseconds",
    "utc", "now",
])
