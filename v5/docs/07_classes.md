# Classes

Most code in YAPL is found in methods within classes, which in turn are located within modules.

## 1. Naming

Classes must follow the standard token naming rules. A class name should generally be a word or phrase that would make sense as the topic of a wiki-page.

### Why?

The YAPL transpiler will eventually generate a wiki for your project.

## 2. Class visibility

Classes are private by default, like all other module-dwelling declarations, but may be explicitly declared as public.

## 3. Class module locations

Public usable classes should be located within a module with a path that ends with the class-name. Private classes may be located anywhere within a module.

## 4. Class Statements

A class is declared at module-scope using the `class <class-name>:` statement. A public class is declared via `public class <class-name>:`.

## 5. Class Statement Comments

Class statements must be commented either using a prefix-comment or a suffix-comment, as described in the section on comments.

### Why?

YAPL takes commenting very seriously as part of maintainability.

## 6. No embedded classes

Classes may not be embedded within other classes.

### Why?

Embedding classes generally does more harm than good for readability and maintainability. Also, embedded functions are often closures, so shouldn't embedded
classes also be closures? How would that even work? If we figure that out, and see a need for it, then YAPL may eventually provide this ability via a separate
closure_class keyword.