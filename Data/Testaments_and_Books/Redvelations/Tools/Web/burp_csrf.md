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
# Burp CSRF bypass

#@TODO

1. Make the request that returns the desired token (proxied through Burp)
2. Go to `Project Options` --> `Sessions`
    - under `Macros`, click `Add`
    - select the request you just made in the browser
    - click `Ok` --> `Ok`
3. Under `Session Handling Rules`, click `Add`
    - under `Rule Actions`, click `Add` --> `Run a Macro`
    - select `Update only the following parameters` and type the names of the cookies, POST parameters, etc. that you need
    - click `Ok`
    - Under the `Scope` tab, make sure the desired tools are checked and the `URL Scope` is set up to match the target site
    - click `Ok`
4. Recommend testing in Repeater before using Intruder, etc.