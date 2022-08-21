# Callables

YAPL provides six different fundamental forms of callables, which are declared in segments.

## 1. Callable types

The callable types within YAPL are as follows:

### 1.1 Functions

Functions in YAPL may be declared at module scope. They are "pure", unable to access any state that is not explicitly passed in to them. This includes anything that would normally be considered *global variables*.

### 1.2 Closures

A closure is a higher-order function which "pre-fills" certain arguments of a callable. This is called "closing over a variable". Closures are pretty explicit in YAPL, compared to other languages.

´´´
function foo:
    inputs:
        a is integer
        b is integer
    ...

function bar:
    code:
        a = 1234
        foo_bar_over_a = closure foo_bar_over_a closes foo over a
        foo_bar_over_a(b=567)

´´´

#### Why?

Closures are an endless source of misunderstandings, so its best to shed light on them by forcing them out into the open and using explicit terminology.

### 1.3 Generator

Generators use yield semantics rather than return semantics, but are otherwise are identical to functions. Invoking a generator function creates an invocation state which
the generator function closes over.

### 1.4 Constructors

A class constructor is invoked by code that uses the 'instantiate' method. The constructor closes over the 'this' reference, which refers to the state of the newly instantiated instance of the class (aka the 'object').

### 1.5 Methods

A class method closes over the 'this' reference, thus it is not 'pure' like a function.

### 1.6 Property Getters

A property getter,

- property getter
- property setter
- closure
  - A closure "closes over" some other variables, such as 


### Why?

Many languages use as few keywords as possible to represent callables, but this tends to muddy the subtle differences between the various forms.

## 2. Abstract callables

Abstract callables do not contain a 'code' segment. All callables declared in an interface are considered abstract. Traits may specify that specific callables are abstract.

´´´
trait foo:

   abstract method bar:
      ...      
´´´

## 3. Callable Statement Comments

Callable statements must be commented using a prefix-comment, as described in the section on comments.

### Why?

YAPL takes commenting very seriously as part of maintainability.

## 4. Declaration

A callable is declared within a module, class, or property section using a keyword.

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

A property must contain a single getter and may also contain a single setter, both of which are declared according to the standard YAPL callable syntax. No short-cuts are offered.

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
                getter get_said_it:
                    returns:
                        said_it is boolean
                    code:
                        return said_it = has_already_said_it

                ------------------------------------------------------------
                -- updates our state, defining whether or not we have said
                -- "hello world"
                ------------------------------------------------------------
                setter set_said_it:
                    inputs:
                        new_value is boolean
                    code:
                        has_already_said_it = new_value
´´´

### Why?

Property declaration syntax varies between programming languages and is often cryptic, illegible, and unsupportive of maintainable coding practices such as commenting. YAPL places a very strong emphasis on readability, with very little emphasis on conciseness. This is reflected in the syntax for properties. See the section below on naming for further discussions.

## 3. Setters are optional

YAPL allows properties to be declared as read-only by omitting the setter. Getters are mandatory however.

### Why?

Read-only properties is a pretty common thing in real-world code, and this supports encapsulation. Write-only properties is a rarity and thus of no value as a mainstream language feature. Feel free to implement write-only properties using normal methods. 

## 4. Properties, Getters, Setters and naming

Properties must have valid token names. Unlike other programming languages that support properties, YAPL requires getters and setters to have their own names:

- may not start or end with an underscore
- may not contain sequential underscores
- may not start with a digit
- may otherwise only contain lower-case 7-bit alpha-numerals.

For example:

´´´
class hello:
    public facet world:
        property foo is boolean:
            getter get_foo:
                ...
            setter set_foo:
                ...
´´´

### Why?

In YAPL, a getter and a setter are considered synonyms / syntactic sugar for real callables. Callables have names, which tend to show up in debug traces and the like.
While we could have implicitly named the getter and setter, this only serves conciseness (which YAPL does not value) and leads to syntax that is unfriendly towards developers
that are unfamiliar with the language or with programming in general. YAPL furthermore favors the explicit over the implicit.

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

## 4. No backing variables

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
                getter get_said_it:
                    returns:
                        said_it is boolean
                    code:
                        return said_it = has_already_said_it

                ------------------------------------------------------------
                -- updates our state, defining whether or not we have said
                -- "hello world"
                ------------------------------------------------------------
                setter set_said_it:
                    inputs:
                        new_value is boolean
                    code:
                        has_already_said_it = new_value

        private facet state:

            -- backing variable for the 'said_it' property
            has_already_said_it is boolean
´´´

## Why?

This kind of magic is only useful to veteran single-language developers and original code authors seeking conciseness while writing code. YAPL favours multi-lingual developers who are reading other-peoples code.
