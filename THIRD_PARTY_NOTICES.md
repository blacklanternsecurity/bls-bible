# Third-party notices

This repository is licensed under AGPL-3.0-or-later (see `LICENSE`). The material
below comes from third parties and remains under its original license. Where that
license is not compatible with AGPL-3.0, the listed files are excluded from the AGPL
grant and stay under their original license. Full license texts that a license
requires to be shipped are in `LICENSES/` or reproduced here.

## Embedded third-party code and text

### Atomic Red Team (Red Canary)

- Source: https://github.com/redcanaryco/atomic-red-team
- Used in: 31 files under `Data/TTP/` restructure Atomic Red Team test descriptions, commands and dependency blocks. Each carries a note saying so.
- License: MIT

```
The MIT License

Copyright (c) 2018 Red Canary, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

### printerbug.py (krbrelayx)

- Source: https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py
- Used in: `Data/TTP/T1557_Adversary-in-the-Middle/001_.../T1557.001.md` (verbatim, notice retained)
- License: MIT

```
The MIT License (MIT)

Copyright (c) 2019 Dirk-jan Mollema (@_dirkjan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### PayloadsAllTheThings

- Source: https://github.com/swisskyrepo/PayloadsAllTheThings
- Used in: `Data/Testaments_and_Books/Redvelations/Web/Attacks/Insecure_Deserialization.md` (PHP phar example)
- License: MIT

```
MIT License

Copyright (c) 2019 Swissky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### PowerUp (PowerSploit)

- Source: https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1 (`Get-ApplicationHost`, by Scott Sutherland)
- Used in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/PowerUp_Script.md`
- License: BSD-3-Clause

```
PowerSploit is provided under the 3-clause BSD license below.

*************************************************************

Copyright (c) 2012, Matthew Graeber
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    The names of its contributors may not be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### The Hacker Recipes

- Source: https://github.com/The-Hacker-Recipes/The-Hacker-Recipes (MachineAccountQuota query, Charlie Bromberg)
- Used in: `Data/Testaments_and_Books/Redvelations/Active_Directory/scripts/MachineAccountQuota.py`
- License: GPL-3.0. That file stays GPL-3.0; full text in `LICENSES/GPL-3.0.txt`.

### Unix & Linux Stack Exchange answer 398497

- Source: https://unix.stackexchange.com/a/398497 (Satō Katsura, 2017)
- Used in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_64-Bit.c` (verbatim)
- License: CC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0/. CC BY-SA 3.0 is not compatible with the GPL family, so this file is excluded from the repository's AGPL grant and stays CC BY-SA 3.0.

## Vendored assets in `bls_bible/static/`

### Bootstrap 5.0.0-beta2

- Source: https://github.com/twbs/bootstrap
- Used in: `bls_bible/static/css/bootstrap.min.css(.map), js/bootstrap.bundle.min.js`
- License: MIT

```
The MIT License (MIT)

Copyright (c) 2011-2026 The Bootstrap Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

### jQuery 3.5.1

- Source: https://github.com/jquery/jquery
- Used in: `bls_bible/static/js/jquery-3.5.1.min.js`
- License: MIT

```
Copyright OpenJS Foundation and other contributors, https://openjsf.org/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

### jQuery UI 1.13.1

- Source: https://github.com/jquery/jquery-ui
- Used in: `bls_bible/static/js/jquery-ui.min.js`
- License: MIT

```
Copyright OpenJS Foundation and other contributors, https://openjsf.org/

This software consists of voluntary contributions made by many
individuals. For exact contribution history, see the revision history
available at https://github.com/jquery/jquery-ui

The following license applies to all parts of this software except as
documented below:

====

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

====

Copyright and related rights for sample code are waived via CC0. Sample
code is defined as all source code contained within the demos directory.

CC0: http://creativecommons.org/publicdomain/zero/1.0/

====

All files located in the node_modules and external directories are
externally maintained libraries used by this software which have their
own licenses; we recommend you read them, as their terms may differ from
the terms above.
```

### SimpleMDE 1.11.2

- Source: https://github.com/sparksuite/simplemde-markdown-editor
- Used in: `bls_bible/static/css/simplemde.min.css, js/simplemde.min.js`
- License: MIT

```
The MIT License (MIT)

Copyright (c) 2015 Next Step Webs, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### CodeMirror (bundled in SimpleMDE)

- Source: https://github.com/codemirror/codemirror5
- Used in: `bls_bible/static/js/simplemde.min.js`
- License: MIT

```
MIT License

Copyright (C) 2017 by Marijn Haverbeke <marijn@haverbeke.berlin> and others

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

### GitHub Linguist language list

- Source: https://github.com/github-linguist/linguist
- Used in: `bls_bible/static/languages.yml`
- License: MIT

```
Copyright (c) 2017 GitHub, Inc.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```

### Material Icons (Google)

- Source: https://github.com/google/material-design-icons
- Used in: `bls_bible/static/css/mat-icons.woff2`
- License: Apache-2.0; full text in `LICENSES/Apache-2.0.txt`.

### MITRE ATT&CK

- Source: https://github.com/mitre/cti
- Used in: `bls_bible/static/mitre/enterprise-attack.json`, `bls_bible/static/mitre/groups/apts.json` (derived)
- License: ATT&CK Terms of Use, https://attack.mitre.org/resources/legal-and-branding/terms-of-use/
- Notice: © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.

### King James Bible text

- Used in: `bls_bible/static/FULLTEXT.txt`, `FULLTEXT2.txt`, `genesis.txt`, `verses.json`
- Status: public domain in the United States (Crown letters patent apply in the United Kingdom).

## Git submodules

These are references to other repositories, not content in this one, and each stays under its own license: `The-Hacker-Recipes` (GPL-3.0) and `PayloadsAllTheThings` (MIT).

## Removed on 2026-10-23

The material below was removed entirely because Black Lantern Security could not confirm it has the right to
redistribute it: either no license was found, the license restricts redistribution, or its provenance could not
be established. It is listed here so the removal is traceable.

- **CACTUSTORCH** by Vincent Yiu (@vysecurity), MDSec ActiveBreach. Source: https://github.com/vysecurity/CACTUSTORCH. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/CactusTorch.js; help banner in Data/Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md`.
- **MSBuild shellcode runners** by dxflatline, original work by Casey Smith (@subTee). Source: https://gist.github.com/dxflatline/99de0da360a13c565a00a1b07b34f5d1. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_dxflatline.xml, _Joel_and_Kerry.xml, _64-bit.xml; Data/TTP/T1127_.../T1127.001.md`.
- **MSBuild ClassExample** by Casey Smith (@subTee). Source: https://github.com/tuian/subTee-gits-backups. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_SubTee.xml`.
- **msbuildQueueAPC.csproj** by vector-sec. Source: https://gist.github.com/vector-sec/1f543c30d0bbc691a6f50a1cc549cef1. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/MSBuild_XML_Shell_vector-sec.xml`.
- **AppDomainManager injection** by Casey Smith (@subTee). Source: https://github.com/kafkaesqu3/subtee-gist-mirror. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/Arbitary_dotnet.cs, Arbitrary_dotnet.exe.config, file.exe.config`.
- **AMSI bypass (AmsiScanBuffer patch, Bypass-AMSI)** by Andre Marques (0x00-0x00). Source: https://0x00-0x00.github.io/research/2018/10/28/How-to-bypass-AMSI-and-Execute-ANY-malicious-powershell-code.html. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/PowerShell_AMSI_Bypass.cs; Data/TTP/T1562_.../T1562.001.md; Data/Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md`.
- **SilentCleanup UAC bypass wrapper** by chryzsh (wrapper); Julio Ureña (C# core, GPL-3.0). Source: https://github.com/chryzsh/Aggressor-Scripts/blob/master/uac-bypass/uac_silentcleanup.ps1. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/bypass_uac_1.ps1, powershell-uac-always-notify-bypass.ps1`.
- **Java serialization template** by PortSwigger. Source: https://github.com/PortSwigger/serialization-examples/tree/master/java/generic. Was in: `Data/Testaments_and_Books/Redvelations/Web/Payloads/Insecure_Deserialization/generic/Main.java, data/Foo.java`.
- **Execute-userAccountControl** by netbiosX. Source: https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c. Was in: `Data/Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md`.
- **ComObjectExec and Move-DLL VBA** by Emeric Nasi (sevagas). Source: https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf. Was in: `Data/Testaments_and_Books/Redvelations/Windows/002-3_VBA-VBS_Execution.md`.
- **.searchConnector-ms lure** by David Middlehurst (@dtmsecurity). Source: https://dtm.uk. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/Search_Connector_File.xml`.
- **API Monitor filter** by Rohitab Batra. Source: http://www.rohitab.com/apimonitor. Was in: `Data/Testaments_and_Books/Redvelations/Windows/Payloads/filter.xml`.
- **Fonts "Road Rage" (personal use only) and "Paint Drops" (all rights reserved)** by Youssef Habchi; 177Studio. Source: http://youssef-habchi.com; https://177studio.com. Was in: `bls_bible/static/css/Road_Rage.otf, blood.ttf; `site.css` now uses system fonts`.
- **Nine `Data/TTP/` pages whose provenance could not be confirmed**: T1021, T1078.002, T1098, T1135, T1482, T1543.003, T1556.001, T1558.002, T1574.002.
- **Two `Data/TTP/` pages made up of VBA of unconfirmed origin**: T1497, T1053.
- **Twelve files of unconfirmed origin** under `Data/Testaments_and_Books/Redvelations/`: Workflow-Compiler `.c`/`.xml`, `config-file-lolbin.xml`, `Global_Assembly_Cache.config`, `Evil_Clippy_Working_Payload.md`, `VBA1.vba`, `VBA2.vba`, `exchangelib.py`, `SQLI_2nd_order_Multi-Verb.py`, `Azurehound-Bloodhound-JSON-Chunking.py`, `dictionary_word_obfuscation.py`, `CSRF.txt`.
- **Threat-actor samples** (CONTI, 2021-08): four files under `Purplippians/Threat_Intel/2021-08-CONTI/Payloads/`.
- **Submodules** `hacktricks`, `RedTeaming-Tactics-and-Techniques` and `Hackers-Rest`: license not verified or none found.
