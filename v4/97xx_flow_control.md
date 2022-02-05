97xx_flow_control.md


1. if-then-else

	if asdf:
	   foo
	else:
	   ignore


2. compare-a-to-b

compare a to be:
   a < b:
       foo
   a > b:
       bar
   a == b:
       meh

3. decisions

   d = decision:
         Hello: a > b
         GoodBye: a < b
         Arg: a == b and c == false
         Meh: a == b

	switch d:
	   Hello: 
	      foo
	   GoodBye:
	      bar
	   Meh, Arg:
	      foobar

.....


exception handling:

do we allow exceptions at all? meh, na... that only leads to errors.

how about the rust model, you must handle all errors. There is also a using block for classes with destructors. Such classes can new be allocated on the heap. Abstract differently (e.g. File vs OpenFile)

......

security reviews, code reviews, and mentors

can't publish a package that isn't code reviewed. If it has a large enough audience, then it needs security review. Can't use open source without paying?!?!?

code reviews should be associated with the reviewer, which is rated and ranked. E.g. only a ranked security reviewer can provide a security review.


.......


shadowing:

shadowing is a bad thing. Thus if you really want to do this, use the shadow keyword:


a = 3
if a > 2:
   shadow a
   a = 3

....


capabilities

yapl has no globals. it has context and capabilities and sandboxes.

.....


return:

a local function should not be able to use return. extract the function to a more global location first.

