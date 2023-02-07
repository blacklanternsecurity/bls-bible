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
# Initial Web Attack Checklist
### Reference
* [https://pentestbook.six2dez.com/others/web-checklist](https://pentestbook.six2dez.com/others/web-checklist)

### Process
* CSP
	* Review the Content Security Policy header
		* Automatic checks (insert CSP header directly in; likely not considered sensitive info)
			* Google's CSP Evaluator
				* Website -<br />[https://csp-evaluator.withgoogle.com/](https://csp-evaluator.withgoogle.com/)
				* Extension -<br />[https://chrome.google.com/webstore/detail/fjohamlofnakbnbfjkohkbdigoodcejf](https://chrome.google.com/webstore/detail/fjohamlofnakbnbfjkohkbdigoodcejf)
* Time-based attack
* Technology Specific
	* [JavaScript](Testaments_and_Books/Redvelations/Apps_and_Services/Web/002-1_javascript_Checklist.md)
	* [NodeJS](Testaments_and_Books/Redvelations/Apps_and_Services/Web/002-2_nodejs_Checklist.md)
