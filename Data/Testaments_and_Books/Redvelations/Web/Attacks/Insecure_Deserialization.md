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
# Insecure Deserialization

## Resources

#### Training ####

* **Portswigger Web Academy - Insecure Deserialization** - [https://portswigger.net/web-security/deserialization](https://portswigger.net/web-security/deserialization)
* **Pentester Lab** - [https://pentesterlab.com/](https://pentesterlab.com/)

#### General ####

* **Payload all the things - Insecure Dserialization** - [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization)

* **JSON deserialization attacks** (.NET and Java) [https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf)

* **PHP Phar unserialize exploits** [https://i.blackhat.com/us-18/Thu-August-9/us-18-Thomas-Its-A-PHP-Unserialization-Vulnerability-Jim-But-Not-As-We-Know-It-wp.pdf](https://i.blackhat.com/us-18/Thu-August-9/us-18-Thomas-Its-A-PHP-Unserialization-Vulnerability-Jim-But-Not-As-We-Know-It-wp.pdf)

* **OWASP Deserialization Cheatsheet** - [https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)

## Tools

#### Known gadget chains exploitation

* **Java** - [https://github.com/frohoff/ysoserial](https://github.com/frohoff/ysoserial)
* **PHP** - [https://github.com/ambionics/phpggc](https://github.com/ambionics/phpggc)
* **C#** - [https://github.com/pwntester/ysoserial.net](https://github.com/pwntester/ysoserial.net)
* **Ruby 2.x Universal Gadget Chain** - [https://www.elttam.com/blog/ruby-deserialization/](https://www.elttam.com/blog/ruby-deserialization/)
* **Python Pickle Injection** - [http://xhyumiracle.com/python-pickle-injection/](http://xhyumiracle.com/python-pickle-injection/)


## Overview
* .NET .NET viewstate derialization specifics [Guide](Testaments_and_Books/Redvelations/Apps_and_Services/Web/Attacks/.net_viewstate_deserialization.md).

## Key Takeaways

* Deserialization of user-supplied data is always a dangerous practice
* The exploit process is quite language-specific
* Control of the object type is particularly dangerous

## Summary

#### Background

In object-oriented programming lanaguages, serialization is simply the practice of converting an object into a data format which is more favorable for transmission of the web (or storage). Deserialization is the opposite, turning this data back into a fully usable object. There are a variety of formats which are used to house serialized data, including:

* A semi-human-readable string, converted to base64 (this is the format for PHP)
* A binary string, converted to base64 or hex (commonly used by Java)
* XML
* JSON

Serialization might also be referred to as **marshalling** or **pickling**. 

Despite sometimes sharing the same text formatting (JSON is currently the most popular), the contents of the serialized object are quite different for every language. Each language has its own set of particular nuances that require different tools to handle. This nuance is carried even farther by differences in individual serialization libraries. 

#### The danger

Deserialization attacks are sometimes called **object injection**, which probably does a better job of conveying their function. An attacker can cause the application to instantiate an object of their choice, in hopes of tricking the application into executing code that can be abused. Sometimes getting to this useful code requires lengthy gadget chains (explained below).

Deserializing user input is always inherantly dangerous, but particularly so if the attacker is allowed to choose the object type. The attacker might have full, partial, or no control of the object type - and full, partial, or no control over the methods which are invoked and the content use with them.

Full control of the type is particularly dangerous and in the absence of any other countermeasurs will almost surely result in an exploitable vulnerability. 

It is important to note that deserialization itself is not inherently dangerous. It is only when performed on user-supplied data. It is possible to deserialize user-supplier safely, but because it is difficult to defend against unknown gadget chains it must be done carefully.

The objects which are available to the attacker can vary significantly from application to application, and this will directly affect the exploitability.

#### Gadget chains

The term gadget chain just refers to the process of traversing through a chain of object methods until arriving at one that can perform a dangerous action on behalf of the attacker. An object might have a method that instantiate another object, which itself has a method that instantiates another object, etc. At the end of the gadget chain there is an object that has a method which performs some action which is useful to an attacker. Some examples might be:

* Direct code execution
* Writing an arbitrary file
* Reading an arbitrary file
* Deleting an arbitrary file 
* SQL Injection
* SSRF

#### Attack methodology

There are generally three broad categories when it comes to attacking insecure deserialization: **known gadget chain**, **custom gadget chain**, and **object manipulation**.

With a known gadget chain, you might identify some software, or library within custom software, which is has a known gadget chain. Using that languages corresponding tool, you can generate an exploit payload and try to exploit it.

If you are dealing with completely custom code, there will obviously not be a known gadget chain, but you can create your own based on this code. This typically requires access to the source code. 

With object manipulation, an attacker may be able to modify values within an object but be unable to change the type or manipulate the method being called. This can still be very dangerous in ther right situation. Doing so can have a range of effects, including logic flaws, SQL injection, authentication bypass, etc. 


#### Burp extensions



## Payloads

#### Java

* [Generic Payload Generation Template](Testaments_and_Books/Redvelations/Apps_and_Services/Web/Payloads/Insecure_Deserialization/generic/Main.java)

#### PHP

Generic Serialization Example:

```
<?php
class User{
public $username;
public $status;
}
$user = new User;
$user->username = 'vickie';
$user->status = 'not admin';
echo serialize($user);
?>
```

PHP Phar Serialization:

Theoretical example of vulnerable PDFGenerator class:

```
<?php
class PDFGenerator { }

//Create a new instance of the Dummy class and modify its property
$dummy = new PDFGenerator();
$dummy->callback = "passthru";
$dummy->fileName = "uname -a > pwned"; //our payload

// Delete any existing PHAR archive with that name
@unlink("poc.phar");

// Create a new archive
$poc = new Phar("poc.phar");

// Add all write operations to a buffer, without modifying the archive on disk
$poc->startBuffering();

// Set the stub
$poc->setStub("<?php echo 'Here is the STUB!'; __HALT_COMPILER();");

/* Add a new file in the archive with "text" as its content*/
$poc["file"] = "text";
// Add the dummy object to the metadata. This will be serialized
$poc->setMetadata($dummy);
// Stop buffering and write changes to disk
$poc->stopBuffering();
?>
```

#### C# .NET

Generic Serialization Example (XML):

```
public class SerializableClass
{
 public string StringProperty { get; set; }
 public int IntegerProperty { get; set; }
}
SerializableClass sc = new SerializableClass();
sc.StringProperty = "Hello World!";
sc.IntegerProperty = 42;
XmlSerializer ser = new XmlSerializer(typeof(SerializableClass));
using (FileStream stm = File.OpenWrite("output.xml"))
{
 ser.Serialize(stm, sc);
}
```


