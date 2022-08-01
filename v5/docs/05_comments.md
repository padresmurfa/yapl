# Comments

Maintainable programs require comments, augmenting computer-speak with human-readable explanations. YAPL thus places more emphasize on comments than is typical of programming languages, as described below.

# 1. The comment symbol

YAPL uses -- both for single-line and multi-line comments.

## Why?

Having compared the various comment symbols used by programming languages, the -- symbol seems to provide to most aesthetically pleasing results. Furthermore, this symbol is rarely used by other
languages which makes it ideal to imply that YAPL comments are different than comments found in other languages, which is quite appropriate.

# 2. Formatting comments

Comments should be legal Markdown and should be formatted as such in editors. The YAPL compiler will compile the markdown and emit markdown syntax errors.

Embedded HTML is not supported within YAPL comments.

## Why?

Walls of lackluster green-text are unappealing. We can and should do better than that.

# 3. The horizontal-rule comment

A comment line consisting solely of three or more `-` symobls should be interpreted as a "horizontal rule" by YAPL-aware editors. The horizontal rule should be extended to the right in a fashion that
is consistent between all horizontal rules within the file, at least 79 characters in length and preferably extending at least three characters beyond the leftmost printable character within any line
within the file.

## Why?

It is quite common to see comments with manually inserted horizontal-rules in source code. Done properly, this makes code far more readable and thus maintainable. YAPL was designed to take advantage of this.

# 4. A trailing space

A comment line that is neither a horizontal-rule nor an empty line should start with at least one space. This space is not considered part of the comment itself for formatting purposes. For example:

```
------------------------------
-- ASDF
```

## Why?

Without the leading space, the comment looks ugly and strongly resembles a prefix-decrement operator. This strict definition also allows developers to know exactly how their comments will be interpreted
during transpilation.

# 5. Prefix comments

A prefix-comment may be provided in either multi-line or single-line form, using the -- symbol.
Prefix comments may only be preceeded by whitespace within a line.

Prefix-Comments are associated with the statement in the line that immediately follows

```
-- This is an example of a multi-line prefix-comment that is associated with the following
-- statement; `method foo:`
method foo:
    ...

-- This is an example of a single-line prefix-comment that is also associated with the following statement, `method foo:`
method bar:
    ...
```

## Why?

Since YAPL is a transpiler, as opposed to a compiler or interpreter, comments are injected into appropriate locations in the output code to aid human readability. Languages that have single-line comment
symbols also do not really need a separate multi-line comment, and providing one leads to a mix-mash of less aesthetically pleasing code, which is ultimately detrimental to readability.

# 6. Suffix comments

A suffix-comment may also be provided in single-line form. Suffix-comments likewise use the -- symbol,
but they must be preceeded by non-empty text.

Suffix-Comments are associated with the statement that immediately preceeds the comment.

```
    foo is integer -- this is a suffix-comment that will be associated with the statement `foo is integer`
```

## Why?

Suffix comments are great to add a quick comment to e.g. a variable declaration. As YAPL not only uses suffix comments in lieue of traditional docstring macros, but also mandates their use in common cases,
an elegant syntax was called for.

# 7. Inline comments

An inline-comment is not directly associated with the statements preceeding or succeeding it. Instead, it is associated with a
point in time within the flow of a function or module declaration. An inline-comment must be separated from its immediate *same-level*
surroundings with empty lines.

```
method main:
    code:
        -- this is an inline-comment. it is not at the same level as `code:`, above, thus it does not need to be separated from
        -- that statement by a blank line. It does however need to be separated by a blank line from the subsequent stdout call,
        -- otherwise it would be associated with that line in transpiler output such as debug traces.

        stdout.write_line("Hello World!")

```

## Why?

For all your other commenting needs...

# 8. Docstrings

YAPL does not support the traditional doc-comment syntax found in other programming languages, e.g. for describing arguments and return values.

In their stead, each semantic component such as method arguments and return values are documented directly within yapl via prefix- or suffix- comments.
The transpilation process uses these comments to create docstring comments automatically, formatted in the correct style for the output language.

```
    ----------------------------------------------------------------------------------------------------------------
    -- Move the rabbit to the best possible square, from the current position, for foraging.
    ----------------------------------------------------------------------------------------------------------------
    method move:
        returns:
            moved is boolean -- true if the rabbit moved. false otherwise
        emits:
            rabbit_moved -- if the rabbit moved to another square
        code:
```

## Why?

Docstrings are quite useful, but their use is inconsistent and they are generally an eyesore. YAPL takes a different route, which time will hopefully show is better.

# 9. Don't combine prefix and suffix comments

Combining a prefix comment with a suffix comment is not allowed.

```
    ----------------------------------------------------------------------------------------------------------------
    -- since the move method has a prefix comment ...
    ----------------------------------------------------------------------------------------------------------------
    method move: -- a suffix comment is not allowed
        ...
```

## Why?

Because its ugly and pointless.

# 10. Hyperlinks in comments

Hyperlinks are supported in Markdown, and thus they are also implicitly supported by YAPL. The `yapl:` uri-scheme can additionally be used to create links
with semantics that the YAPL transpiler is aware of. This will be documented in a subsequent chapter, but here are some examples:

* `yapl:com.yapllang.docs.comments/comments/foo` refers to the foo-method of the comments-class in the com.yapllang.docs.comments module.
* `yapl:com.yapllang.docs.comments/uml_class_diagram?automatic.png` refers to an automatically generated UML class-diagram for the com.yapllang.docs.comments module. The editor should preferably support opening the diagram in an embedded interactive mode.

## Why?

Markdown supports hyperlinks. YAPL comments are markdown. The possibilities here just seem endless.