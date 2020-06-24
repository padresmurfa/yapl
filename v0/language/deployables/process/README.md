YAPL can be used to create deployable processes. A process is a deployable that may be executed directly from a 
terminal, and is one of the oldest building blocks of software.

A YAPL program must include a file that declares a `process { }` to be deployable in this fashion. 

A process may return an *integer status code* and has access to *stdout, stdin, and stderr*, assuming that the OS has
attached these streams.

The entry point of a process is always a function named **main**, for historical reasons.
