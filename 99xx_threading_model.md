sidenote:
==========
We should have support for multihoming directories and symlinks

sidenote:
==========
closures vs lambdas: https://stackoverflow.com/questions/220658/what-is-the-difference-between-a-closure-and-a-lambda

// a closure is a function that closes over some variables in it's parent's scope
// a lambda is a closure that closes over the parameters passed to it during creation. In most languages, lambdas are
//   nameless, but YAPL requires them to have names for readability / debuggability. They are useful, e.g. when creating
//   callbacks or launching workers
// a method is a term that we should avoid
// a procedure is a term that we should avoid, but is a function with no return value.
// methods are always closures, in that they always import the "this" pointer from the object they are a part of.

coroutines vs workers vs async methods:
======================
NOTE - YOU PROBABLY DON'T WANT LAMBDAS TO CLOSE OVER THINGS WITHOUT DECLARING IT, LIKEWISE COROUTINES.

// a worker is bound to a context, such as a session, global, service, request, etc. If the context is disowned, then
// all workers bound to the context are terminated. You can query a context for what workers it has running.
// You start a worker by invoking a factory method on the context. e.g. request.worker(lambda doStuff(x) { ... })
// A worker can be called with a lambda or a function, but not a closure or method.
// A worker cannot return a value.
 
// A coroutine is a form of asynchronous method. It closes over it's parameters, taking ownership of them, but releases
//   ownership to it's caller after it has been waited upon. A coroutine has two stacktraces associated with it; the
//   stacktrace where it was started, and the stacktrace where it is awaited. If an exception occurs in a coroutine,
//   it will be thrown from the await function. It is illegal to return a coroutine from a function without awaiting
//   it.
// A coroutine that is called from within a method also closes over the this pointer.
// A coroutine can return a value, but does not 


=========
performance engineering:
it might be cool to be able to attribute a function (class of functions) with a performance attribute, such as claiming
that a request will take no more than 1ms on the average, and 10ms at most. This could be specified in some sort of
contract (or SLA). Metrics, logs and alarms could then automatically be emitted for SLA violations.

==========
layers:
a layer is a vertical grouping of software. A component is a horizontal one, within a layer. If you organize your code
in layers and components, then you could visualize it better. Layers and components are architectural constructs.
Components contain modules. They may declare the relationship between them perhaps. Architecture is heirarchial, thus
a layer A containing component B, can be further viewed as component B containing layer C, which in turn contains
component D, etc. This is a static model, and is not reentrant.

==========

Async is a first-class citizen of YAPL. Any function can be called in a synchronous or asynchronous fashion.

promise = async foo.doSomething()
promise = foo..doSomething()
promise = foo...doSomething()
promise = foo->doSomething()

promise = foo.doSomething@()
promise = foo->doSomething()
promise = foo->doSomething()

result = await promise

function doSomething() {
}

async function doSomething@() {
    promise = Promise()
    Fiber.run(doSomething, promise)
    return promise
}



no, you cannot chain things together in a single line like this. it leads to error handling anti-patterns:
foo.doSomething@() | promise => blat.doSomething@(promise) | promise => barf.doSomething@(promise)


..

If there is a reason to allow this, then a function could be declared exclusively synchronous like this:

sync function doSomething() {
}

foo.~doSomething() // syntax error: explicitly synchronous functions cannot be called asynchronously

...

Likewise, if you want a function to exclusively be called in an asynchronous fashion:

async function doSomething() {
}

foo.doSomething() // syntax error: explicitly asynchronous functions cannot be called synchronously

....

