# Memory Management

YAPL is intended for readable, maintainable, robust software development. Manual memory management is none of that. Thus YAPL favours a traditional garbage-collected model, using heap allocations.

## 1. Inferred stack allocation

YAPL reserves the right to infer during transpilation that an instance's lifetime is short enough that it be placed on the stack instead of the heap.

## Why?

The garbage-collection folks are right. Memory management really shouldn't be left in the hands of developers. Where that stuff matters, use C, C++, or Rust.

## 2. Requesting stack allocation

To request that an object be allocated on the stack, use 'stack.instantiate´ instead of ínstantiate. YAPL may still allocate the object on the heap,
depending on the capabilities of the transpilation target. However it will reserve the right to assert that the object's lifetime expire when the
variable leaves scope. 

´´´
foo = stack.instantiate bar()
´´´

## Why?

Since we're going to let the transpiler put things on the stack at its own leisure, we might as well allow the developer to ask for the same. But ignoring the developer's request in this case doesn't really have a serious drawback. This also allows us to leave the door open for more advanced and interesting techniques,
such as arena based memory allocation, thread local allocations and fiber local allocations.

## 3. Mutable by default

References in YAPL are mutable by default, although they may be declared to be immutable.

´´´
bar = instantiate baz()
bar.change() -- this is fine
foo = immutable bar
foo.change()  -- this will generate a compile-time-error
´´´

## Why?

The ability to use 'immutable' semantics is great and all that, but this stuff is mostly only important in high-performance code. YAPL is intended however for maintainable, readable code, and the concept of mutability leaks through a code-base like async keywords. There is a classic tale regarding that, involving the metaphor of code-color, which proves philosophically that the concept sucks for readability, writability, and maintainability. 

## 4. Pass-by-reference or pass-by-value

YAPL will infer whether a value should be passed-by-reference or passed-by-value based on performance and whether or not the callee attempts to mutate the object.

