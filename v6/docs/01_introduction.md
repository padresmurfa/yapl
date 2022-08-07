# Introduction

YAPL stands for Yet Another Programming Language. So why on earth would we need yet another programming language? We already have so many, and they all pretty much do the same thing.  They provide us with a language that we can use to command machines to do our bidding.

Yet, none of these language can command *all machines* to do our bidding.  The same code snippet will not run natively on Mac, Windows, iOS, Android, in the browser, in the database, in a JVM, in Python, in Node, in an EVM, and in a .NET application. YAPL is intended to do precisely that.

YAPL is a general-purpose language designed with code reusability, readability and maintainability in mind. But unlike most other languages, YAPL is intended first and foremost to *(eventually)* be transpiled into *all other (common) languages*.

## 1. Purpose and benefits of YAPL

YAPL is intended to mitigate a number of issues within software development, described in the following subchapters.

## 1.1. Cross-language coding

Professional software developers must often use multiple programming languages to perform their daily tasks. Furthermore, as software developers switch work environments and programming languages rise and fall in popularity, this
set of languages changes. Each language has its own idiosyncracies, naming conventions, toolchains, editor behaviour and so forth. This places an undue amount of cognitive overload on developers that would be better spent on
implementing and iterating core business logic.

YAPL enables developers to use the same language for all platforms and purposes, thus reducing the cognitive overload.

## 1.2. Reduced code-rot

As an organization's code-base grows over time and their environment changes, older parts of the code tend to sit around and gather dust. Given time, an organization will tend to have to rejuvenate their development team and their
tech stack. This rejuvenation process introduces code-rot in the older code, as the original developers migrate to different projects and companies and the tools used to create the older code become obsolete.

YAPL enables developers to rejuvenate old code by migrating the code to YAPL without changing the execution environment.

## 1.3. Consistently maintainable code

Maintainability is often overlooked and unenforced in code bases. This leads to poorly named modules, classes, functions and variables.  Tooling that leverages and exposes metadata including comments is typically a second-class
citizen in the programming language, leading to less perceived and actual value of the extra effort developers put into maintainability.

YAPL is opinionatedly biased towards maintainability, placing hard constraints on numerous aspects that typically lead to unmaintainable code. For example, all classes, functions and variables must be commented. All tokens must
be provided in lower_snake_case, which will be then transformed into the appropriate naming conventions of the target language. YAPL furthermore emits transpiled docs, diagrams, and integrations for observability tools.

## 1.4. Cross-platform coding

There have been many attempts at cross-platform solutions in the past.

The C/C++ community attempted this through the notion of precompiler macros and standard libraries, so that the code could compile to different target architectures. The Java community
attempted this through the notion that all programmers should use Java, making sure that the JVM would run everywhere, including lackluster incursions into the browser via applets and mobile via J2ME. Python followed suit, but
did not follow suit into the browser or mobile. Microsoft attempted something similar with .NET, which would natively support multiple programming languages. The JVM community one-upped this, introducing independent languages
such as Scala and Koitlin that target the JVM. JavaScript attempted to expand its domain to the server through node.js. The browser community attempted to bring all languages to the web via WebAssembly. Go and Rust attempt to
follow in C's footsteps, through native compilation to server architectures and latching on to the browser community's WebAssembly approach for client-side code.

YAPL provides an alternate approach to cross-platform coding, through transpilation as opposed to compilation. YAPL code is transpiled to languages that in turn run in every execution environment. YAPL can thus be used to
create software that simultaneously targets .NET (through transpilation to C#), the JVM (through transpilation to Java), the Python VM (through transpilation to Python), the browser (through transpilation to JavaScript), or
natively (through transpilation to Rust), and the Erlang VM (through transpilation to Elixir).

## 2. Characteristics of YAPL

YAPL has characteristics targeting pragmatic programming languages. It is structured, and strongly typed, supporting the modular, producural, object-oriented, functional and imperative paradigms. 

## 3. Readability over Brevity

YAPL is not intended to be brief, but rather readable and maintainable.  Some patterns that are avoided due to this include:

* Abbreviations, such as strcpy, def or fun
* inplace assignment operators, such as +=, <<=, -=
* increment/decrement operators, such as ++, --
* non-standard mathematical operators, such as ** and ^
* special bitwise operators, such as <<, >>, | and &

## 4. Explicit over Implicit

YAPL provides explicit keywords for many things that would otherwise be implicit in other environments, such as:

* reentrant, threadsafe, logical xor, coroutine, singleton, composite

## 5. Obvious

Surprising syntax and semantics are avoided in YAPL, such as:

* Scala's for-comprehensions
* C++ operator overloading
* Idiomatic operators such as <<=

## 6. Memory model

YAPL transpiles to languages and environments that are garbage-collected (e.g. Java), use memory-ownership (e.g. Rust), use smart-pointers (e.g. C++), and have manual memory management (e.g. C)

To ensure that all of these target environments can be supported, YAPL syntax relies on ownership tracking.

An object can be owned by a reference on a stack, or by a reference that can be tracked to a singleton, such as a static collection. A reference may also be owned by a shared reference tracker.

## 7. Structural whitespace

YAPL strictly enforces whitespace structural rules, akin to Python's, discussed.

# 8. Explicit Precedence

YAPL avoids implicit precedence rules that may vary between different programming languages. The precedence of basic mathematical operators are however supported (+, -, *, /)

The order of operations must otherwise be made explicit, e.g. through the use of parenthesis.
