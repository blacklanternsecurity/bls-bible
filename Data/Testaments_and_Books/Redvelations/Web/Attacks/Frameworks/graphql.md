<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# GraphQL
### References
* <details><summary>References (Click to expand)</summary><p>
	* [https://github.com/carlospolop/hacktricks/blob/master/pentesting/pentesting-web/graphql.md](https://github.com/carlospolop/hacktricks/blob/master/pentesting/pentesting-web/graphql.md)
	* [https://jondow.eu/practical-graphql-attack-vectors/](https://jondow.eu/practical-graphql-attack-vectors/)
	* [https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696)
	* [https://medium.com/@apkash8/graphql-vs-rest-api-model-common-security-test-cases-for-graphql-endpoints-5b723b1468b4](https://medium.com/@apkash8/graphql-vs-rest-api-model-common-security-test-cases-for-graphql-endpoints-5b723b1468b4)
	* [http://ghostlulz.com/api-hacking-graphql/](http://ghostlulz.com/api-hacking-graphql/)
	* [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/GraphQL%20Injection/README.md)
	* [https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696)
	* Video explaining AutoGraphQL -<br />[https://www.youtube.com/watch?v=JJmufWfVvyU](https://www.youtube.com/watch?v=JJmufWfVvyU)

### Tools
* <details><summary>Tools (Click to expand)</summary><p>
	* Clients
		* [https://github.com/graphql/graphiql](https://github.com/graphql/graphiql)
		* [https://github.com/swisskyrepo/GraphQLmap](https://github.com/swisskyrepo/GraphQLmap)
		* [https://altair.sirmuel.design/](https://altair.sirmuel.design/)
		* [https://blog.doyensec.com/2020/03/26/graphql-scanner.html](https://blog.doyensec.com/2020/03/26/graphql-scanner.html)
		* [https://github.com/doyensec/inql](https://github.com/doyensec/inql)
		* [https://altair.sirmuel.design/](https://altair.sirmuel.design/)
		* [https://gitlab.com/dee-see/graphql-path-enum](https://gitlab.com/dee-see/graphql-path-enum)
	* Automatic Tests
		* [https://graphql-dashboard.herokuapp.com/](https://graphql-dashboard.herokuapp.com/)

### Overview
* <details><summary>Overview (Click to expand)</summary><p>
	* GraphQL is a data query language developed by Facebook and was released in 2015. GraphQL acts as an alternative to REST API. Rest APIs require the client to send multiple requests to different endpoints on the API to query data from the backend database. With graphQL you only need to send one request to query the backend. This is a lot simpler because you don’t have to send multiple requests to the API, a single request can be used to gather all the necessary information.
	* As new technologies emerge so will new vulnerabilities. By **default** graphQL does **not** implement **authentication**, this is put on the developer to implement. This means by default graphQL allows anyone to query it, any sensitive information will be available to attackers unauthenticated.
	* When performing your directory brute force attacks make sure to add the following paths to check for graphQL instances.
		* `_/graphql_`
		* `_/graphiql_`
		* `_/graphql.php_`
		* `_/graphql/console_`
	* Once you find an open graphQL instance you need to know what queries it supports. This can be done by using the introspection system, more details can be found here: [Website](https://graphql.org/learn/introspection/)

### Process
* <details><summary>Basic Enumeration (Click to expand)</summary><p>
	* Graphql usually supports GET, POST (x-www-form-urlencoded) and POST(json).
	* `query={\__schema{types{name,fields{name}}}}`
		* With this query you will find the name of all the types being used:
		* ![](<../../.gitbook/assets/image (202).png>)
	* `query={\__schema{types{name,fields{name, args{name,description,type{name, kind, ofType{name, kind}}}}}}}`
		* With this query you can extract all the types, it's fields, and it's arguments (and the type of the args). This will be very useful to know how to query the database.
		* ![](<../../.gitbook/assets/image (207).png>)
	* Errors
		* It's interesting to know if the **errors** are going to be **shown** as they will contribute with useful **information.**

					?query={__schema}
					?query={}
					?query={thisdefinitelydoesnotexist}
			* ![](<../../.gitbook/assets/image (205).png>)
	* Enumerate Database Schema via Introspection

			/?query=fragment%20FullType%20on%20Type%20{+%20%20kind+%20%20name+%20%20description+%20%20fields%20{+%20%20%20%20name+%20%20%20%20description+%20%20%20%20args%20{+%20%20%20%20%20%20...InputValue+%20%20%20%20}+%20%20%20%20type%20{+%20%20%20%20%20%20...TypeRef+%20%20%20%20}+%20%20}+%20%20inputFields%20{+%20%20%20%20...InputValue+%20%20}+%20%20interfaces%20{+%20%20%20%20...TypeRef+%20%20}+%20%20enumValues%20{+%20%20%20%20name+%20%20%20%20description+%20%20}+%20%20possibleTypes%20{+%20%20%20%20...TypeRef+%20%20}+}++fragment%20InputValue%20on%20InputValue%20{+%20%20name+%20%20description+%20%20type%20{+%20%20%20%20...TypeRef+%20%20}+%20%20defaultValue+}++fragment%20TypeRef%20on%20Type%20{+%20%20kind+%20%20name+%20%20ofType%20{+%20%20%20%20kind+%20%20%20%20name+%20%20%20%20ofType%20{+%20%20%20%20%20%20kind+%20%20%20%20%20%20name+%20%20%20%20%20%20ofType%20{+%20%20%20%20%20%20%20%20kind+%20%20%20%20%20%20%20%20name+%20%20%20%20%20%20%20%20ofType%20{+%20%20%20%20%20%20%20%20%20%20kind+%20%20%20%20%20%20%20%20%20%20name+%20%20%20%20%20%20%20%20%20%20ofType%20{+%20%20%20%20%20%20%20%20%20%20%20%20kind+%20%20%20%20%20%20%20%20%20%20%20%20name+%20%20%20%20%20%20%20%20%20%20%20%20ofType%20{+%20%20%20%20%20%20%20%20%20%20%20%20%20%20kind+%20%20%20%20%20%20%20%20%20%20%20%20%20%20name+%20%20%20%20%20%20%20%20%20%20%20%20%20%20ofType%20{+%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20kind+%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20name+%20%20%20%20%20%20%20%20%20%20%20%20%20%20}+%20%20%20%20%20%20%20%20%20%20%20%20}+%20%20%20%20%20%20%20%20%20%20}+%20%20%20%20%20%20%20%20}+%20%20%20%20%20%20}+%20%20%20%20}+%20%20}+}++query%20IntrospectionQuery%20{+%20%20schema%20{+%20%20%20%20queryType%20{+%20%20%20%20%20%20name+%20%20%20%20}+%20%20%20%20mutationType%20{+%20%20%20%20%20%20name+%20%20%20%20}+%20%20%20%20types%20{+%20%20%20%20%20%20...FullType+%20%20%20%20}+%20%20%20%20directives%20{+%20%20%20%20%20%20name+%20%20%20%20%20%20description+%20%20%20%20%20%20locations+%20%20%20%20%20%20args%20{+%20%20%20%20%20%20%20%20...InputValue+%20%20%20%20%20%20}+%20%20%20%20}+%20%20}+}
		* The last code line is a graphql query that will dump all the meta-information from the graphql (objects names, parameters, types...)
		* If introspection is enabled you can use [**GraphQL Voyager**](https://github.com/APIs-guru/graphql-voyager) to view in a GUI all the options.
	* No Introspection
		* More and more **graphql endpoints are disabling introspection**. However, the errors that graphql throws when an unexpected request is received are enough for tools like [**clairvoyance**](https://github.com/nikitastupin/clairvoyance) to recreate most part of the schema.
* <details><summary>Querying (Click to expand)</summary><p>
	* Now that we know which kind of information is saved inside the database, let's try to **extract some values**.
	* In the introspection you can find **which object you can directly query for** (because you cannot query an object just because it exists). In the following image you can see that the "_queryType_" is called "_Query_" and that one of the fields of the "_Query_" object is "_flags_", which is also a type of object. Therefore you can query the flag object.
	* You can see that the "_Flags_" objects are composed by **name** and .**value** Then you can get all the names and values of the flags with the query:

			query={flags{name, value}}
	* Note that in case the **object to query** is a **primitive** **type** like **string** like in the following example
	* You can just query is with:

			query={hiddenFlags}
	* In another example where there were 2 objects inside the "_Query_" type object: "_user_" and "_users_".\
	If these objects don't need any argument to search, could **retrieve all the information from them** just **asking** for the data you want. In this example from Internet you could extract the saved usernames and passwords:
	* However, in this example if you try to do so you get this **error**:
	* Looks like somehow it will search using the "_**uid**_" argument of type _**Int**_.\
	* Anyway, we already knew that, in the [Basic Enumeration](graphql.md#basic-enumeration) section a query was purposed that was showing us all the needed information: `query={__schema{types{name,fields{name, args{name,description,type{name, kind, ofType{name, kind}}}}}}}`
	* If you read the image provided when I run that query you will see that "_**user**_" had the **arg** "_**uid**_" of type _Int_.
	* So, performing some light _**uid**_ bruteforce I found that in _**uid**=**1**_ a username and a password was retrieved:\
	`query={user(uid:1){user,password}}`
	* And during the **enumeration phase** I discovered that the "_**dbuser**_" object had as fields "_**user**_" and "_**password**_.
	* Query string dump trick (thanks to @BinaryShadow\_)
		* If you can search by a string type, like: `query={theusers(description: ""){username,password}}` and you **search for an empty string** it will **dump all data**. (_Note this example isn't related with the example of the tutorials, for this example suppose you can search using "**theusers**" by a String field called "**description**"_).
		* GraphQL is a relatively new technology that is starting to gain some traction among startups and large corporations. Other than missing authentication by default graphQL endpoints can be vulnerable to other bugs such as IDOR.
* <details><summary>Searching (Click to expand)</summary><p>
	* For this example imagine a data base with **persons** identified by the email and the name and **movies** identified by the name and rating. A **person** can be **friend** with other **persons** and a person can **have movies**.
	* You can **search** persons **by** the **name** and get their emails (javacript):

			{
			  searchPerson(name: "John Doe") {
			    email
			  }
			}
	* You can **search** persons **by** the **name** and get their **subscribed** **films** (javascript):
	
			{
			  searchPerson(name: "John Doe") {
			    email
			    subscribedMovies {
			      edges {
			        node {
			          name
			        }
			      }
			    }
			  }
			}
	* Note how its indicated to retrieve the `name` of the `subscribedMovies` of the person.
	* You can also **search several objects at the same time**. In this case, a search 2 movies is done (javascript):

			{
			  searchPerson(subscribedMovies: [{name: "Inception"}, {name: "Rocky"}]) {
			    name
			  }
			}
	* Or even **relations of several different objects using aliases** (javascript):

			{
			  johnsMovieList: searchPerson(name: "John Doe") {
			    subscribedMovies {
			      edges {
			        node {
			          name
			        }
			      }
			    }
			  }
			  davidsMovieList: searchPerson(name: "David Smith") {
			    subscribedMovies {
			      edges {
			        node {
			          name
			        }
			      }
			    }
			  }
			}
* <details><summary>Mutations (Click to expand)</summary><p>
	* **Mutations are used to make changes in the server-side.**
	* For this example imagine a data base with **persons** identified by the email and the name and **movies** identified by the name and rating. A **person** can be **friend** with other **persons** and a person can **have movies**.
	* A mutation to **create new** movies inside the database can be like the following one (in this example the mutation is called `addMovie`) (javascript):

			mutation {
			  addMovie(name: "Jumanji: The Next Level", rating: "6.8/10", releaseYear: 2019) {
			    movies {
			      name
			      rating
			    }
			  }
			}
		* **Note how both the values and type of data are indicated in the query.**
	* There may also be also a **mutation** to **create** **persons** (called `addPerson` in this example) with friends and files (note that the friends and films have to exist before creating a person related to them) (javascript):

			mutation {
			  addPerson(name: "James Yoe", email: "jy@example.com", friends: [{name: "John Doe"}, {email: "jd@example.com"}], subscribedMovies: [{name: "Rocky"}, {name: "Interstellar"}, {name: "Harry Potter and the Sorcerer's Stone"}]) {
			    person {
			      name
			      email
			      friends {
			        edges {
			          node {
			            name
			            email
			          }
			        }
			      }
			      subscribedMovies {
			        edges {
			          node {
			            name
			            rating
			            releaseYear
			          }
			        }
			      }
			    }
			  }
			}
* <details><summary>Batching brute-force in 1 API request (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* [https://lab.wallarm.com/graphql-batching-attack/](https://lab.wallarm.com/graphql-batching-attack/).
	* Process
		* Authentication through GraphQL API with **simultaneously sending many queries with different credentials** to check it. It’s a classic brute force attack, but now it’s possible to send more than one login/password pair per HTTP request because of the GraphQL batching feature. This approach would trick external rate monitoring applications into thinking all is well and there is no brute-forcing bot trying to guess passwords.
		* Below you can find the simplest demonstration of an application authentication request, with **3 different email/passwords pairs at a time**. Obviously it’s possible to send thousands in a single request in the same way:
		* As we can see from the response screenshot, the first and the third requests returned _null_ and reflected the corresponding information in the _error_ section. The **second mutation had the correct authentication** data and the response has the correct authentication session token.
* <details><summary>CSRF in GraphQL (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* CSRF in GraphQL -<br />[https://blog.doyensec.com/2021/05/20/graphql-csrf.html](https://blog.doyensec.com/2021/05/20/graphql-csrf.html)
	* Process
		* Out there you are going to be able to find several GraphQL endpoints **configured without CSRF tokens.**
		* Note that GraphQL request are usually sent via POST requests using the Content-Type `application/json` (javascript):

				{"operationName":null,"variables":{},"query":"{\n  user {\n    firstName\n    __typename\n  }\n}\n"}
		* However, most GraphQL endpoints also support **`form-urlencoded` POST requests** (javascript):

				query=%7B%0A++user+%7B%0A++++firstName%0A++++__typename%0A++%7D%0A%7D%0A
		* Therefore, as CSRF requests like the previous ones are sent **without preflight requests**, it's possible to **perform** **changes** in the GraphQL abusing a CSRF.
		* However, note that the new default cookie value of the `samesite` flag of Chrome is `Lax`. This means that the cookie will only be sent from a third party web in GET requests.
		* Note that it's usually possible to send the **query** **request** also as a **GET** **request and the CSRF token might not being validated in a GET request.**
		* Also, abusing an XS-Search attack might be possible to exfiltrate content from the GraphQL endpoint abusing the credentials of the user.