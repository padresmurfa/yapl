# Tokens

Tokens in YAPL, be they reserved-words or programmer-defined, are more strictly defined than in most other programming languages.

## 1. use lower_snake_case

All tokens, without exception, and that means including class names and constants, must be specified in lower_snake_case.

### Why?

When working with multiple programming languages, the use of upper-case letters in tokens tends to become quite muddied and thus provides little actual value. lower_snake_case, the naming
convention of choice for almost all things Python, is simply more readable and maintainable. The decision to use UpperCamelCase is specific scenarios within Python furthermore provides
little value and is super-annoying in the case of e.g. True and False.

## 2. Case sensitivity

While YAPL comments may contain the full range of characters defined by the character set, YAPL code only allows lower-case letters in tokens. Thus whether or not
it is case-sensitive is a moot point.

### Why?

Programming languages typically allow all of the following to co-exist, yet refer to different things: Foo, foo, fOO, fOo, and foO. This is just plain wrong.

## 3. Restricted alphabet

Tokens in *standard* YAPL code may only contain the following characters:
* a .. z
* 0 .. 9
* _

Developers using *standard* YAPL should either translate non-english token names to english, or transliterate them to the english alphabet.

### Why?

The lingua-franca of software development is international english. While a case can be made for supporting non-english characters in token names, e.g. class, method, and variable, for the
purpose of using domain-specific language terms within source code, this practice generally only leads to pain and can be sufficiently addressed by transliterating such terms to the english
alphabet. Furthermore, supporting non-english token names while requiring all reserved words to be expressed in english is a weak half-measure.

## 4. Constraints on underscores

Tokens may neither start or end with an underscore. They may furthermore not contain sequences of two or more underscores.

### Why?

During transpilation, an underscore is interpreted as a whitespace-separator, allowing the transpiler to convert tokens to other naming conventions such as UpperCamelCase or UPPER_SNAKE_CASE.
A token or phrase that starts or ends with whitespace doesn't make sense. Furthermore, some programming languages have conventions regarding when to use leading and trailing underscores. As for
the rule on multiple sequential underscores, there is insufficient visual difference between e.g. foo_bar and foo__bar.

## 5. Localized YAPL

Future versions of YAPL may be localized to provide fully-localised editions, akin to how (I believe) Chinese BASIC and Python would or should be implemented.

### Why?

Because YAPL is intended for all programmers, not just those who primarily use the latin alphabet and english as a primary or secondary language.

## 6. Token length

A YAPL token should be no more than 128 characters in length. This is a soft limit.

### Why?

To place a reasonable, albeit arbitrary, constraint on what YAPL tooling should be expected to performantly support.
