# AutobahnObject
A Crossbar worker to create database replicated objects which can be manipulated by CRUD operations

An example of a AutobahnPython worker which can manage an object system.

With a good JavaScript abstraction, you could easily manage complex objects.

For now, you can test and hack the test_object.js (which need the autobahn package, npm install autobahn).
You need to crossbar start before.

* I plan to add disk support (Redis, PostgreSQL, a simple JSON store? I can't decide!)
* I plan to add granular permission support:
	* There is three permission level: object type level, object-level, attribute-level (per single instance of object)
		* You can subscribe / publish on a specific type / object
		* You can edit or read on all or a subset attributes of a specific object or object type.

It would be cool to develop a good abstraction JS with AutobahnJS for this.
I have a lot of CRUD projects which would love to ditch their REST API and use this.

# LICENSE
MIT license, see LICENSE for more information.

