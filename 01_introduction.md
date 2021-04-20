## 1. Introduction

YAPL is a general-purpose language design with code reusability, readability and maintainability in mind.

It is strongly typed, object-oriented, functional and memory-ownership / garbage-collected.

YAPL is intended first and foremost to be transpiled into other languages, but may also be compiled or interpreted directly.

The grammar is explicit and regular, allowing for easy analysis by automatic tools such as integrated development environments.

## 1.1. Readability over Brevity

YAPL is not intended to be brief, it is intended to be readable.  Some patterns that are avoided:

* Abbreviations, such as strcpy, def or fun
* inplace assignment operators, such as +=, <<=, -=
* increment/decrement operators, such as ++, --
* non-standard mathematical operators, such as ** and ^
* special bitwise operators, such as << and >>

## 1.2. Explicit over Implicit

YAPL provides explicit keywords for many things that would otherwise be implicit in other environments.

* reentrant, threadsafe, logical xor, coroutine, singleton, composite, 

## 1.3. Obvious

Surprising syntax and semantics are avoided in YAPL, such as:

* Scala's for-comprehensions
* C++ operator overloading
* Complex operators such as <<=

## 1.4. Memory management

YAPL transpiles to languages and environments that are garbage-collected (e.g. Java), use memory-ownership (e.g. Rust), use smart-pointers (e.g. C++), and have manual memory management (e.g. C)

To ensure that all of these target environments can be supported, YAPL syntax relies on ownership tracking.

An object can be owned by a reference on a stack, or by a reference that can be tracked to a singleton, such as a static collection. A reference may also be owned by a shared reference tracker.

## 1.5. Strict whitespace

YAPL strictly enforces whitespace rules, including INDENT/DEDENT rules akin to Python's, even though YAPL does not use whitespace alone for program structure.

# 1.6. Explicit Precedence

YAPL avoids implicit precedence rules that may vary between different programming languages. The precedence of basic mathematical operators are however supported (+, -, *, /)

The order of operations must otherwise be made explicit, e.g. through the use of parenthesis.

