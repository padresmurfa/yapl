# Class Properties

YAPL supports the concept of properties, found in many object-oriented languages, albeit with it's own twist.

Properties, along with their getters and setters, are provided by YAPL to encapsulate and clearly project a programming concept. They are not intended as a tool for conciseness, brevity, or as syntactic sugar.

## 1. Declaration

A property is declared within a class-facet using the ´property´ statement, which declares the property name, type, and semantic comment.

´´´
    class hello_world:

        public facet properties:

            ----------------------------------------------------------------
            -- whether or not this instance of hello_world has already
            -- spoken
            ----------------------------------------------------------------
            property said_it is boolean:
                ...
´´´

### Why?

A property declaration is intended to be quite similar to a member variable declaration

## 2. Getters and Setters

A property must contain a single getter and may also contain a single setter, both of which are declared according to the standard YAPL callable syntax, although the name of the getter and setter is implied.

´´´
    class hello_world:

        public facet properties:

            ----------------------------------------------------------------
            -- whether or not this instance of hello_world has already
            -- spoken
            ----------------------------------------------------------------
            property said_it is boolean:

                ------------------------------------------------------------
                -- returns true, if we have said "hello world", else false
                ------------------------------------------------------------
                getter:
                    returns:
                        said_it is boolean
                    code:
                        return said_it = has_already_said_it

                ------------------------------------------------------------
                -- updates our state, defining whether or not we have said
                -- "hello world"
                ------------------------------------------------------------
                setter:
                    inputs:
                        new_value is boolean
                    code:
                        has_already_said_it = new_value
´´´

### Why?

Property declaration syntax varies between programming languages and is often cryptic, illegible, and unsupportive of maintainable coding practices such as commenting. YAPL places a very strong emphasis on readability, with very little emphasis on conciseness. This is reflected in the syntax for properties.

## 3. Setters are optional

YAPL allows properties to be declared as read-only by omitting the setter. Getters are mandatory however.

### Why?

Read-only properties is a pretty common thing in real-world code, and this supports encapsulation. Write-only properties is a rarity and thus of no value as a mainstream language feature. Feel free to implement write-only properties using normal methods. 

## 4. Properties and naming

Properties must have valid token names:

- may not start or end with an underscore
- may not contain sequential underscores
- may not start with a digit
- may otherwise only contain lower-case 7-bit alpha-numerals.

For example:

´´´
class hello:
    public facet world:
        property foo is boolean:
            ...
´´´

## 5. Lack of magical "value"

Languages with separate property declaration syntaxes often have a ´value´ variable syntax in the setter. YAPL does not follow this approach, rather requiring the input value parameter to be declared as in any other callable.

´´´
    setter set_said_it:
        inputs:
            new_value is boolean
        code:
            has_already_said_it = new_value
´´´

### Why?

The traditional approach is cryptic, implicit, and hostile towards folks that are learning the language.

## 6. No backing variables

YAPL does not provide "backing variables" automatically for properties via syntactic sugar. Declare the backing variables manually instead.

´´´
    class hello_world:

        public facet properties:

            ----------------------------------------------------------------
            -- whether or not this instance of hello_world has already
            -- spoken
            ----------------------------------------------------------------
            property said_it is boolean:

                ------------------------------------------------------------
                -- returns true, if we have said "hello world", else false
                ------------------------------------------------------------
                getter:
                    returns:
                        said_it is boolean
                    code:
                        return said_it = has_already_said_it

                ------------------------------------------------------------
                -- updates our state, defining whether or not we have said
                -- "hello world"
                ------------------------------------------------------------
                setter:
                    inputs:
                        new_value is boolean
                    code:
                        has_already_said_it = new_value

        private facet state:

            -- backing variable for the 'said_it' property
            has_already_said_it is boolean
´´´

### Why?

This kind of magic is only useful to veteran single-language developers and original code authors seeking conciseness while writing code. YAPL favours multi-lingual developers who are reading other-peoples code.

## 7. Using getters and setters

YAPL does not allow getters and setters to be used as if they were member variables, requiring instead the more typical call syntax.

´´´
class hello:
    public facet world:
        property said_it is boolean:
           getter:
              ...
           setter:
              ...

function say_it:
    inputs:
        sayer references hello
    code:
        if not sayer.said_it.get():
           console.print_line("hello world!)
           sayer.said_it.set(true)

´´´

### Why?

Explicit over implicit. Traditional property access syntax is ambiguous, surprising, and idiosyncratic. When you access a YAPL property, it is clear whether you are invoking the getter or setter, acquiring a reference to the getter or setter, and that a function invocation is involved that could have side-effects or failure modes that are more complicated than those of member variable access.

## 8. Property Statement Comments

Property statements must be commented using a prefix-comment, as described in the section on comments.

### Why?

YAPL takes commenting very seriously as part of maintainability.
