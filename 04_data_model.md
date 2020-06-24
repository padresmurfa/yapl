## 4. Data model

### 4.1. Objects, values and types

Objects are YAPLs abstraction for data. All data in a YAPL program is represented by objects or by relations between objects. Every object has an identity, a type, an owner & scope, and a value. 

#### 4.1.1. Object Identity

An object’s identity never changes once it has been created; you may think of it as the object’s address in memory.

The 'Identity.equal' method compares the identity of two objects. The 'Identity.of' method returns the identity of an object.

#### 4.1.2. Object Type

An object's type determines the operations that the object supports, and also defines the possible values for objects of that type.

The 'Type.of' method returns the type of an object. Like its identity, an object’s type is also immutable.

An object's type is determined by a type operator:

```
foo = int(0)

blat = MyObject(333)
```

#### 4.1.3. Object Ownership, Lifetime and Scope

a reference can be:
- transient vs resilient
- shared vs unshared
- movable vs nonmovable
- perhaps bound to a thread/fiber?
- locked vs unlocked

an object can be:
- managed vs unmanaged
- synchronised vs unsynchronised
- reentrant vs nonreentrant?

a synchronised object:
- should not contain other synchronised objects, that do not use the same synchronisation barrier
- should not give out references to its internals

Each object has one and only one owner. Object lifetime is dictated by the scope of it's owner.

The object owner is a reference, which may in turn be owned by an object. It is always possible to trace the ownership of an object to one of the following:

- a stack frame, attached to a fiber or a thread
- a message (e.g. rpc request or actor message)
- a managed object, such as a session, actor or system resource.
  - a managed object must be associated with a manager, such as a global collection
  - xcxc: a managed object should be accessed within a using block. this allows adding debug/tracing info, ensuring that the object is not prematurely released
- a process, i.e. a global or class variable
  - this is in fact a stack frame of the main thread.

Object ownership must be explicitly transferred between references, using the move ($) prefix-operator.
 
An object is released when it's owner's scope is terminated. The memory of a released object may be henceforth not be accessed, and may be reclaimed immediately or in a delayed fashion by the runtime environment.

When an object is no longer owned, it's disowned() {} method will be called. It is the effective destructor of the object, and can be used e.g. to release system resources.

e.g.

```
foo = Foo("blat") // foo owns Foo("blat")

blat = foo // foo still owns Foo("blat")

function bar(y = Foo) { // bar does not own y
 l = y // l does not own y
}

bar(blat) // foo still owns Foo("blat")

new_owner = $foo // new_owner now owns foo

TODO: objects are created on the stack by default. how does this transfer.

foo = shared Foo("blat") // foo resides in the garbage collector. may not have a destructor.

```

#### 4.1.3.1 Garbage Collection

An object's ownership may be transferred to a garbage collector, such as the global process garbage collector. An object that has been assigned to the garbage collector is never explicitly destroyed, but will eventually garbage-collected after it becomes unreachable.

#### 4.1.4. Object Constructors

The default constructor will assign default values to all member variables of the instance. It is executed prior to executing a custom constructor. Each class may only have one constructor.

e.g.

```
class Foo {
    constructor(i = int) {
    }
}
```

#### 4.1.5. Object Destructors

An object that has a destructor may not be owned directly or indirectly by the garbage collector. When the owner of such an object goes out of scope or otherwise expires, the object will be released and its destructor invoked.

Objects with destructors are convenient e.g. to hold references to external resources, such as open files and sockets. Such an object should typically be split into two parts, such as File and OpenFile, where File holds metadata but does not hold onto system resources (i.e. an open file handle).

Objects that hold references to external resources should also provide an explicit way to release the external resource, such as a close() method. The destructor should free these resources whether or not they have previously been explicitly released.

Exceptions do not propagate out of destructors, but they do get reported to global exception handlers.

e.g.

```
class Bar {
    destructor() {
    }
}
```

#### 4.1.5. Object Value

The value of mutable objects can be changed, while the value of immutable objects may not.

##### 4.1.5.1. Uninitialized values

Values may be declared as uninitialized (aka undefined), but must be initialized before they could be read for the first time. An uninitialized variable is constructed by assigning the type of the value to the variable directly.

```
foo = string

if (bar) {
  foo = "bar"
} else {
  foo = "blat"
}

print(foo)

```

##### 4.1.5.2. Mutable Objects and References

Objects whose value can change are said to be mutable. A mutable object must be stored in a mutable reference, and is introduced by using the mutable assignment operator, e.g.

```
foo := int(0)
```

###### 4.1.5.2.1. Mutable Objects and Concurrency

Mutable objects are only accessible in the most restrictive execution context (i.e. thread/fiber/actor) that declared them. This is enforced at compile time.

##### 4.1.5.3. Immutable Objects contained in Immutable References

Objects whose value cannot change after construction are said to be immutable. Immutable objects may be accessed from any thread, fiber or actor that has visibility of them according to naming/binding/scope rules.

An immutable reference cannot be changed. e.g.

```
class ImmutableStuff {

    name = string

    constructor(name = string) {
        this.name = args.name // when a member name and a param name are identical, the member name must be clarified with 'this' and the param name must be clarified with 'args'
    }
}

foo = ImmutableStuff("asdf")
foo = ImmutableStuff("fdsad") // error: this can't be done

```

#### 4.1.5.4. Containers

Some objects contain references to other objects; these are called containers. Examples of containers are sequences, queues, packed arrays, associative arrays (maps), and sets.


##### 4.1.5.4.1. Mutable Objects contained in Immutable References

Container classes are often mutable by their very nature. While they may be assigned to an immutable reference, their contents may still change afterwards.

Mutable object types are declared by prefixing their class declaration with the 'mutable' keyword. E.g.

```
mutable class MutableMap {
    function clear() {
    }
}
foo = MutableMap()
foo.clear()
```

It is recommended that mutable classes be denoted as such via naming convention.

#### 4.1.5.4.2. ReadOnly References to Mutable Containers

Container classes provide a read-only interface, which can e.g. be passed to sub functions. This is not the same as immutability, as the container could be changed externally to the recipient of such a reference.

