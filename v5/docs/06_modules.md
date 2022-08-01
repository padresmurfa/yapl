# Modules

All code in YAPL is found in named modules, which in turn are located in files.

## 1. Naming

Modules must be named according to the following rules:

* must include a path, using reverse-DNS notation to describe a dot-separated path of path components
* path components must be valid tokens (as per the separate chapter on tokens)
* paths must
  * contain at least two dots, e.g. `org.yapllang.bla`
  * represent a DNS domain that the code author is affiliated with in some fashion
  * not contain two sequential dots
  * neither start, or end, with a dot
  * be longer than 255 characters
* paths should
  * use transliteration or character omission to turn actual domain names into valid module names, e.g. `foo-bar.com => com.foo_bar or com.foobar` 

### Why?

Programming languages often have a pretty dodgy relationship between file-names and namespaces. We'll have none of that. Java's reverse-DNS name approach was the right way to go.

## 2. Reserved words

Module names may contain what would generally be considered reserved words, e.g. `org.yapllang.new.string`.

### Why?

Because lists of reserved words contain all the good stuff, and YAPL is transpiled into multiple target languages with different lists of reserved words. Also, module names are only used in
using clauses in YAPL, which are always fully-qualified.

## 3. Module file locations

Modules must be contained in files that are located appropriately, in accordance with their module names, as described in the section on files.

## 4. Module Statements

A module is declared at file-scope using the `module <module-name>:` statement.

## 5. Sub-modules

Sub-modules should be declared in their own files.

### Why?

Shorter files are better for tools, such as the transpiler.

## 6. Module Statement Comments

Module statements may be commented either using a prefix-comment or a suffix-comment, as described in the section on comments.

## 7. Module contents

Modules can contain declarations for classes, singletons, functions, constants and types. They may not contain variables.

## Why?

Ad-hoc initialisation code in module scope is shoddy craftmanship that leads to unreadable, untestable, and unmaintainable code. Thus YAPL only allows singletons to exist as concrete values at module scope, in addition to declarations.

## 8. Visibility of module-scoped items

The purpose of modules is to group and publicize classes, functions, constants and types. Module-scoped items are thus always public, and developers are
encouraged to use sub-modules for private internals, or to use packages to place restrictions on access to internals.  

## Why?

Having given the matter some thought, it seems like the ability to fine-tuned visibility of module-scoped items is in fact an act of over-generalization and over-engineering. Less is more in this case.
 