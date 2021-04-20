# Actual Lines

An actual line of YAPL may not exceed 120 characters in width. This
constraint is intended first and foremost to enforce source code
readability. Actual lines are also known as `physical lines`.

# Logical Lines

Actual lines of YAPL code are however of little interest. They are
instead grouped into more interesting 'logical lines'.

Logical lines may consist of comments or code. As YAPL is considered
to be transpiled-first, comments are not stripped out of YAPL code
early during processing, but rather stored to inject into transpiled
source code.

The key difference between actual lines and logical lines is that
line-continuation markers have been resolved in logical lines.

## Structure and Indentation

YAPL uses an indentation scheme akin to that of Python to denote program
structure, based on 4 characters per indentation level. Tab characters are
illegal in YAPL files.

Unlike Python however, YAPL does not the : symbol or other additional
characters to denote a change in indentation level.

E.g.

```
    if a == b
        print("a == b")
```

Empty lines are ignored for the sake of structure, but superfluous
indentation is not and is not allowed.

## Comments

Logical lines consisting solely of comments may violate the line width-limit
if need be, but this is not recommended.

YAPL comments are denoted by prefixing content with `--`. The IDE should extend
comments that are prefixed with `---` to the end of the width limit, and should
save the line in that fashion to persistent storage. In this fashion, a powerful
IDE should assist external tools, such as `less`, `vim`, etc.

### Indentation

Comments in YAPL follow the same indentation rules as any other code.

### Multi-line Comments

Multi-line comments may consist of an unlimited number of lines.

The same notation is used for single and multi-line comments. In this regard, the
developer must cooperate with the transpiler, so that it can fulfill the
developer's needs for performance in a simple fashion.

### Semantic Comments
YAPL comments are semantic, in that they are associated with their surroundings in
a structured form.

A YAPL comment that is added to the end of a content line is
associated with that line, e.g.

```
    a = 1 -- initialize 'a'
```

A YAPL comment that is not initiated in this fashion is associated with the
subsequent line, e.g.

```
    -- this is a comment that will also be associated with 'a'
    a = 1
```

### Statements

YAPL does not provide a mechanism (e.g. ;) to indicate the termination of
a statement, which could e.g. be used to separate multiple statements on
a single line. This is an intentional language design choice.

### Single-line statements

A SLS of yapl-code can be evaluated in a REPL.
 
E.g.

```
    a = 1 + 2
```

### Multi-line statements

Line-continuation markers may be used to create multi-line YAPL statements.

The first line in a multi-line statement is called the *opening line*. The
final line is called the *closing line*. Lines between the two are called
*continuing lines*.

Opening and continuing lines of an MLS shall end with a line-continuation
marker (\), after having ignored all whitespace immediately before and after
the line-continuation marker. A line-continuation marker must be preceded by
at least one whitespace character.

All continuing and closing lines shall have an equal amount of leading
whitespace, which shall be at least one level of indentation (4 spaces)
greater than that of the opening line.

All line-continuation markers in the same MLS must be present in the same
text column number.

The first line following an MLS opening/continuing line that lacks a line-
continuation marker is considered to be the closing line for that MLS.

E.g.

```
    a =     \
        1 + \
        2
```

#### Multi-line strings

When two strings are adjacent after a line continuation symbol is
resolved, then they will be joined into the same string when transformed
from actual to logical lines.

E.g. 'a' and 'b' in the following are semantically equal

```
    a = "hello " \
        "world"
    b = "hello world"
```

YAPL also supports a multi-line string syntax using triple quotes. Multiline
strings should have no content on their first line, and should be indented
internally exactly one level from the declaring statement. Any additional
whitespace will be considered content of the string

E.g. a and b are semantically equal in the following

```
    a = """
        Hello World!

        This is a hello world program!

            It does hello-worldy things"""
    b = "Hello World!\n\nThis is a hello world program!\n\n    It does hello-worldy things"
```

## Minimum Expectations for Editors

A proper YAPL editor should:

* always replace tabs with 4 spaces
* align the leading white-space of all lines to increments of 4
* align the leading white-space of continuing lines
* align line-continuation markers by inserting/removing
additional whitespace before the marker on all lines of a MLS
* strip trailing whitespace from lines prior to saving
* extend triple-comments to the end of the legal actual line length
* provide a visual indication of the legal actual line length
  
