## 3. Naming and Binding

### 3.1. Blocks and Scopes 

A block is a possibly empty sequence of declarations and statements.  

#### 3.1.1. Implicit Scopes

Scopes are generally implicit in YAPL, although the scope statement may also be used to explicitly create a new scope.

1. The global scope encompasses all YAPL source text.
2. Each package has a package scope containing all YAPL source text for that package.
3. Each file has a file scope containing all YAPL source text in that file.
4. Each block has a block scope (e.g. if, else, try, catch, finally, function, method, class, switch statement clauses, ...)

Scopes can be nested.

#### 3.1.2. Scoped Declarations

A declaration binds a non-blank identifier to a constant, type, variable, function, method, class, label, or package. Every identifier in a program must be declared. No identifier may be declared twice in the same scope, and no identifier may be declared in both the file and package scope.

The blank identifier may be used like any other identifier in a declaration, but it does not introduce a binding and thus is not declared.

```
Declaration   = ConstDecl | TypeDecl | VarDecl .
TopLevelDecl  = Declaration | FunctionDecl | MethodDecl .
```

#### 3.1.3. Block Scopes

The scope of a declared identifier is the extent of source text in which the identifier denotes the specified constant, type, variable, function, label, or package.

YAPL is lexically scoped using blocks:

- The scope of a predeclared identifier is the universe block.
- The scope of an identifier denoting a constant, type, variable, or function declared at top level (outside any function) is the package block.
- The scope of the package name of an imported package is the file block of the file containing the import declaration.
- The scope of an identifier denoting a function, function parameter, or result variable is the function body.
- The scope of a constant or variable identifier declared inside a function begins at the end of the ConstSpec or VarSpec (ShortVarDecl for short variable declarations) and ends at the end of the innermost containing block.
- The scope of a type identifier declared inside a function begins at the identifier in the TypeSpec and ends at the end of the innermost containing block.
- An identifier declared in a block may be redeclared in an inner block. While the identifier of the inner declaration is in scope, it denotes the entity declared by the inner declaration.

The package clause is not a declaration; the package name does not appear in any scope. Its purpose is to identify the files belonging to the same package and to specify the default package name for import declarations.

#### 3.1.4. Blank identifier

The blank identifier is represented by the underscore character _. It serves as an anonymous placeholder instead of a regular (non-blank) identifier and has special meaning in declarations, as an operand, and in assignments.

#### 3.1.5. Packages

All files in YAPL must be associated with packages, and all files within a package must be located in a relative directory that ends with the package namespace.

Packages result in separate compilation entities

##### 3.1.5.1. Exporting identifiers from packages

An identifier may be exported to permit access to it from another package. To export a symbol, declare it as public.

```
package com.yaplang.samples.export

public class Foo {
    function Blat() returns string {
        return "Hello World!"
    }
}
```

#### 3.1.5.2. Importing identifiers into packages

Exported identifiers become available in other packages via import statements.

Import statements are package level constructs, in that it is illegal for two separate import statements within the same package to assign the same name binding to two different things. Import is also a file-level construct however in that a token should only be used if it is imported in the file that it is used.

Using a token that is known within the package but not within the current file should generate a compiler warning, as opposed to an error.

```
package com.yaplang.samples.import

import Foo from com.yaplang.samples.export as Foobar
import Foo from com.yaplang.samples.export
import com.yaplang.samples.export

```

#### 3.1.6. Uniqueness of identifiers

Given a set of identifiers, an identifier is called unique if it is different from every other in the set. Two identifiers are different if they are spelled differently, or if they appear in different packages and are not exported. Otherwise, they are the same.

#### 3.1.7. Type definitions

A type may be defined by using the type statement.  Aliases may augment the original type with metadata, such as minimums, maximums, and constants. 

Type defines are considered concrete types.

TODO: this syntax is crap. fix.

```

type UserId = uint32

const UserId.Nobody = 0
const UserId.Everybody = 0xFFFFFFFF
const UserId.Maximum = 100000

assert.eq(UserId.Nobody, 0)
assert.eq(UserId.Everybody, 0xFFFFFFFF)
try {
    UserId(100001)
} catch MaxRangeError(e) {
}

```

#### 3.1.8. Object.this

The 'this' variable is implicitly defined in all object methods. It must be used when omitting it would be ambiguous, and must not be used otherwise.

#### 3.1.9. Function.args

The 'args' variable is implicitly defined in all functions. It must be used to disambiguate references to function arguments when they would otherwise be ambiguous, e.g. because they are identical to class member variable names.

