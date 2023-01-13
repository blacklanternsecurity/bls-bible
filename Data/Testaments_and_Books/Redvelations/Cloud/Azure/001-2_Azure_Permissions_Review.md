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
## Consent and Permissions

* Applications can ask users for permissions to access their data. For example, for basic sign-in
* If allowed, a normal user can grant consent only for "Low Impact" permissions. In all other cases, admin consent is required (an admin is notified over email).
* GA, Application Administrator, Cloud Administrator and a custom role including 'permission to grant permissions to applications' can provide tenant-wide consent.

### App Consent Policies

* Consent policies can be set for all users
	* Do not allow user consent
	* Allow user consent for apps from verified publishers, for selected permissions - Only for "Low Impact" permissions for apps from same tenant and verified publisher
	* Allow user consents for all apps - Allows consent for apps from other tenants and unverified publishers for Low Impact permissions
	* Custom app consent policy
* 'Allow user consent for all apps' is interesting and **abusable**

### Low Impact Permissions

* Only the permissions that don't need admin consent can be classified as low impact
* Permissions required for basic sign-in are openid, profile, email, User.Read and offline_access
* That means, if an organization allows user consent for all apps, an employee can grant consent to an app to read the above from their profile
* There are some very interesting low impact permissions. For example: **User.ReadBasic.All** that allows the app to read display name, first and last name, email address, open extensions and photo for all the users