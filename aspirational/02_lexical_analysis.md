## 2. Lexical Analysis

A YAPL program is read by a parser. Input to the parser is a stream of tokens, generated by the lexical analyzer. This chapter describes how the lexical analyzer breaks a file into tokens.

YAPL code is Unicode text encoded in UTF-8. The text is not canonicalized, so a single accented code point is distinct from the same character constructed from combining an accent and a letter; those are treated as two code points. For simplicity, this document will use the unqualified term character to refer to a Unicode code point in the source text.

Each code point is distinct; for instance, upper and lower case letters are different characters.

Implementation restriction: For compatibility with other tools, a compiler should disallow the NUL character (U+0000) in the source text and ignore a UTF-8-encoded byte order mark (U+FEFF) if it is the first Unicode code point in the source text. A byte order mark may be disallowed anywhere else in the source.

### 2.1. Notation

The syntax is specified using a Parsing Expression Grammar [(PEG)](https://en.wikipedia.org/wiki/Parsing_expression_grammar) compatible with pest.rs's [.pest file format](https://docs.rs/pest_derive/2.1.0/pest_derive/)

### 2.2. Whitespace

A YAPL program is divided into a number of logical lines.

#### 2.2.1. Logical lines

The end of a logical line is represented by the token NEWLINE. Statements cannot cross logical line boundaries except where NEWLINE is allowed by the syntax (e.g., between statements in compound statements). A logical line is constructed from one or more physical lines by following the implicit line joining rules.

#### 2.2.2. Physical lines

A physical line is a sequence of characters terminated by an end-of-line sequence. In source files and strings, any of the standard platform line termination sequences can be used - the Unix form using ASCII LF (linefeed), the Windows form using the ASCII sequence CR LF (return followed by linefeed), or the old Macintosh form using the ASCII CR (return) character. All of these forms can be used equally, regardless of platform. The end of input also serves as an implicit terminator for the final physical line.

When embedding YAPL, source code strings should be passed to YAPL APIs using the standard C conventions for newline characters (the \n character, representing ASCII LF, is the line terminator).

#### 2.2.3. Tabs

YAPL code may not contain tab characters. Tabs must be replaced (from left to right) by one to four spaces such that the total number of characters up to and including the replacement is a multiple of four. The total number of spaces preceding the first non-blank character then determines the line’s indentation.

This replacement should be done prior to the compilation phase, e.g. by a YAPL aware editor or by preprocessing the YAPL file.

#### 2.2.4. Indentation

Leading whitespace (spaces and tabs) at the beginning of a logical line is used to compute the indentation level of the line.
 
Indentation is rejected as inconsistent if it is not provided as a multiple of 4 spaces.

Comments must follow the same indentation rules as code.

The indentation levels of consecutive lines are used to generate INDENT and DEDENT tokens, using a stack, as follows.

Before the first line of the file is read, a single zero is pushed on the stack; this will never be popped off again. The numbers pushed on the stack will always be strictly increasing from bottom to top. At the beginning of each logical line, the line’s indentation level is compared to the top of the stack. If it is equal, nothing happens. If it is larger, it is pushed on the stack, and one INDENT token is generated. If it is smaller, it must be one of the numbers occurring on the stack; all numbers on the stack that are larger are popped off, and for each number popped off a DEDENT token is generated. At the end of the file, a DEDENT token is generated for each number remaining on the stack that is larger than zero.

Indentation is used in conjunction with curly braces to determine the grouping of statements.

An INDENT must be immediately preceeded by an opening curly brace. A DEDENT must be immediately succeeded by a closing curly brace, BLOCK-CONTINUATION statement (else, catch, finally). An opening curly brace may not occur on a line by itself. A BLOCK-CONTINUATION statement must occur on the same line as both the closing and opening curly braces that it is associated with.

Here is a snippet of YAPL code demonstrating correct usage of indentation and curly-braces:
    
```
function perm(l) {
    try {
        // Compute the list of all permutations of l
        if l.length() <= 1 {
            return [l]
        } else {
            r = []
            for i in range(l.length()) {
                s = l.left(i) + l.substring(i+1)
                p = perm(s)
                for x in p {
                    r.append(l.substring(i, i + 1) + x)
                }
            }
            return r
        }
    } catch IOError(e) {
        print("WAT???")
        throw e
    } finally {
        print("DONE")
    }
}
```

And here is a snippet of YAPL code demonstrating incorrect usage of indentation and curly-braces:

The following example shows various indentation and curly-brace placement errors:

```
    function perm(l) {                          // error: first line indented
    for i in range(l.length()):                 // error: not indented
    {                                           // error: opening curly brace alone on line
      // iterate over l                         // error: comment incorrectly indented
        s = l.left(i) + l.substring(i+1)        //    
            p = perm(s)                         // error: unexpected indent
        for x in p:                             //
            print("hello world")                // error: missing opening curly after ident
           r.append(l.substring(i, i + 1) + x)  // error: indentation not in increments of 4
        return r                                // error: inconsistent dedent
                                                // error: dedent without closing curly braces
```

#### 2.2.5. Implicit line joining

##### 2.2.5.1. Square brackets

Expressions in square brackets can be split over more than one physical line, following the same indentation rules as curly braces.

Implicitly continued lines can carry comments. Blank continuation lines are not allowed. There is no NEWLINE token between implicit continuation lines. 

Here is a snippet of YAPL code demonstrating correct usage of indentation and square-brackets:

```
month_names = [
    "Januari", "Februari", "Maart",      // These are the
    "April",   "Mei",      "Juni",       // Dutch names
    "Juli",    "Augustus", "September",  // for the months
    "Oktober", "November", "December",   // of the year
]
```

Here is a snippet of YAPL code demonstrating incorrect usage of indentation and square-brackets:

```
month_names = ["Januari", "Februari", "Maart",  // error: opening square-bracket must be immediately followed by INDENT
        "April",   "Mei",      "Juni",          // error: only one INDENT should occur
         "Juli",    "Augustus", "September",    // error: inconsistent INDENT
        "Oktober", "November", "December"]      // error: closing square-bracked must be immediately preceded by DEDENT
```

##### 2.2.5.2. Parenthesis in expressions

Logical and arithmetic expressions in parenthesis can be split over more than one physical line.

The following rules apply to indentation with parenthesis.
- the opening line may not contain a operator
- the opening line must be immediately succeeded by one and only one INDENT
- each subsequent continuation line must start with an operator (and, or, xor, +, -, *, /)
- each subsequent continuation line must contain one and only one operator outside of parenthesis
- the last continuation line must contain a closing parenthesis

Implicitly continued lines can carry comments. Blank continuation lines are not allowed. 

Here is a snippet of YAPL code demonstrating correct usage of indentation and parenthesis in a logical expression:

```
if (foo
    and blat
    and (bark or growl)     // note: extra operators are allowed within parenthesis
    and (brar
        or brarf)
    and bork) {
```

And here is a snippet of YAPL code demonstrating incorrect usage of indentation and parenthesis in a logical expression:

```
if (foo and blat            // error: the opening line may not contain a operator
        and bork            // error: the opening line must be immediately succeeded by one and only one INDENT
    and garf or dorg        // error: each subsequent continuation line must contain one and only one operator outside of parenthesis
    and gorg or (a or b)    // error: again, each subsequent continuation line must contain one and only one operator outside of parenthesis
    and (gu
    or bu)                  // error: sub-expression in parenthesis must also follow valid indentation rules.
    gurgle                  // error: each subsequent continuation line must start with a logical operator (and, or, xor) and each subsequent continuation line must contain one and only one logical operator
) {                         // error: the last continuation line must contain a closing parenthesis
```

Likewise, an example of correct usage of indentation and parenthesis in an arithmetic expression:

```
foo = (smoorfasa
    + (smu * ur / ff)
    + ((smu + r + ff - f)
        / sss))
```

And finally, an example of incorrect usage of indentation and parenthesis in an arithmetic expression:

```
foo = (smoor + fasa         // error: the opening line may not contain a operator
        + smu * ur          // error: the opening line must be immediately succeeded by one and only one INDENT 
    / f / f                 // each subsequent continuation line must contain one and only one operator
    + ((smurff - f)         // error: sub-expression in parenthesis must also follow valid indentation rules.
    / sss)                  //
    smusmurrf               // error: each subsequent continuation line must start with an operator (+, -, *, /) and each subsequent continuation line must contain one and only one operator
)                           // error: the last continuation line must contain a closing parenthesis
```

##### 2.2.5.3. Parenthesis in function parameters

Function parameters and parameter declarations may be split over multiple lines.

```
function foo(
    blat = int,
    foo = bool(true),
    mutable bar = bool(false)
    bar := true)
    
i = int(0)
mutable v = int(0)
v := v + 1

bar := 3

type inference, not in parameters, member variables, or return values
```

#### 2.2.8. Whitespace between tokens

Except at the beginning of a logical line or in string literals, the space character should be used to separate tokens. Whitespace is needed between two tokens if their concatenation could otherwise be interpreted as a different token (e.g., ab is one token, but a b is two tokens).

#### 2.2.9. Whitespace consistency

A YAPL file should use consistent whitespace rules.  A YAPL compiler/transpiler should treat any detected inconsistencies as a compilation error.

#### 2.2.10. Escape Sequences

The following escape sequences are recognized in character and string literals.

| charEscapeSeq | unicode | name | notes |
| --- | --- | --- | --- |
| ‘\‘ ‘t‘  | \u0009 | horizontal tab | HT |
| ‘\‘ ‘n‘  | \u000a | linefeed | LF |
| ‘\‘ ‘r‘  | \u000d | carriage return | CR |
| ‘\‘ ‘"‘  | \u0022 | double quote | " |
| ‘\‘ ‘\‘  | \u005c | backslash | \ |
| ‘\‘ ‘$‘  | \u0024 | dollar sign | $ |
| ‘\‘ ‘||‘  |  | margin | When placed at the start of a multi-line string, allows retaining the margin |
| ‘\N‘ ‘{name}‘  |  | <name> | Character named name in the Unicode database |
| ‘\u‘ ‘xxxx‘  | \uxxxx |  | Character with 16-bit hex value xxxx |
| ‘\U‘ ‘xxxxxxxx‘  | \uxxxxxxxx |  | Character with 32-bit hex value xxxxxxxx |

It is a compile time error if a backslash character in a character or string literal does not start a valid escape sequence.

#### 2.2.11. Trailing Commas

If a comma (,) is followed immediately, ignoring whitespace and newlines, a closing parenthesis ()), bracket (]), or brace (}), then the comma is treated as a "trailing comma" and is ignored. For example:

```
foo(
  23,
  "bar",
  true,
)
```

#### 2.3. Comments

Comments are generally ignored by the syntax, but are included during transpiling, and are available during various debugging scenarios.

They come in three forms:

- A single-line comment is a sequence of characters which starts with // and extends to the end of the physical line. A single-line comment signifies the end of the logical line unless the implicit line joining rules are invoked. 
- A multi-line comment is a sequence of characters between /* and */.  A multi-line comment may be used in any place a space character would be valid. does not signify the end of the logical line.
- A multi-line (GFM) Markdown comment is a sequence of characters between /# and #/. A multi-line Markdown comment may not be mixed in with other code on the same line.

Multi-line comments may be nested, but are required to be properly nested. Therefore, a comment like /* /* */ or /# /# #/ will be rejected as having an unterminated comment.

For the purpose of debugging, metrics, and tracing, a comment is associated with the subsequent logical line of code, if it is not a blank line and is at the same indentation level.

#### 2.4. Other tokens

Besides NEWLINE, the following categories of tokens exist:

- Identifiers
- Keywords
- Literals
- Operators
- Delimiters

Whitespace characters (other than NEWLINE, discussed earlier) are not tokens, but serve to delimit tokens.

Where ambiguity exists, a token comprises the longest possible string that forms a legal token, when read from left to right.

### 2.5. Character classes

To construct tokens, characters are distinguished according to the following classes (Unicode general category given in parentheses):

- **Whitespace characters**. \u0020
- **Letters**, which include lower case letters (Ll), upper case letters (Lu), titlecase letters (Lt), other letters (Lo), letter numerals (Nl).
- **Digits** ‘0’ | … | ‘9’.
- **Quotes**, which include the single-quote ('), double-quote ("), and back-tick (`)
- **Punctuation**
  - **Parentheses** ‘(’ | ‘)’ | ‘[’ | ‘]’ | ‘{’ | ‘}’.
  - **Delimiter characters** ‘"’ | ‘.’ | ‘,’.
  - **Operator characters**. These consist of all printable ASCII characters (\u0020 - \u007E) that are in none of the sets above, mathematical symbols (Sm) and other symbols (So).
  - **Reserved characters** '@', '?', ':', `'`

### 2.6. Identifiers and Keywords

#### 2.6.1. Identifiers 

Identifiers may be of unlimited length.

Case is significant, but restricted in that identifiers must be in one of the following forms:
- upper camel-case, composed of letters and digits
- lower camel-case, composed of letters and digits
- lower snake-case, composed of letters, digits and underscores
- upper snake-case, composed of letters, digits and underscores
- back-tick enclosed identifiers, composed of letters, digits, operators, commas, periods, and spaces.  Commas, periods, and whitespace is ignored.

Back-ticked identifiers are treated as if they were synonymous with their camel-cased equivalents, where operators are replaced with their english equivalents, i.e.

- `The Horse` is synonymous with TheHorse
- `Horse #1` is synonymous with HorseNumber1
- `One=1` is synonymous with OneIsEqualTo1

Two identifiers may not exist within the same naming scope that differ only by case.

An identifier may not start with a digit or an underscore.

Internal identifiers may start with "@".

#### 2.6.2. Keywords

The following identifiers are used as reserved words, or keywords of the language, and cannot be used as ordinary identifiers. They must be spelled exactly as written here:

- is-a, has-a, 
- true, false
- and, or, xor, not
- null, undefined
- if, else
- import, from, package
- assert
- try, catch, finally, throw
- for, while/until, do, in, scope
- function, coroutine, return, returns
  - static
- reentrant, threadsafe
- class, interface, abstract
- this, args
- extends, implements, reifies
- structure
- composite, component, composer
  - a component has access to its composer via the composer keyword
  - a component declares the type of its composer, placing e.g. interface requirements on it
- private, public, protected, overridable, override
- continue, break, pass
- is, as
- type, alias
- generator, yield
- lazy
- singleton
- constructor
- new, release, claim, give
- superclass
- let, const[ant]
- switch, case
- optional, some, none
- enumeration
- shared
- primitives:
  - bool[ean]
  - exception
  - float32, float64
  - integer, unsigned
  - int8, int16, int32, int64
  - uint8, uint16, uint32, uint64
  - byte, char[acter]
  - bits
   - stdlib bit functions: or, not, and, xor, ffs, ctz, ntz, popcount, shift (https://en.wikipedia.org/wiki/Bitwise_operation)
   - bitwise_or, bitwise_not, bitwise_and, ...
  - time, date, moment, interval, timezone
    - year(s), month(s), day(s), hour(s), minute(s), second(s), millisecond(s), nanosecond(s)
    - utc, now
  - identifier
  - string, filename, uri, url

TODO: lambda, nonlocal, global, with
TODO: new keywords

- public, protected, testing as an interface in the class?
- serialise, deserialize?
- modulo, **, pow
- compose: the ability to create a composite inplace, akin to scala's object/with syntax.
- typescript utility types: https://www.typescriptlang.org/docs/handbook/utility-types.html
- decorators and metaprogramming
- jsx/xml
- collection, array, map, [], iterator, list, set
- partial definitions, and interface merging
- module vs namespace?
- unit: a highly unit testable piece of code
- for...of? iterates over values
- each? each.key, each.value, each.index
- union enums ala typescript?
- ? as optional?
- overloading method args
- varargs
- procedure? functions have no side effects
- parent/owner?
- union, discriminated unions
- mutable, immutable
- list, tuple, collection, array, queue, set, map, hashtable, bag
- transaction, commit, rollback
- using
- lock
- pointer
- heap, stack?
- implicit
- properties, getters, setters
- readonly
- destructor
- test, mock
- async, await, run
- template
- trait, mixin, sealed
- select / match
- actor, select
- channel, send, receive
- db? rpc?
- given - a keyword to declare singletons / context
- thread, fiber - declares an attribute to be thread-local or fiber-local
- privacy
 - sensitive / sensitivity level
 - personal
  
notes:
alias is retained in debugging info
value origin/history may also be retained

### 2.6.3. Reserved Words

The following identifiers are reserved, but are not part of the language:

- goto, label
- method, procedure, 
  - a function declared inside a class is a method
  - a static function declared inside a class is a class method
  - a procedure is a synonym for a function that has no return value, i.e. only having side effects
  - a function declared in a package is a pure function
    - there is no package state, other than singletons
  - a function declared in a function is not automatically a coroutine
    - a coroutine has access to the variables in its creator's scope
- template
- complex64, complex128, real, rational16, rational32, rational64, rational128, number
- unicode, ascii
- mutable, immutable

### 2.7. Literals

There are literals for integer numbers, floating point numbers, characters, booleans, objects, strings.

```
Literal  ::=  integerLiteral
           |  floatingPointLiteral
           |  booleanLiteral
           |  characterLiteral
           |  stringLiteral
           |  objectLiteral
```

#### 2.7.1. Integer Literals

The syntax for defining an integer literal is:

```
integerLiteral  ::=  integerType '(' untypedLiteral ')'
untypedLiteral  ::=  [unarySign] (decimalNumeral | hexNumeral)
unarySign       ::=  '-' | '+'
decimalNumeral  ::=  ‘0’ | nonZeroDigit {digit}
hexNumeral      ::=  ‘0’ (‘x’ | ‘X’) hexDigit {hexDigit}
digit           ::=  ‘0’ | nonZeroDigit
nonZeroDigit    ::=  ‘1’ | … | ‘9’
integerType     ::=  ( 'int' | 'uint' ) ( '8' | '16' | '32' | '64' )
```

e.g.

```
i = int32(0)
j = uint64(0)
k = uint16(29292)
```

#### 2.7.2. Floating Point Literals

The syntax for defining a floating point literal is:

```
floatingPointLiteral  ::=  floatType '(' untypedLiteral ')'
untypedLiteral        ::= [unarySign] digit {digit} ‘.’ digit {digit} [exponentPart]
                        |  digit {digit} exponentPart
                        |  digit {digit} [exponentPart]
unarySign             ::= '-' | '+'
exponentPart          ::=  (‘E’ | ‘e’) [‘+’ | ‘-’] digit {digit}
floatType             ::=  'float' ( '32' | '64' )
```

e.g.

```
i = float32(0.0)
j = float32(3.444E-8)
```

float32 consists of all IEEE 754 32-bit single-precision binary floating point values, whereas float64 consists of all IEEE 754 64-bit double-precision binary floating point values.

Floating point numbers may not be specified without a leading 0. (i.e. ```.23``` is not a valid way of expressing ```0.23```)

**Example:**

```
0.0        1e30f      3.14159f      1.0e-100      -1.3    
```

The phrase 1.toString parses as three different tokens: the integer literal 1, a ., and the identifier toString.

1. is not a valid floating point literal because the mandatory digit after the . is missing.

#### 2.7.3. Boolean Literals

```
booleanLiteral  ::=  ‘true’ | ‘false’
```

The boolean literals true and false are members of type Boolean.

#### 2.7.4. String Literals

A string literal is a sequence of characters in double quotes. The characters can be any Unicode character except the double quote delimiter, \u000A (LF), \u000D (CR), or any Unicode character represented by either a Unicode escape or by an escape sequence.

If the string literal should contain a double quote character, LF or CR, they must be escaped using a backslash (`\`).

The value of a string literal is an instance of class String.

**Example:**

```
"Hello, world!\n"
"\"Hello,\" replied the world."
```

#### 2.7.4.1. Character Literals

A string literal of length 1 is considered a character literal

#### 2.7.4.2. Multi-Line String Literals

```
stringLiteral   ::=  ‘"""’ multiLineChars ‘"""’
multiLineChars  ::=  {[‘"’] [‘"’] charNoDoubleQuote} {‘"’}
```

A multi-line string literal is a sequence of characters enclosed in triple quotes """ ... """. The sequence of characters is arbitrary, except that it may contain three or more consecutive quote characters only at the very end. Characters must not necessarily be printable; newlines or other control characters are also permitted. Unicode escapes work as everywhere else, but none of the escape sequences here are interpreted.

Newlines and leading/trailing margins are folded into a single space character in multi-line string literals.

Multi-line string literals follow the following indentation rules:

1. The first line that contains a multi-line string literal shall end with """ and a NEWLINE
2. The second line shall be INDENTed.
3. The last line shall only contain the terminating """ and be DEDENTed.

**Example:**

```
    foo = """
        The present string
        spans three
        lines.
    """
```

This would produce the string:

```
The present string spans three lines.
```

To actually make the string span multiple lines, embed the "\n" character:

**Example:**

```
    foo = """
        The present string\n
        spans three\n
        lines.
    """
```

This would produce the string:

```
The present string
spans three
lines.
```

To retain the margin, add whitespace after the INDENT.


**Example:**

```
    foo = """
        The present string\n
            spans three\n
                lines.
    """
```

This would produce the string:

```
The present string
    spans three
        lines.
```

#### 2.7.4.3. String Interpolation

String Interpolation allows users to embed variable references directly in processed string literals.
 
This means that the compiler does some additional work to these types of literals. A processed string literal is denoted by a set of characters preceded by an interpolator identifier.

Interpolation variables are specified by enclosing them in curly braces, e.g. "{foo}". If an interpolated string literal should contain a { character, it must be escaped using a backslash (`\`).

YAPL provides a number of interpolation methods: f[ormat], i18n, raw, yaml, json, and xml, but does not allow declaring custom string interpolators.

##### 2.7.4.4. The format String Interpolator

Prefixing format, or f for short, to any string literal allows the usage of variables directly in the string. 

Here’s an example:

```
name = "Jane"
println(f"Hello, {name}")  // Hello, Jane
```

In the above, the literal "Hello, {name}" is a processed string literal.  The format interpolator knows to insert the value of the "name" variable at this location in the string, resulting in the string "Hello, Jane".

With the format interpolator, any variable that is in scope can be used within a string.

The format interpolator does not accept arbitrary expressions, but does accept member variable dereferencing. For example, the following are illegal uses of the format interpolator:

```
println(f"1 + 1 = {1 + 1}") // error: string interpolators do not support arbitrary expressions
```

##### 2.7.4.5. Format Specifiers

The format string interpolator does allow the creation of simple formatted strings, similar to printf in other languages. 
However, YAPL does not support the majority of formatting options found in other languages, to favour readability. YAPL
considers them cryptic, rarely used features, and encourages using string methods instead.

Control characters are not needed to specify the input variable's type, as YAPL string interpolation is type safe.

```
height = 1.7d
name = "Jane"
println(f"{name} is {height:.2} meters tall")  // Jane is 1.70 meters tall
```

| Control Character | Explanation |
| ----------------- | ----------- |
| E | scientific notation, with an uppercase "E" |
| G	| use decimal or scientific notation with an uppercase "E", whichever is shorter |
| o | an octal number |
| x | unsigned hexadecimal, with lowercase letters |

YAPL does not support a field-length specifier, which is typically provided in other languages, nor does it support
padding, zero-fill, using precision for strings, or controlling the case of hexadecimal or scientific output. 

It does however support the precision modifier for numeric types, in the form of a .n where n is a positive integer.

This modifier allows you to specify the number of decimal places desired.
 
##### 2.7.4.6. The raw Interpolator

The raw interpolator, or r for short, is identical to the format interpolator, except it does not support escape codes via `\`.

Example:

```
println(f"a\nb")
// output: 
// a
// b

println(r"a\nb")
// output: a\nb
```

##### 2.7.4.7. The i18n string interpolator

The i18n string interpolator, or i for short, is reserved for internationalisation.

The i18n interpolator is identical to the format interpolator, except the string must start with an i18n identifier name.

At runtime, any string interpolated with i18n will use the current user context's locale to lookup translations.

Attempting to load a translation string that refers to values that are not in the template string will result in an exception.

Attempting to use the i18n interpolator in a context that does not have a user will lead to a compiler error.

```
i18n.locale("ALIEN").translate("FOO", "{name} is an alien")
i18n.locale("ALIEN").translate("BLAT", (user, name)=>{
  const pronoun = user.pronouns.their
  return s"{name} likes {pronoun} coffee"
})
context.user.setLocale("ALIEN")
println(i"FOO: {name} is a person")
println(i"BLAT: {name} likes their coffee")
```

##### 2.7.4.8. The raw-i18n string interpolator

The raw-i18n string interpolator, or ri for short, combines the properties of the raw interpolator and the i18n interpolator.

##### 2.7.4.9. The json Interpolator

The json interpolator, or j for short, is similar to the format interpolator, except that it returns a parsed JSON object.

The json interpolator does not require escaping { characters.

It is a compiler error to pass a string to the json interpolator that is syntactically incorrect.

Interpolated variables are considered tainted, and cannot alter the JSON structure of the template text, except via interpolated json variables.

Example:

```
world = "funky world";
dogs = 3
u = j"""{"name":"Mrs Bar", "address": "Foo Street"}"""
json = j"""{
    "hello" : "{world}",
    "dogs"  : {dogs},
    "user"  : {u}
}"""

println(json.hello);
// output:
// funky world

println(f"{json.user.name} lives at {json.user.address} with {json.dogs} dogs."
```

##### 2.7.4.10. The xml Interpolator

The xml interpolator, or x for short, is similar to the format interpolator, except that it returns a parsed XML object.

It is a compiler error to pass a string to the xml interpolator that is syntactically incorrect.

Interpolated variables are considered tainted, and cannot alter the XML structure of the template text, except via interpolated xml variables.

Example:

```
world = "funky world"
goodbye = x"""<goodbye>bless</goodbye>"""
x = x"""
    <hello>
        {world}
    </hello>
    {goodbye}
"""

println(j.hello);
// output:
// funky world
println(j.goodbye)
// output:
// bless
```

##### 2.7.4.11. The yaml Interpolator

The yaml interpolator, or y for short, is similar to the format interpolator, except that it returns a parsed YAML object.

It is a compiler error to pass a string to the yaml interpolator that is syntactically incorrect.

Interpolated variables are considered tainted, and cannot alter the YAML structure of the template text, except via interpolated yaml variables.

Example:

```
const blat = "bar"
bar = y"""bar: true"""
x = y"""
    foo: "{blat}"
    {bar}
"""

println(x.foo);
// output:
// bar

println(x.bar);
// output:
// true
```

#### 2.7.5. Object Literals

Object literals may be created by specifying the object type, followed by parenthesis and constructor parameters.

e.g.

```
foo = Blat(123,338)

mutable bar = Blat(123,338)
bar := foo
```

### 2.8 Operators

The following tokens are operators:

| Token | Operator |
| ----- | -------- |
| = | immutable assignment |
| := | mutable assignment |
| # | transfer ownership |
| + | add |
| - | subtract |
| * | multiply |
| / | divide |
| += | mutable inplace addition |
| -= | mutable inplace subtraction |
| *= | mutable inplace multiplication |
| /= | mutable inplace division |
| < | less than |
| <= | less than or equal to |
| == | equal to |
| >= | greater than or equal to |
| > | greater than |
| != | not equal to |
| and | logical and |
| or | logical or |
| xor | logical xor |
| not | logical not |

#### 2.8.1. Operator Precedence

##### 2.8.1.1. Mathematical Operator Precedence

Parenthesis have highest priority.
Unary minus has the second highest priority.
Multiplication and division have third highest.
Addition and subtraction have lowest.
Otherwise mathematical expressions are evaluated left-to-right.

YAPL does not provide other mathematical operators directly, but rather supports them through methods on the number types.

##### 2.8.1.2. Logical Operator Precedence

Logical operators are evaluated left to right, using short-circuit evaluation for and/or operators.

YAPL requires the usage of parenthesis to resolve ambiguities that arise due to logical operator precedence. Ambiguous logical expresses result in a compiler error.

For example, the following are legal uses of logical operators:

```
a and b
a and b and c
a or b
a or b or c
a xor b
not a
a and not b
(not a) and b and c
(a and b) or (c and d)
(a or b) and (c or d)
```

The following are however ambiguous and thus illegal uses of logical operators, i.e. compilation errors:

```
not a and b   # error: could mean either "(not a) and b" or "not (a and b)"
a and b or c  # error: could mean either "a and (b or c)" or "(a and b) or c"
a xor b and c # error: could mean either "(a xor b) and c" or "a xor (b and c)"
a xor b xor c # error: could mean either "(a xor b) xor c" or "a xor (b xor c)"
a xor b or c  # error: could mean either "(a xor b) or c" or "a xor (b or c)"
not a xor b   # error: could mean either "not (a xor b)" or "(not a) xor b"
```

##### 2.8.1.3. Precedence between different operator categories

Different operator categories much use parenthesis to determine precedence.

For example, the following YAPL is illegal:

```
if foo and blat and 1<3 {
```

and should be rewritten e.g. as:

```
if foo and blat and (1<3) {
```

##### 2.8.1.4. Bitwise Operators

YAPL does not provide bitwise operators, but rather provides a bits type in its stdlib with all relevant functions.

Bitwise operators are rarely used directly in well written code, and thus the extra verbosity can be encapsulated in helper functions.

e.g. instead of

```
x = y<<7 & 7
```

use a pattern such as

```
function foobar(y: bits):
    shifted = y.lshift(7, bits.ZEROFILL)
    return shifted.and(bits(7))
    
x = foobar(y)
```

##### 2.8.1.5. String Operators

YAPL only provides the string concatenation operators, +, <=, >=, == and !=.  All other string operations are performed through functions.

##### 2.8.1.6. Assignment Operator

YAPL does not allow assignments within expressions, thus they do not require precedence.

##### 2.8.1.7. ?: Operator

YAPL does not provide an inline if-else operator.

### 2.9. Delimiters

The following tokens serve as delimiters in the grammar:

- ( ) [ ] { }
- , : . =

The period can also occur in floating-point literals. A sequence of three periods has a special meaning as an ellipsis literal.
 
The following printing ASCII characters have special meaning as part of other tokens or are otherwise significant to the lexical analyzer:

- " \

The following printing ASCII characters are not used in YAPL. Their occurrence outside string literals and comments is an unconditional error:

- ? :
