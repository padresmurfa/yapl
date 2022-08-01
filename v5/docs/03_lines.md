# Lines of Code

YAPL follows Python's train of thought regarding using indentation to denote structure, based on the opinion that this style is more readable and maintainable than that used by other programming languages.

## 1. Whitespace

A YAPL program is divided into a number of logical lines. The end of a logical line is represented by the token NEWLINE. Statements cannot cross logical line boundaries except where NEWLINE is allowed by the syntax (e.g., between statements in compound statements). A logical line is constructed from one or more physical lines by following the implicit line joining rules.

## Why?

Python is generally more readable than all other past and present programming languages. Its the py-way or the hi-way.

## 2. Physical lines vs logical lines

A physical line of text is a line of code found in a file. YAPL is however generally only concerned with logical lines of text. Usually each physical line is translated into a single logical line, but there are exceptions.

## Why?

Python rulez.

## 3. No tabs

A YAPL file should not contain tab characters, but if it does, they will be interpreted as exactly 4-spaces. YAPL-aware editors should strip tabs upon saving by default.

### Why?

The relaxed interpretation of tabs within Python is a sore spot.

## 4. Indentation

Leading whitespace at the beginning of a logical line is used to compute the indentation level of the line.
 
Indentation is rejected as inconsistent if it is not provided as a multiple of 4 spaces.

Comments must start in a fashion that follows the same indentation rules as code, but indentation within comments in not considered syntactical.

### Why?

Professional developers use linters and formatters. Supporting variable indentation is pointless, and it almost exclusively is a code-smell. 4-character-indent seems to be the norm, having won out due to aesthetics, but editors may opt to support visualising leading indentation in a condensed fashion to save screen space for developers who favour a 2-character-indent style.

## 5. Implicit line joining in statements

Sequences of physical lines are implicitly joined into a single logical line when the following hold true:

* the first physical line ends by opening a parenthesis or bracket
* the subsequential physical lines are indented by one INDENT from the first in the sequence
* the last physical line is indented at the same level as the first physical line in the sequence
* each of the subsequential lines (i.e. excluding the first and last line, which only hold the opening/closing symbol) are terminated by a trailing comma
* the trailing comma is optional in the last subsequential line

```
bar = [
    "a",
    "b",
]
```

### Why?

Python also rulez here.

## 6. Multi-line strings

Sequences of physical lines within a multi-line string are implicitly joined into a single string:

* the first physical line ends with a """
* the subsequential physical lines are indented by exactly one INDENT from the first in the sequence
* the last physical line is indented at the same level as the first physical line in the sequence
* any leading whitespace beyond the INDENT is considered part of the multi-line string
* newlines in multi-line strings are interpreted as nothing. To include an actual newline, use the \n escape sequence

```
foo = """
    And where's that soggy plain?\n
    In Spain In Spain\n
    The rain in spain
     stays mainly in the plain.\n
    The rain in spain stays mainly in the plain.\n
"""
```

### Why?

Multi-line strings are cool, but typically programming languages use fudgy definitions that make it hard to format them prettily in code, and the rules around newlines in multi-line strings typically seem dodgy.

## 7. Length constraints

A line of physical YAPL should not be more than 128 characters. A logical line should not be more than 65536 characters. These are soft constraints.

### Why?

To place a reasonable, albeit arbitrary, constraint on what YAPL tooling should be expected to performantly support.
