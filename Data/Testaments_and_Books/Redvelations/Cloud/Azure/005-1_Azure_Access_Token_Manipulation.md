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

# Access Token Juggling

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@Teams #@Outlook #@Graph #@O365`

</details>

## Summary

Microsoft Azure and other related products such as Teams, Outlook, etc., utilize JWTs to determine authentication status. These tokens come with `refresh_tokens` that can be used to renew an existing `access_token`, or to request an `access_token` to another resource. The `access_token` usually only has a limited lifetime (about 2 hours). A `refresh_token` on the other hand may have a lifetime up to 90 days. Once you use a `refresh_token` to request a new `access_token`, you will also be presented with a new `refresh_token`. Juggling these tokens and keeping them alive gives an attacker a high level of persistence over an account.

- [`Cloud Accounts` TTP](TTP/T1078_Valid_Accounts/004_Cloud_Accounts/T1078.004.md)

## Prevention

This cannot be entirely prevented unless there is some information we are missing currently.

## Mitigation

This can be mitigated. A `refresh_token`'s lifetime cannot be altered, however you may deploy conditional access policies on sign-in frequency that will require the user to re-authenticate after X amount of time. At the time of writing this, there is not a blue team article written fully explaining the steps to mitigate this technique. Once there is, I'll come back and link to it here.

## Installation and Usage

### Installation

- Clone the repository:

```bash
git clone https://github.com/blacklanternsecurity/offensive-azure.git
```

- Navigate to the `./offensive-azure/Access_Tokens/` directory:

```bash
cd ./offensive-azure/Access_Tokens/
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

```bash
usage: token-juggle.py <resource> [-r 'refresh_token' | -R './path/to/refresh_token.json']

  =====================================================================================
  # Requests a new access token for a Microsoft/Azure resource using a refresh token. #
  #                                                                                   #
  # This script will attempt to load a refresh token from a REFRESH_TOKEN             #
  # environment variable if none is passed with '-r' or '-R'.                         #
  =====================================================================================

positional arguments:
  resource              The target Microsoft/Azure resource. Choose from the following: win_core_management,
                        azure_management, graph, ms_graph, ms_manage, teams, office_apps, office_manage, outlook,
                        substrate

optional arguments:
  -h, --help            show this help message and exit
  -r <refresh_token>, --refresh_token <refresh_token>
                        (string) The refresh token you would like to use.
  -R <refresh_token_file>, --refresh_token_file <refresh_token_file>
                        (string) A JSON file saved from this script containing the refresh token you would like to
                        use.
  -o <filename>, --outfile <filename>
                        (string) The path/filename of where you want the new token data (json object) saved. If not
                        supplied, script defaults to "./YYYY-MM-DD_HH-SS_<resource>_token.json"
```

#### Examples

Supplying a refresh token as an argument

```bash
python3 token-juggle.py teams -r '<refresh_token>'
```

Supplying a refresh token via `REFRESH_TOKEN` environment variable

```bash
python3 token-juggle.py outlook
```

Supplying a refresh token via `token-juggle.py` output file

```bash
python3 token-juggle.py ms_graph -R './path/to/YYYY-mm-DD_HH-MM-SS_<resource>_token.json'
```