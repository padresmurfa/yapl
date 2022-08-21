# Facets

YAPL differs from other languages in that YAPL's classes are organised as a composition of *facets*. A facet can be considered a one-off *trait*, implemented and embedded within a class. In the context of an UML diagram, the class is related to its facets via a relationship of composition.  

## 1. Facets are mandatory

Classes in YAPL may not directly contain member variables or methods. Everything must be segmented into facets.

## Why?

Classes tend to be large and unwieldy, thus good code will often naturally use comments to split a class into logical sections. Taking a closer look at this, doesn't that really look like UML composition? If so, why not just go all the way, and introduce a syntax for it, and get nicer diagrams while you're at it?

## 2. Facet naming

Facets must have valid token names:

- may not start or end with an underscore
- may not contain sequential underscores
- may not start with a digit
- may otherwise only contain lower-case 7-bit alpha-numerals.

For example:

´´´
class hello:

    public facet world:

        ...
´´´

## 2. Facets and namespacing

A method or member variable within a class may not have the same name as a facet. Methods and member variables in different facets within the same class may not have the same name, in spite of the fact that they could have been referenced by a qualified name.

### Why?

If facets had their own namespaces, then cross-facet member and method access would be annoying, destroying the benefits of facets.

## 3. Facet visibility

Facets may be public, private, or protected. The visibility of a facet defines the visibility of all methods and member variables within the facet.

### Why?

This creates a nice syntactic, visual, structure for a class, and it reduces the need for ugly and noisy visibility declarations on every single member and method that is common in programming languages. 

## 4. No sub-facets

A facet may not contain sub-facets.

## Why?

This would only be useful for classes that are way too complicated in the first place. If you want this, you can simulate it by using underscores in facet names.

## 5. References to facets

A facet may be considered a type, using a qualified name including the class name.

´´´
class foo:
    public facet bar:
       method baz:
          ...

-- fubar takes a ´foo´ as a parameter, but only needs access to its ´bar´ facet.
function fubar:
   inputs:
       fb is foo.bar
    code:
        ...

´´´

## Why?

This increases encapsulation and clarity, which is a good thing.
