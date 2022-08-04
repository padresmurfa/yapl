# Classes

Most code in YAPL is found in methods within classes, which in turn are located within modules.

## 1. Naming

Classes must follow the standard token naming rules. A class name should generally be a word or phrase that would make sense as the topic of a wiki-page.

### Why?

The YAPL transpiler will eventually generate a wiki for your project.

## 2. Class visibility

Classes are public, like all other declarations at module scope. To create the developer-experience of private classes, use sub-modules.

## Why?

See the discussion on module visibilty for details.

## 3. Class module locations

Classes should be located within a module with a path that ends with the class-name.

## 4. Class Statements

A class is declared at module-scope using the `class <class-name>:` statement.

## 5. Class Statement Comments

Class statements must be commented either using a prefix-comment or a suffix-comment, as described in the section on comments.

### Why?

YAPL takes commenting very seriously as part of maintainability.

## 6. Extending classes

A class may inherit from at most once other class, for convenience, using the *extends* keyword.

## Why?

Multiple-interitance has been proven time and time again to be an abomination. The choice of the *extends* keyword is a nod towards UML notation, as YAPL is
designed to be friendly towards diagramming. 

## 7. No embedded classes

Classes may not be embedded within other classes.

### Why?

Embedding classes generally does more harm than good for readability and maintainability. Also, embedded functions are often closures, so shouldn't embedded
classes also be closures? How would that even work? If we figure that out, and see a need for it, then YAPL may eventually provide this ability via a separate
closure_class keyword.

## 8. Instances and class instantiation

YAPL uses the keyword ´instantiate´ to denote the creation of a new instance of a class.

´´´
foo = instantiate bar()
´´´

### Why?

YAPL favours clarity, maintainability and readability over brevity. The ´new´ keyword seems like a linguistic kludge that was introduced for the sake of brevity in the early days of object-oriented programming. Invoking a class name as a function is another popular option, but that obscures the computer-science and IMO
doesn't really help folks that are learning the ropes of their first few programming languages. 

### Why no prototype cloning?

The only popular/mainstream programming language based on prototypes is JavaScript. Even JavaScript developers eventually caved in and admitted that classes are the way to go via adding the *class* keyword to the language.
