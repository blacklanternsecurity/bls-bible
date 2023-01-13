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
# README.md
## Application Setup
### pipx
1. Install pipx
	1. Install pipx with pip

			pip3 install --user pipx
	1. Ensure that pipx-installed tools are in your path

			pipx ensurepath
1. Install the BLS Bible
	
		pipx install git+https://gitlab.com/BLS/bls-bible
### Poetry
1. Run the app with poetry

		poetry run python app.py

### Python

* Easy install
	1. Install python and pip

			apt install python3 python3-pip
	1. install tool requirements

			pip3 install -r requirements.txt
* Run the server application

		python3 app.py

### Docker

1. The **docker-compose.yml** and **Dockerfile** files are prepared for immediate build. Just run:

		sudo docker-compose up -d

## Application Access

1. Navigate to the webpage once install is complete and the application server is running

		localhost:5000

## Data
### Update
* In the web application, the data can be updated by accessing the update endpoint. The app scrape the gitlab repo or wherever you cloned the repo and update the `arf.json` file. The page will notify you when it is done.

		localhost:5000/update

### Additional Data Options

Two additional folders (currently) are prepared for the user to include their own data, **Assessalonians** and **Apocrypha**.

It is recommended that the user add in their private content to the **Assessalonians** folder, including organizing assessment-related directions. This data is then kept out of any potential future contributions to the project. The **Apocrypha** folder is intended for holing additional GitBook repositories that can be included in the application's local search process.

## Preparation, Configuration

Define the following configuration settings, which have further details under subsequent headers:

* Server Type
	* Shared Server
	* Operations Server
	* Self-Server
* Assessalonians Location
* Apocrypha Selection
* Auto-update settings

### Server Type

There are three pre-defined server types that can be adjusted with custom settings as needed. Each is designed to meet the needs of three supported functions.

In the shared server design, end-users are intended to access the BLS Bible server from a shared, static server. Users are intended to have shared the access to the server and are consequently restricted from accessing certain server functions that would affect other users, including the in-app file edit feature. 

The operations server design is intended for cases where multiple operators are testing a network together. The configuration choices are intended to support multiple users that are expected to perform sensitive functions with the server and store sensitive data. However, the server is intended for very short term usage.

The self-server design is intended to be used by a single operator with full control over their local server. The server can be used to individual goals such as CTFs or content development for the BLS Bible.

### Assessalonians Location

Assessalonians is intended to be a dedicated folder for containing contents related to engagement operations. For example, contents may specifically guiding operators on expectations for setting up infrastructure, or preferred tools and techniques to use in networks.

### Apocrypha Selection

The Apocrypha are additional sources of content that can provide operators with insight that the BLS Bible may not already have. The BLS Bible is optimized for presenting information according to various use cases, but the total content may not include the breadth of other well-known guides. In configuring the application, several pre-selected options are available for inclusion as Apocrypha, but you may configure additional repositories and API keys to retrieve additional content.

## Usage
### From the application

In the initial dashboard, several options appear for the user to click:

* Leaderboard
	* The Leaderboard button will redirect the user to view project contributors ordered according to the contributors' total content submitted.
* Manage Profiles
	* The Manage Profiles button produces an interface for the user when clicked to manage threat profiles. 
* Filters, `(.*)`
	* The filter buttons allow a user to refine results. The `(.*)` button will produce a user interface that allows advanced regex searches with grep-like capabilities, providing similar advantages seen in command line search.
* Update
	* The Update button will redirect a user to an update interface where a user can update the application's index of files (default), and/or pull in more recent MITRE data
* Settings (Cog Icon)
* The Books
* MITRE TTPs

### The Books

The application presents the data as Redvelations on the left, representing the traditional "Red Team" tactics, techniques, and procedures (TTPs), including Active Directory relay attacks. On the right, the Blue Testament represents the traditional "Blue Team" TTPs, including GPO configuration recommendations.

### MITRE TTPs

MITRE TTPs a presented as the central bridge between the traditional "Red" and "Blue" TTPs. 

### Key Features, Optimal Use

The application is designed to fit with a variety of engagement operations' workflow. Below are several example outlines of how engagements can make the most of the application:

### Traditional Penetration Test

1. Operators begin by following guidance contained with Assessalonians. Assessalonians ensures that the operator is achieving the expected steps by the organization.
1. Operators create a new threat profile to track the TTPs used during their engagement.
	1. Click the "Manage Profiles" button in the top-left area of the application
	1. Click the **+** button to add a new threat profile
	1. Name the threat profile something meaningful
1. Operators perform attacks in the engagement following a mix of information from the books of Redvelations, Assessalonians, and Apocrypha.
1. Operators record TTPs used
	* Current Feature Set - Manual)
		1. Operators type in the attacks they successfully complete into the search bar at the center-top of the application
			* Note that as Redvelations improves, the MITRE TTPs will appear listed alongside the detailed attacks. This detail provides an advantage over the books not optimized for this process, including the GitBooks contained in the Apocrypha.
		1. Operators right-click the related TTPs, click "Add To Profile," and select the recently created threat profile.
			* If the operator forgot to add a profile by this point, the application will take care of the operator and provide an option to create a new profile with a button, "Add To New Profile."
	* Future Feature Set - Automated
		1. Operator attacks that are executed are logged by the local system
		1. The local system forwards the techniques to a Red Team SIEM that can interpret the activities and produce a list of TTPs.
		1. The Red Team SIEM sends the executed TTPs to the BLS Bible, which organizes the TTPs into an operations threat profile.
1. Operators produce reports and data to examine activities of the engagement.
	1. Click Manage Profiles
	1. Select any of these options to produce reports:
		* **Match To Known Profiles**
		* **Export For ATT&CK Navigator**
		* **Export TTPs To PDF**


### Threat Hunt

1. Collect a list of potential TTPs performed by the threat actor
1. Create a new threat profile for tracking the identified TTPs
	1. Click the "Manage Profiles" button in the top-left area of the application
	1. Click the **+** button to add a new threat profile for this threat hunt
	1. Name the threat profile something meaningful
1. Type each TTP into the search bar, and as the TTP appears, right-click and select "Add To Profile." Select the recently created threat profile.
	* If you forgot to add a profile by this point, the application will take care of you and provide an option to create a new profile with a button, "Add To New Profile."
1. Return to "Manage Profiles," click the tick-box next to the threat profile, and keep "Match To Known Profiles" highlighted (default) at the top. Click the button to the right of the "Match To Know Profiles" to produce a dashboard showing which known threat actors match with the indicated TTPs.
1. For additional exploration, the steps above can be followed with the Manage Profiles option set to **Open TTPs In Tabs** or **Export TTPs To PDF**.

### Purple Team Table-Top Exercises
#### Note

Many approaches can be used to perform table-top exercises, but a few example methods are documented below. The various methods described can likely have the steps switched with other examples as you prefer.

#### Emulating Real Threats - MITRE

1. 



#### Emulating Real Threats - Past Assessments






## Contributing

Contributions are very appreciated!

For git newbies, here's a rough workflow you can follow, but feel free to adjust as you pickup more knowledge:

1. Clone the repo locally. The branch with the latest features being updated is Development, so we'll use that for contrbution.

		git clone https://github.com/blacklanternsecurity.com/bls-bible.git --branch development
1. Checkout a new branch so that your future changes can be reviewed in comparison to the existing development branch.

		git checkout -b  "New-Branch-Name"
1. Make your contrubutions into the repo.
1. Commit your changes locally. The below commmand will automatically allow you to insert a message using your system's default message editor (e.g., vim, nano), unless you append `-m "commit message"`.

		git commit
1. Push the committed changes to the external repo.

		git push
1. Review the branch in the GitHub GUI to confirm your changes. When you are ready, submit a merge request for your branch to be merged into development.
1. Eventually, the development branch will be merged into the main branch for the majority end-user.

### Additional configurations to make contributing easier
* Setup your Git profile with an SSH key so committing and pushing files does not require your credentials again. To take advantage of this once setup, clone the repository with the following command:

		git clone git@github.com:blacklanternsecurity/bls-bible.git --branch development
* To automatically set your designate your git settings to automatically setup your upstream branch and save a step, use the below command:

		git config --global push.autoSetupRemote true
	* References
		* [https://twitter.com/SantoshYadavDev/status/1558086948484530177](https://twitter.com/SantoshYadavDev/status/1558086948484530177)
		* [https://git-scm.com/docs/git-config#Documentation/git-config.txt-pushautoSetupRemote](https://git-scm.com/docs/git-config#Documentation/git-config.txt-pushautoSetupRemote)

## Development Setup
### Poetry
1. Install poetry

		curl -sSL https://install.python-poetry.org | python3 -
1. Navigate into BLS Bible working directory
1. Install the app with poetry

		poetry install
1. Enter a shell with poetry

		poetry shell