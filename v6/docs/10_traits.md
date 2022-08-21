# Interfaces

A YAPL module may *declare* traits, which YAPL classes may *extend*.

## 1. Traits

YAPL considers traits to be abstract, partial implementations. They are useful, impure, siblings of interfaces.

´´´
trait world:

    public facet default:

        abstract method say_it:
            ...

        property said_it is boolean:

            getter get_said_it:
                returns:
                    said_it is boolean
                code:
                    return has_already_said_it

    private facet implementation:

        has_already_said_it is boolean


class hello:

    public trait world:

        method say_it:
            code:
                has_already_said_it = true
´´´

## 2. Traits may contain callables

Traits may define and optionally implement callables. A non-implemented callable must be declared 'abstract'

trait world:

    public facet default:

        abstract method say_it:
            ...

        method do_it:
            code:
                ...

        property said_it is boolean:

            abstract getter get_said_it:

´´´
´´´

### Why?

This is one of the key areas where traits differ from interfaces. Maybe they implement a method or property, maybe they require the class that extends them to do so.

## 3. Traits may contain members

Like classes, but unlike interfaces, traits may contain member variables.

### Why?

Traits provide implementations, as opposed to mere declarations.

## 4. Trait naming

Trait must have valid token names:

- may not start or end with an underscore
- may not contain sequential underscores
- may not start with a digit
- may otherwise only contain lower-case 7-bit alpha-numerals.

## 5. Traits and facets

Traits are split into facets, like classes.

### Why?

Traits mix the concepts of implementation and interface. They may thus be equally complex to classes, justifying splitting them into sub-components. Implementation details should generally not be exposed to the extending class however, thus traits need a visibility declaration mechanism. In YAPL that is provided by facets, with the added benefit of splitting constructs into component parts.

## 6. Traits, sub-traits and interfaces

Traits may contain other traits and interfaces, just like classes

## 7. Instantiating traits

Traits are abstract, and thus cannot be instantiated

### Why?

YAPL likes to keep the abstractions clean. If you find yourself in a scenario where you'd like to instantiate a trait, you are free to create a class that contains nothing but that trait and to instantiate that.

## 8. Extending traits

Classes extend traits as if they were facets, using the 'trait' keyword instead of the 'facet' keyword. 

´´´
class foo:

    public trait bar:

       method baz:
          ...
´´´
