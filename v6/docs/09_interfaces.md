# Interfaces

A YAPL module may *declare* interfaces, which YAPL classes may *implement*.

## 1. Interfaces

Interfaces are abstract definition that describe a single facet that may be shared by multiple classes. Interfaces do not provide implementations of any callable.

´´´
interface world:

    method say_it:
        ...

    property said_it is boolean:

        get:
            ...

        set:
            ...

class hello:

    public interface world:

        method say_it:
            ...
´´´

## 2. Interfaces contain callables

Interfaces define callables, without their corresponding ´code´ implementation segments.

## 3. Interfaces may not contain member variables

Unlike classes, interfaces do not contain member variables. Member variables are an implementation detail, and thus have no place in interfaces.

## 4. Interface naming

Facets must have valid token names:

- may not start or end with an underscore
- may not contain sequential underscores
- may not start with a digit
- may otherwise only contain lower-case 7-bit alpha-numerals.

## 5. Content visibility

All interface content is mandatorily public.

### Why?

The entire point of interfaces is to define publicly visible callables. 

## 6. Interfaces and facets

Interfaces may not contain facets.

## Why?

If your interface is so complext that it requires facets, you're doing something wrong. Split your interface into multiple interfaces instead.

## 7. Implementing interfaces

Classes implement interfaces as if they were facets, using the 'interface' keyword instead of the 'facet' keyword.

´´´
class foo:

    public interface bar:

       method baz:
          ...
´´´
