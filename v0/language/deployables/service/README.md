YAPL can be used to create deployable services. A service is hosted in a *server process*, which may allow access to it
via a variety of means such as grpc, web-api or SOAP.

A YAPL program must include a file that declares a `service { }` to be deployable in this fashion. 

Every public function declared in a *service* will be exposed as an endpoint.
