<!--
 -------------------------------------------------------------------------------
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
 -------------------------------------------------------------------------------
-->

# Device Code Authentication Phishing

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Device #@DeviceCode #@Phishing`

</details>

## Summary

Device Code Auth Flow allows users to sign in to input-constrained devices such as a smart TV, IoT device, or printer. To enable this flow, the device has the user visit a webpage in their browser on another device to sign in. Once the user signs in, the device is able to get access tokens and refresh tokens as needed.

- [`Spearphishing Link` TTP](TTP/T1566_Phishing/002_Spearphishing_Link/T1566.002.md)

### Pros

- No need to register any apps
- No need to setup a phishing infrastructure for fake login pages etc.
- The user is only asked to sign in (usually to “Microsoft Office”) - no consents asked
- Everything happens in login.microsoftonline.com namespace
- Attacker can use any client_id and resource (not all combinations work though)
- If the user signed in using MFA, the access token also has MFA claim (this includes also the access tokens fetched using the refresh token)
- Preventing requires Conditional Access (and Azure AD Premium P1/P2 licenses)

### Cons

- The user code is valid only for 15 minutes

Of course, the attacker can minimise the time restriction by sending the phishing email to multiple recipients - this will increase the probability that someone signs in using the code.

Another way is to implement a proxy which would start the authentication when the link is clicked (credits to @MrUn1k0d3r). However, this way the advantage of using a legit microsoft.com url would be lost.

## Process Flow

- A user starts an app supporting device code flow on a device
- The app connects to Azure AD /devicecode endpoint and sends client_id and resource
- Azure AD sends back device_code, user_code, and verification_url
- Device shows the verification_url (hxxps://microsoft.com/devicelogin) and the user_code to the user
- User opens a browsers and browses to verification_url, gives the user_code when asked and logs in
- Device polls the Azure AD until after succesfull login it gets access_token and refresh_token

## Phishing Flow

- An attacker connects to /devicecode endpoint and sends client_id and resource
- After receiving verification_uri and user_code, create an email containing a link to verification_uri and user_code, and send it to the victim.
- Victim clicks the link, provides the code and completes the sign in.
- The attacker receives access_token and refresh_token and can now mimic the victim.

## Prevention

The only effective way for preventing phishing using this technique is to use Conditional Access (CA) policies. To be specific, the phishing can not be prevented, but we can prevent users from signing in based on certain rules. Especially the location and device state based policies are effective for protecting accounts. This applies for the all phishing techniques currently used.

## Mitigation

If the user has been compromised, the user’s refresh tokens can be revoked, which prevents attacker getting new access tokens with the compromised refresh token.

## Installation and Usage

### Installation

- Clone the repository:

```bash
git clone https://github.com/blacklanternsecurity/offensive-azure.git
```

- Navigate to the `./offensive-azure/Device_Code/` directory:

```bash
cd ./offensive-azure/Device_Code/
```

- Spawn a pip environment:

```bash
pipenv shell
```

- Install the requirements:

```bash
pip install -r requirements.txt
```

### Usage

- Open the script, and select which resource you are targetting by setting `resource` to one of the supplied URIs
- Execute the script:

```bash
python3 device-code-easy-mode.py
```

- Send your victim the `deviceLogin` URL along with the code they need to enter
  - The device code is only valid for 15 minutes
  - You may want to prep your victim before hand.
- Once the victim successfully authenticates, you will be presented with the access token and refresh token