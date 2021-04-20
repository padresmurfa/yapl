## YAPL file

A file containing code in the yapl language. YAPL files have types and identifiers. The
identifiers should be specified in reverse domain notation. YAPL files should be located 
in folders that are consistently named for these identifiers.

### YAPL file layout

YAPL files start with:
* an optional hashbang directive, e.g.
  ```
  #!/usr/bin/yapl
  ```
* a mandatory comment section, describing the file, preceded and succeded by a comment
  section marker, e.g. 
  ```
  ----------------------
  this is a yapl file
  ----------------------
  ```
* a type and identifier declaration, e.g.
  ```
  module foo
  ```
* one or more _sections_, composed of a section header, a section header marker, and indented
  content according to YAPLs whitespace indentation rules, e.g.
  ```
  this is a section
  ======================
  
      -- this is indented section content
  ```
  
### Project

A YAPL project file declares the top level id of the project, as well as what it's top level
artifacts are (e.g. libraries or executables). The project is described in a .project.yapl file.


### Packages

A YAPL package is a folder containing a package yapl file, named .package.yapl. Packages have
a _type_, where currently defined types are: _library_ and _executable_. The future may hold
other types in store, e.g. dynamically linked libraries, runnable docker containers,
host-able web services, etc.

* The package yapl file contains:
  * The package type and identifier, e.g.
  ```
  library foo.bar
  ```
  * a _modules_ section, which enumerates the modules that the package contains, e.g.
  ```
  modules
  ======================
  
      foo, bar
  ```
  * an optional _packages_ section, which enumerates any sub-packages that this package contains, e.g.
  ```
  packages
  ======================

        foobar
  ```
  * an optional _dependencies_ section, which enumerates any external dependencies, e.g.
  ```
  packages
  ======================

        foo.bar
  ```
 
### Modules

A module is considered an independent unit of compilation and initialization.

* A module yapl file contains:
  * The module type and id.
  * an optional _imports_ section
  ```
  imports
  ======================

        from foo
            import bar
  ```
  * an _exports_ section (not optional, as a module with no exports has no purpose)
  ```
  exports
  ======================

        foo, bar
  ```
  * a _contains_ section, that contains the source code of the module, e.g.
  ```
  contains
  ======================

        function foo
            accepts
                bar:string
            body
                not implemented
  ```

### Unit Test Suites

A unit test suite is a sibling to a module, which resides in a file named <module_name>_test.yapl.

The relationship between unit test suites and their modules is a special one, and the syntax of
test suite yapl files is tailored to the needs of unit testing.

The YAPL transpiler expects each function/method to be unit tested. There should be at least
one test per potential branch (including exceptions) per function/method. The YAPL transpiler
shall provide a mechanism to identify which branches are missing test coverage. It is up to
the CI/CD system however to determine whether it will allow uncovered code to pass.

* A unit test suite yapl file contains
  * A reference to the module that is the system under test, e.g.
  ```
  unit test suite for rabbit
  ```
  * A section for each function/method under test, in indented form, e.g.
  ```
  unit tests for rabbit:Rabbit > public instance methods > forage
  ======================================================================================================================
  ```
    * each of which in turn contain one or more test scenarios, e.g.:
    ```
        ----------------------------------------------------------------------------------------------------------------
        there is nothing to eat, and nowhere to go
        ----------------------------------------------------------------------------------------------------------------
        scenario
            given
                rabbit.eat_carrots().eaten = 0
                rabbit.move().moved = false
            when
                eaten = rabbit.forage()
            then
                eaten == 0
    ```
    * unit tests may not perform blocking calls of any sort, including file operations
      and socket operations
  * There may be optional sections for other forms of tests, such as _integration tests_
    and _contract tests_.
    

