# -------------------------------------------------------------------------------
# Copyright:   (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
# threat_profiles.py

import json
import os
import hashlib
import markupsafe
import time
import re
from bs4 import BeautifulSoup
from weasyprint import HTML
from weasyprint import CSS
from bls_bible.lib.utils import utils


class manage_profiles:
    def __init__(self, localPath):
        self.localPath = localPath
        self.utils = utils(self.localPath)
        self.threat_profile_file = self.localPath + "bls_bible/static/profiles.json"

    def getGroups(self):
        content = ""
        try:
            f = open(self.threat_profile_file)
            data = json.load(f)
            f.close()
        except Exception as e:
            print("Failed to read profiles.json")
            print(e)
            return ""
        for profile in data:
            content += '<div class="profile-container">'
            content += '<div class="row profile-title">'
            content += (
                '<div class="col-sm-1">'
                '<input type="checkbox" class="form-check-input '
                'threat-profile-check" value="'
                + str(markupsafe.escape(profile["id"]))
                + '"></div>'
            )
            content += (
                '<div class="col-sm-8">'
                + str(markupsafe.escape(profile["name"]))
                + "</div>"
            )
            content += (
                "<span onclick=\"editGroup('"
                + str(markupsafe.escape(profile["id"]))
                + '\')" class="material-icons col-sm-1 no-border">edit</span>'
            )
            content += (
                "<span onclick=\"deleteGroup('"
                + str(markupsafe.escape(profile["id"]))
                + '\')" class="material-icons col-sm-1 no-border">delete</span>'
            )
            content += "</div>"
            if profile["ttps"]:
                content += '<div class="row profile-ttps">'
                if profile["ttps"]:
                    content += "<ul>"
                    for ttp in profile["ttps"]:
                        if not ttp["ttp_minor"] == "":
                            content += (
                                "<li>"
                                + str(markupsafe.escape(ttp["ttp_file"]))
                                + " - "
                                + str(markupsafe.escape(ttp["ttp_major"]))
                                + " - "
                                + str(markupsafe.escape(ttp["ttp_minor"]))
                                + "</li>"
                            )
                        else:
                            content += (
                                "<li>"
                                + str(markupsafe.escape(ttp["ttp_file"]))
                                + " - "
                                + str(markupsafe.escape(ttp["ttp_major"]))
                                + "</li>"
                            )
                content += "</ul>"
                content += "</div>"
            content += "</div>"
        return content

    def createGroup(self, name="New Threat Profile", ttp=None):

        # load in the profiles data file
        try:
            f = open(self.threat_profile_file)
            data = json.load(f)
            f.close()
        except Exception as e:
            data = []
            print(e)

        # using seconds since epoch to generate ids for each threat profile
        # should hopefully avoid collisions
        id = hashlib.md5(str(time.time()).encode()).hexdigest()

        # Append to our data a new threat profile entry
        ttps = []
        if ttp:
            ttps.append(ttp)

        profile = {"id": id, "name": name, "ttps": ttps}

        """
		Structure of a profile object:
		{
			'id': "<md5 hash>",
			'name': "Threat Actor Delta",
			'ttps': [{ttp},{ttp}]
		}
		"""

        """
		Structure of a TTP object:
		{
			'ttp_file': 'T1234.123.md',
			'ttp_major': 'Exploit the shit',
			'ttp_minor': 'Using magic'
		}
		"""

        data.append(profile)

        try:
            with open(self.threat_profile_file, "w+") as out:
                json.dump(data, out, indent=4)
        except Exception as e:
            print("Failed to write to profiles.json")
            print(e)

        return self.getGroups()

    def deleteGroup(self, id):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            data = json.load(f)
            f.close()
        except Exception as e:
            print("Failed to read profile data")
            print(e)
            data = {}

        for profile in data:
            if profile["id"] == id:
                data.remove(profile)
                break

        with open(self.localPath + "bls_bible/static/profiles.json", "w+") as out:
            json.dump(data, out, indent=4)

        return self.getGroups()

    def getGroupForEdit(self, id):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            data = json.load(f)
            f.close()
        except Exception as e:
            print("Failed to read profile data")
            print(e)
            data = {}

        group = {}
        for profile in data:
            if profile["id"] == id:
                group = profile
                break

        content = ""

        content += '<div class="group-edit-container">'  # close container
        content += '<div class="row" style="margin-top:10px;">'  # open row 1
        content += '<div class="col-sm-12">'  # open col 1
        content += '<div class="form-group">'  # open form-group
        content += '<label for="profile_name">Name:</label>'
        content += (
            '<input id="profile_name" class="form-control bg-dark text-light" type="text" value="'
            + str(markupsafe.escape(group["name"]))
            + '">'
        )
        content += "</div>"  # close form-group
        content += "</div>"  # close col 1
        content += "</div>"  # close row 1
        content += '<div class="row" style="margin-top:10px;">'  # open row 2
        content += '<div class="col-sm-12">'  # open col 1
        if len(group["ttps"]) > 0:
            content += '<label for="ttp-list">Sort TTPs:</label>'
            content += '<ul id="ttp-list" class="group-edit-ttps">'
            for ttp in group["ttps"]:
                if not ttp["ttp_minor"] == "":
                    content += (
                        '<li data-ttp-file="'
                        + str(markupsafe.escape(ttp["ttp_file"]))
                        + '" data-ttp-major="'
                        + str(markupsafe.escape(ttp["ttp_major"]))
                        + '"  data-ttp-minor="'
                        + str(markupsafe.escape(ttp["ttp_minor"]))
                        + '" class="group-edit-ttp">'
                        + str(markupsafe.escape(ttp["ttp_file"]))
                        + " - "
                        + str(markupsafe.escape(ttp["ttp_major"]))
                        + " - "
                        + str(markupsafe.escape(ttp["ttp_minor"]))
                        + '<span onclick="removeTTP(this);" style="margin-left:auto;" '
                        'class="material-icons no-border">delete</span>'
                        + '<span style="" '
                        'class="material-icons no-border">drag_handle</span></li>'
                    )
                else:
                    content += (
                        '<li data-ttp-file="'
                        + str(markupsafe.escape(ttp["ttp_file"]))
                        + '" data-ttp-major="'
                        + str(markupsafe.escape(ttp["ttp_major"]))
                        + '"  data-ttp-minor="'
                        + str(markupsafe.escape(ttp["ttp_minor"]))
                        + '" class="group-edit-ttp">'
                        + str(markupsafe.escape(ttp["ttp_file"]))
                        + " - "
                        + str(markupsafe.escape(ttp["ttp_major"]))
                        + '<span onclick="removeTTP(this);" style="margin-left:auto;" '
                        'class="material-icons no-border">delete</span>'
                        + '<span style="" '
                        'class="material-icons no-border">drag_handle</span></li>'
                    )
            content += "</ul>"
        content += "</div>"  # close col 1
        content += "</div>"  # close row 2
        content += "</div>"  # close container
        content += '<div class="row group-footer">'  # open row 3
        content += '<span class="col-sm-10"></span>'  # col 1
        content += (
            "<span onclick=\"updateGroup('"
            + str(markupsafe.escape(group["id"]))
            + '\')" class="col-sm-2 material-icons">save</span>'
        )  # col 2
        content += "</div>"  # close row 3

        return content

    def updateGroup(self, id, name, ttps):

        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            data = json.load(f)
            f.close()

        except Exception as e:
            print("Failed to read profile data")
            print(e)
            data = {}

        for profile in data:
            if profile["id"] == id:
                profile["name"] = name
                profile["ttps"] = ttps
                break

        with open(self.localPath + "bls_bible/static/profiles.json", "w+") as out:
            json.dump(data, out, indent=4)

        return self.getGroups()

    def getGroupsForAddProfile(self, path):
        content = ""
        if not os.path.exists(self.localPath + "bls_bible/static/profiles.json"):
            f = open(self.localPath + "bls_bible/static/profiles.json", "w+")
            profiles = []
            json.dump(profiles, f, indent=4)
            f.close()
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            data = json.load(f)
            f.close()
        except Exception as e:
            print("Failed to read profiles.json")
            print(e)
            return ""

        # Front load a 'add to new' item
        content += (
            '<li class="context-menu-item add-to-profile-item" onclick="addTTPToProfile(\''
            + str(markupsafe.escape(path))
            + "', 'new')\">Add To New Profile</li>"
        )
        for profile in data:
            content += (
                '<li class="context-menu-item add-to-profile-item" onclick="addTTPToProfile(\''
                + str(markupsafe.escape(path))
                + "', '"
                + str(markupsafe.escape(profile["id"]))
                + "')\">"
                + str(markupsafe.escape(profile["name"]))
                + "</li>"
            )
        return content

    def addTTPToProfile(self, filePath, profileId):
        # First, we need to get the relevant TTP info
        # As a reminder, TTP model object:
        """
        Structure of a TTP object:
        {
                'ttp_file': 'T1234.123.md',
                'ttp_major': 'Exploit the shit',
                'ttp_minor': 'Using magic'
        }
        """

        ttp_file = filePath.split("/")[-1]

        ttp_minor = ""
        ttp_phases = []

        # We need to grab the unique parent and child external IDs to get the TTP name from our MITRE data file
        ttp_tech = ttp_file.replace(".md", "").split("_")[0]
        ttp_parent = ttp_tech.split(".")[0]
        ttp_child = None
        if len(ttp_tech.split(".")) > 1:
            ttp_child = ttp_tech

        # TTP_Major: Use ttp_parent to find the attack-pattern in our MITRE data file
        ttp_parent_data = self.utils.get_ttp_content(ttp_parent)
        ttp_major = ttp_parent_data["name"]
        for phase in ttp_parent_data["phases"]:
            ttp_phases.append(phase["phase_name"])

        # TTP_Minor: Use ttp_child if we have it to find the attack-pattern
        # otherwise just return the empty ttp_minor value
        if ttp_child is not None:
            ttp_phases = []
            ttp_child_data = self.utils.get_ttp_content(ttp_child)
            ttp_minor = ttp_child_data["name"]
            for phase in ttp_child_data["phases"]:
                ttp_phases.append(phase["phase_name"])

        ttp = {
            "ttp_file": ttp_file,
            "ttp_major": ttp_major,
            "ttp_minor": ttp_minor,
            "ttp_phases": ttp_phases,
        }

        if profileId == "new":
            # Create profile and add TTP to it
            return self.createGroup("New Threat Profile", ttp)
        else:
            # Add TTP to existing profile
            f = open(self.localPath + "bls_bible/static/profiles.json")
            profiles = json.load(f)
            f.close()

            for profile in profiles:
                if profile["id"] == profileId:
                    profile["ttps"].append(ttp)
                    break

            with open(self.localPath + "bls_bible/static/profiles.json", "w+") as out:
                json.dump(profiles, out, indent=4)
            return self.getGroups()


class analyze_profiles:
    def __init__(self, localPath, safePath, localDeployment, parent):
        self.localPath = localPath
        self.safePath = safePath
        self.localDeployment = localDeployment
        self.parent = parent
        self.utils = utils(self.localPath)

    def get_matching_profiles(self, profileIds):
        f = open(self.localPath + "bls_bible/static/mitre/groups/apts.json")
        mitre_apts = json.load(f)
        f.close()

        f = open(self.localPath + "bls_bible/static/profiles.json")
        custom_profiles = json.load(f)
        f.close()

        selected_profiles = []
        for profileId in profileIds:
            for profile in custom_profiles:
                if profileId == profile["id"]:
                    selected_profiles.append(profile)
                    break

        results = {}

        for selected in selected_profiles:
            matches = []
            selected_techniques = []

            # We need to isolate the technique Ids from the file name
            for tech in selected["ttps"]:
                techId = tech["ttp_file"].replace(".md", "").split("_")[0]
                selected_techniques.append(techId)

            # Now we will check our isolated Ids against our custom profiles
            for custom in custom_profiles:
                if custom["id"] == selected["id"]:
                    continue
                custom_techniques = []
                counter = 0
                for cust_tech in custom["ttps"]:
                    custTechId = cust_tech["ttp_file"].replace(".md", "").split("_")[0]
                    custom_techniques.append(custTechId)
                for technique in selected_techniques:
                    if technique in custom_techniques:
                        counter += 1
                if len(custom_techniques) == 0:
                    percentage = "0%"
                else:
                    percentage = (
                        str(round(counter / len(custom_techniques) * 100, 2)) + "%"
                    )
                if counter == 0:
                    continue
                match = (custom["name"], counter, len(custom_techniques), percentage)
                # match = ("Custom Profile 1", 4, 16, "25%")
                matches.append(match)

            # We want to do the same for APTs identified by MITRE
            for apt in mitre_apts:
                apt_techniques = []
                counter = 0
                try:
                    for apt_technique in apt["techniques"]:
                        apt_techniques.append(apt_technique["techniqueID"])
                except Exception:
                    continue
                for technique in selected_techniques:
                    if technique in apt_techniques:
                        counter += 1
                if len(apt_techniques) == 0:
                    percentage = "0%"
                else:
                    percentage = (
                        str(round(counter / len(apt_techniques) * 100, 2)) + "%"
                    )
                if counter == 0:
                    continue
                match = (apt["name"], counter, len(apt_techniques), percentage)
                matches.append(match)

            # Add our matches for this selected threat profile
            matches.sort(key=lambda x: float(x[3].replace("%", "")), reverse=True)
            results[selected["id"]] = {"name": selected["name"], "matches": matches}

        return results

    def export_to_navigator(self, profileIds):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            profiles = json.load(f)
            f.close()
        except Exception:
            print("Error opening profiles.json")
            profiles = []
        selected_profiles = []
        for id in profileIds:
            for profile in profiles:
                if id == profile["id"]:
                    selected_profiles.append(profile)
                    break
        # We need to build our layer object
        layer_file = {}

        # Naming
        if len(selected_profiles) > 1:
            layer_file["name"] = "Combined Profiles"
        elif len(selected_profiles) == 1:
            layer_file["name"] = selected_profiles[0]["name"]
        else:
            layer_file["name"] = "No Profile Selected"

        # Versioning
        layer_file["versions"] = {"attack": "10", "navigator": "4.5.5", "layer": "4.3"}

        # Meta Info
        layer_file["domain"] = "enterprise-attack"
        if len(selected_profiles) > 1:
            description = selected_profiles[0]["name"]
            for profile in selected_profiles[1:]:
                description += "+" + profile["name"]
        elif len(selected_profiles) == 1:
            description = selected_profiles[0]["name"]
        else:
            description = ""
        layer_file["description"] = description
        layer_file["filters"] = {
            "platforms": [
                "Linux",
                "macOS",
                "Windows",
                "Azure AD",
                "Office 365",
                "SaaS",
                "IaaS",
                "Google Workspace",
                "PRE",
                "Network",
                "Containers",
            ]
        }
        layer_file["sorting"] = 0

        # Layout
        layer_file["layout"] = {
            "layout": "side",
            "aggregateFunction": "average",
            "showID": False,
            "showName": True,
            "showAggregateScores": False,
            "countUnscored": False,
        }

        layer_file["hideDisabled"] = False

        # Techniques
        techniques = []
        if len(selected_profiles) > 1:
            color = ""
        else:
            color = "#e60d0d"
        tech_dict = {}
        for profile in selected_profiles:
            for ttp in profile["ttps"]:
                techId = ttp["ttp_file"].replace(".md", "").split("_")[0]
                if techId in tech_dict:
                    tech_dict[techId]["score"] += 1
                else:
                    tech_dict[techId] = {
                        "techniqueID": techId,
                        "score": 1,
                        "tactic": ttp["ttp_phases"][0],
                        "color": color,
                        "comment": "",
                        "enabled": True,
                        "metadata": [],
                        "links": [],
                        "showSubtechniques": False,
                    }
        for tech in tech_dict:
            techniques.append(tech_dict[tech])
        layer_file["techniques"] = techniques

        # More Meta Info
        if len(selected_profiles) > 1:
            minValue = 1
            maxValue = len(selected_profiles)
        else:
            minValue = 0
            maxValue = 100
        layer_file["gradient"] = {
            "colors": ["#ff6666ff", "#ffe766ff", "#8ec843ff"],
            "minValue": minValue,
            "maxValue": maxValue,
        }
        layer_file["legendItems"] = []
        layer_file["metadata"] = []
        layer_file["links"] = []
        layer_file["showTacticRowBackground"] = False
        layer_file["tacticRowBackground"] = "#dddddd"
        layer_file["selectTechniquesAcrossTactics"] = True
        layer_file["selectSubtechniquesWithParent"] = False

        return layer_file

    def open_profile_in_tabs(self, profileIds):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            profiles = json.load(f)
            f.close()
        except Exception:
            profiles = []
        fileNames = []
        for pId in profileIds:
            for profile in profiles:
                if profile["id"] == pId:
                    for ttp in profile["ttps"]:
                        if ttp["ttp_file"] not in fileNames:
                            fileNames.append(ttp["ttp_file"])
                    break
        # We only have the actual file names, not the full path
        # We can use the fileList.json to retrieve them
        f = open(self.localPath + "bls_bible/static/fileList.json")
        fileList = json.load(f)
        f.close()

        filePaths = []
        for name in fileNames:
            for path in fileList:
                if name in path and path not in filePaths:
                    filePaths.append(path)
                    break
        if len(filePaths) > 0:
            dataStr = filePaths[0]
        else:
            dataStr = ""
        for filePath in filePaths[1:]:
            dataStr += "|" + filePath
        return dataStr

    def export_profile_to_pdf(self, profileIds):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            profiles = json.load(f)
            f.close()
        except Exception:
            profiles = []
        selected_profiles = []
        for pId in profileIds:
            for profile in profiles:
                if profile["id"] == pId:
                    selected_profiles.append(profile)
                    break
        html_doc = (
            "<html>"
            "<head>"
            '<script src="js/jquery-3.5.1.min.js" type="text/javascript"></script>'
            '<script src="js/bootstrap.bundle.min.js" type="text/javascript"></script>'
            '<script src="js/site.js" type="text/javascript"></script>'
            '<link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">'
            '<link href="css/site.css" media="print" rel="stylesheet" type="text/css">'
            '<link href="css/native.css" rel="stylesheet" type="text/css">'
            "</head>"
            "<body>"
        )
        fileNames = []
        for selected_profile in selected_profiles:
            for ttp in selected_profile["ttps"]:
                if ttp["ttp_file"] not in fileNames:
                    fileNames.append(ttp["ttp_file"])
        filePaths = []
        f = open(self.localPath + "bls_bible/static/fileList.json")
        fileList = json.load(f)
        f.close()
        for fileName in fileNames:
            for path in fileList:
                if fileName in path and path not in filePaths:
                    filePaths.append(path)
                    break
        for filePath in filePaths:
            html_doc += self.utils.get_content(
                filePath, self.safePath, self.localDeployment, self.parent
            )
            html_doc += '<p style="page-break-after: always;">&nbsp;</p>'

        html_doc += "</body></html>"

        soup = BeautifulSoup(html_doc, "html.parser")
        icons = soup.find_all("div", class_="material-icons")
        for icon in icons:
            icon.decompose()
        buttons = soup.find_all("button")
        for button in buttons:
            button.decompose()
        guide_ref_h3s = soup.find_all("h3", class_="guides-referencing-h3")
        for h3 in guide_ref_h3s:
            h3.decompose()
        guide_ref_uls = soup.find_all("ul", class_="guides-referencing-ul")
        for ul in guide_ref_uls:
            ul.decompose()

        syntax_css = self.localPath + "bls_bible/static/css/native.css"
        site_css = self.localPath + "bls_bible/static/css/site.css"
        print(self.localPath)
        html_weasy = HTML(string=str(soup), base_url="")
        pdf_weasy = html_weasy.write_pdf(stylesheets=[CSS(site_css), CSS(syntax_css)])

        return pdf_weasy


class CLI_manage_profiles:
    """
    Much of the CLI functionality has been removed.

    It may be finalized and included at some point, in which case
    this will be useful code.
    """

    def __init__(self, localPath):
        self.localPath = localPath
        self.utils = utils(self.localPath)
        self.threat_profile_file = self.localPath + "bls_bible/static/profiles2.json"

    def get_threat_profiles(self):

        try:

            f = open(self.threat_profile_file)
            data = json.load(f)
            f.close()

            return data

        except FileNotFoundError:

            print("Failed to read profiles2.json")

        except Exception as e:

            print(e)
            return ""

    def get_specific_threat_profile(self, threat_profile_id):
        file = open(self.threat_profile_file)
        json_data = json.load(file)

        for profile in json_data:

            if profile["id"] == threat_profile_id:

                return profile

    def createProfile_ETM(
        self, name="New Threat Profile", ttp=None, ETM_Scenario_id=None
    ):

        # load in the profiles data file

        try:

            f = open(self.threat_profile_file)
            data = json.load(f)
            f.close()

        except Exception as e:

            data = []
            print(e)

        # using seconds since epoch to generate ids for each threat profile
        # should hopefully avoid collisions
        id = hashlib.md5(str(time.time()).encode()).hexdigest()

        # Append to our data a new threat profile entry
        ttps = []
        if ttp:
            ttps.append(ttp)

        profile = {
            "id": id,
            "name": name,
            "ttps": ttps,
            "ETM_Scenario_id": ETM_Scenario_id,
        }

        """
		Structure of a profile object:
		{
			'id': "<md5 hash>",
			'name': "Threat Actor Delta",
			'ttps': [{ttp},{ttp}]
		}
		"""

        """
		Structure of a TTP object:
		{
			'ttp_file': 'T1234.123.md',
			'ttp_major': 'Exploit the shit',
			'ttp_minor': 'Using magic'
		}
		"""

        data.append(profile)

        try:

            with open(self.threat_profile_file, "w+") as out:
                json.dump(data, out, indent=4)

        except Exception as e:

            print("Failed to write to profiles2.json")
            print(e)

    def updateProfile_ETM(self, id, name=None, ETM_Scenario_id=None, ttps=None):

        data = self.get_threat_profiles()

        for profile in data:
            if profile["id"] == id:

                if ETM_Scenario_id == None:

                    ETM_Scenario_id = profile["ETM_Scenario_id"]

                if ttps == None:

                    ttps = profile["ttps"]

                else:
                    ttp_list = []
                    for ttp_id in ttps:
                        next_ttp = self.get_specific_ttp(ttp_id)
                        ttp_list.append(next_ttp)
                    ttps = ttp_list

                if name == None:

                    name = profile["name"]

                profile["name"] = name
                profile["ttps"] = ttps
                profile["ETM_Scenario_id"] = ETM_Scenario_id

                break

        with open(self.threat_profile_file, "w+") as out:
            json.dump(data, out, indent=4)
        """
		"""

    def TTP_lookup_in_MITRE(self, mitre_TTP_value):

        # Step one, get the relevant TTP info
        # As a reminder, TTP model object:
        """
        Structure of a TTP object:
        {
                'ttp_file': 'T1234.123.md',
                'ttp_major': 'Exploit the shit',
                'ttp_minor': 'Using magic'
        }
        """

        if (re.match("^T[0-9]{4}\.[0-9]{3}$", mitre_TTP_value)) or (
            re.match("^T[0-9]{4}$", mitre_TTP_value)
        ):
            ttp = mitre_TTP_value
            print("first ttp occurance")
        else:
            if re.match("^T[0-9]{4}/[0-9]{3}$", mitre_TTP_value):
                ttp = mitre_TTP_value.replace("/", ".")

            else:
                print(
                    'mitre TTP id format incorrect. Expecting either "T1234.001" or "T1234" format'
                )
                print(f"your format :\n{mitre_TTP_value}item")
                exit()

                # for TTPs with subtechniques:

        print("ttp = ", ttp)
        ttp_minor = ""
        ttp_phases = []

        # We need to grab the unique parent and child external IDs to get the TTP name from our MITRE data file
        # 		ttp_tech = ttp_file.replace('.md', '').split('_')[0]
        ttp_parent = ttp.split(".")[0]
        ttp_child = None
        if len(ttp.split(".")) > 1:
            ttp_child = ttp

        # TTP_Major: Use ttp_parent to find the attack-pattern in our MITRE data file
        ttp_parent_data = self.utils.get_ttp_content(ttp_parent)
        ttp_major = ttp_parent_data["name"]
        for phase in ttp_parent_data["phases"]:
            ttp_phases.append(phase["phase_name"])

        # TTP_Minor: Use ttp_child if we have it to find the attack-pattern
        # otherwise just return the empty ttp_minor value
        if ttp_child is not None:
            ttp_phases = []
            ttp_child_data = self.utils.get_ttp_content(ttp_child)
            ttp_minor = ttp_child_data["name"]
            for phase in ttp_child_data["phases"]:
                ttp_phases.append(phase["phase_name"])

        return ttp_phases, ttp_major, ttp_minor

    def addTTPToProfile_ETM(
        self, mitreId, profileId, threat_source, step_name, finding, ETM_Step_id=None
    ):

        ttp_phases, ttp_major, ttp_minor = self.TTP_lookup_in_MITRE(mitreId)

        # set the ttp_id in the same manor as threat profile id generation
        ttp_id = hashlib.md5(str(time.time()).encode()).hexdigest()

        if mitreId is None:

            pass

        else:

            if (re.match("^T[0-9]{4}\.[0-9]{3}$", mitreId)) or (
                re.match("^T[0-9]{4}$", mitreId)
            ):
                ttp = mitreId
                print("first ttp occurance")
            else:
                if re.match("^T[0-9]{4}/[0-9]{3}$", mitreId):
                    ttp = mitreId.replace("/", ".")
                    print("replaced ID: \n", ttp)

                else:
                    print(
                        'mitre TTP id format incorrect. Expecting either "T1234.001" or "T1234" format'
                    )
                    print(f"your format :\n{mitreId}item")
                    exit()

        ttp = {
            "ttp_id": ttp_id,
            "step_name": step_name,
            "ttp": ttp,
            "ttp_major": ttp_major,
            "ttp_minor": ttp_minor,
            "ttp_phases": ttp_phases,
            "finding": finding,
            "threat_source": threat_source,
            "ETM_Step_id": ETM_Step_id,
        }

        if profileId == "new":

            # Create profile and add TTP to it
            return self.createGroup("New Threat Profile", ttp)

        else:

            # Add TTP to existing profile

            # f = open(self.threat_profile_file)
            # profiles = json.load(f)
            # f.close()

            profiles = self.get_threat_profiles()

            for profile in profiles:

                if profile["id"] == profileId:
                    profile["ttps"].append(ttp)
                    break

            with open(self.threat_profile_file, "w+") as out:
                json.dump(profiles, out, indent=4)
            return self.get_threat_profiles()

    def get_specific_ttp(self, ttp_id):

        data = self.get_threat_profiles()
        for profile in data:

            for ttps in profile["ttps"]:

                if ttps["ttp_id"] == ttp_id:

                    return ttps

    def updateTTPs_ETM(
        self,
        ttp_id,
        step_name=None,
        ttp=None,
        finding=None,
        threat_source=None,
        ETM_Step_id=None,
    ):

        # this function is prepared to receive a list of TTP IDs, as opposed to some CLI options for singular/str submissions

        if ttp is None:
            pass
        else:
            if (re.match("^T[0-9]{4}\.[0-9]{3}$", ttp)) or (
                re.match("^T[0-9]{4}$", ttp)
            ):
                ttp = ttp
                print("first ttp occurance")
            else:
                if re.match("^T[0-9]{4}/[0-9]{3}$", ttp):
                    ttp = ttp.replace("/", ".")

                else:
                    print(
                        'mitre TTP id format incorrect. Expecting either "T1234.001" or "T1234" format'
                    )
                    print(f"your format :\n{ttp}item")
                    exit()

        data = self.get_threat_profiles()

        for profile in data:

            for ttps in profile["ttps"]:

                # 				for ttp_id in ttp_ids:

                if ttps["ttp_id"] == ttp_id:

                    # We matched.
                    matched_ttp = ttps

                    # For empty vars, update to be existing values of the matched_ttp

                    if step_name == None:

                        step_name = matched_ttp["step_name"]

                    if ttp == None:

                        ttp = matched_ttp["ttp"]
                        ttp_phases = matched_ttp["ttp_phases"]
                        ttp_major = matched_ttp["ttp_major"]
                        ttp_minor = matched_ttp["ttp_minor"]

                    # in this particular case, if the user submitted a new TTP value, several related values can be dynamically updated.

                    else:

                        ttp_phases, ttp_major, ttp_minor = self.TTP_lookup_in_MITRE(ttp)

                    if finding == None:

                        finding = matched_ttp["finding"]

                    if threat_source == None:

                        threat_source = matched_ttp["threat_source"]

                    if ETM_Step_id == None:

                        ETM_Step_id = matched_ttp["ETM_Step_id"]

                    # perform update actions

                    matched_ttp["step_name"] = step_name
                    matched_ttp["ttp"] = ttp
                    matched_ttp["finding"] = finding
                    matched_ttp["threat_source"] = threat_source
                    matched_ttp["ETM_Step_id"] = ETM_Step_id
                    matched_ttp["ttp_major"] = ttp_major
                    matched_ttp["ttp_minor"] = ttp_minor
                    matched_ttp["ttp_phases"] = ttp_phases

        with open(self.threat_profile_file, "w+") as out:
            json.dump(data, out, indent=4)

    def deleteProfile_ETM(self, threat_profile_id):
        data = self.get_threat_profiles()
        print(f"data: {data}")

        for profile in data:
            print(f"profile: {profile}")
            print(f"profile['id']: {profile['id']}")
            if profile["id"] == threat_profile_id:
                data.remove(profile)
                break

        with open(self.threat_profile_file, "w+") as out:
            json.dump(data, out, indent=4)

        return self.get_threat_profiles()

    def deleteProfileTTP_ETM(self, ttp_id):

        data = self.get_threat_profiles()

        for profile in data:

            for ttps in profile["ttps"]:

                if ttps["ttp_id"] == ttp_id:
                    profile["ttps"].remove(ttps)
                    break

        with open(self.threat_profile_file, "w+") as out:
            json.dump(data, out, indent=4)

        return self.get_threat_profiles()
