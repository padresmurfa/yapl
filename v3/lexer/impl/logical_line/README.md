# Actual Lines

An actual line of YAPL may not exceed 80 characters in width. This
constraint is intended first and foremost to encourage source code
readability.

# Logical Lines

Actual lines of YAPL code are however of little interest. They are
instead grouped into 'logical lines'.

Logical lines may consist of comments or code. As YAPL is considered
to be transpiled-first, comments are not stripped out of YAPL code
early during processing, but rather stored to inject into transpiled
source code.

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
indentation is not and is not allowed except in multi-line comments.

## Comments

Logical lines consisting solely of comments may violate the 80 character
width-limit if need be, but this is not recommended. Multi-line comments may
consist of an unlimited number of lines, although transpilers are not required
to perform well beyond a reasonable limit (1000 lines / 80.000 characters).

YAPL comments may be *semantic* or *non-semantic*, *single-line* or *multi-line*.

### Non-semantic comments

Non-semantic comments in YAPL have no special meaning to their surroundings, other
than their position between statements. During transpilation, they will be injected
in an equivalent position to the extent possible.

Non-semantic comments are denoted using the `#` and `/# #/` tokens.

### Semantic comments

Unlike their non-semantic counterparts, semantic comments are more akin to javadoc
comments. Semantic comments are associated with the following statement, and must
adhere to certain structural norms. These will be discussed in a later section (xcxc)

Semantic comments are denoted using the `//` and `/* */` tokens.

### Single-line comments

Single-line comments in YAPL follow the same indentation rules as other statements.
At least one space character must separate the comment token from the comment text.

Thus the following is a legal comment statement in YAPL:

```
    # this is a comment
    a = 1
```

The following on the other hand is not a legal comment statement in YAPL:

```
// this is a comment
    a = 1
```

### Multi-line comments

Multi-line comments in YAPL follow the same indentation rules as block statements,
using indentation. Thus the actual comments must be indented internally at least
one level beyond the starting position of the opening comment token. Superfluous
whitespace is allowed, and will be retained by transpilation. The opening and
closing line of a multi-line comment in YAPL may not however contain comment content.

Thus the following is a legal multi-line comment statement in YAPL:

```
    /#
        this is a multi-line comment
    #/
```

The following on the other hand is not a legal comment statement in YAPL:

```
    /*
    this is a multi-line comment
    */
    a = 1
```

Multi-line comments are nestable, e.g.:

```
    /#
        this is a multi-line comment
        /#
            this is an embedded multi-line comment
        #/
    #/
```

### Multi-line comments using single-line comment tokens

Multi-line comments may likewise be created using subsequent lines of single-line
comments.

E.g.

```
    # hello
    # world
    hello_world()
```

or

```
    // hello
    // world
    hello_world()
```

## Statements

Logical lines that contain statements may not exceed 160 characters in total
length. This limited is intended to create an upper limit on the amount of
computing power requiired to process a single line of YAPL code, as
YAPL is intended to support massively-parallel distributed
transpilation using logical-lines as a core unit of abstraction.

The following exemptions are made to this rule:

* data declarations are not limited in total length, such as static strings and
arrays
* inline comments do not count towards this limit, except where they violate
the length constraints of a comment line

### On the topic of multiple statements per line

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

A MLS of yapl-code may be joined into a single logical line for execution.

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
resolved, then will be joined into the same logical line.

E.g. 'a' and 'b' in the following are semantically equal

```
    a = "hello " \
        "world"
    b = "hello world"
```

YAPL also supports a multi-line string syntax using triple quotes. Multiline
strings should have no content on their first line, and should be indented
internally one level from the declaring statement.

E.g. a and b are semantically equal in the following

```
    a = """
            Hello World!

            This is a hello world program!

            It does hello-worldy things"""
    b = "Hello World!\n\nThis is a hello world program!\n\nIt does hello-worldy things"
```

## Editors

A proper YAPL editor should:

* replace tabs with 4 spaces
* align the leading white-space of all lines to increments of 4
* align the leading white-space of continuing lines
* align line-continuation markers by inserting/removing
additional whitespace before the marker on all lines of a MLS
* strip trailing whitespace from lines prior to saving
  
