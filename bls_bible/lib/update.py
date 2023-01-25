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
# update.py

import json
import os
import requests
import re
from bs4 import BeautifulSoup
import logging
import git
from bls_bible.lib.utils import utils


class git_update:
    def __init__(self, token, domain, repo, id, branch, parent, localPath):
        self.token = token
        self.domain = domain
        self.repo = repo
        self.projectId = id
        self.branch = branch
        self.parent = parent
        self.localPath = localPath

    def git_submodule_pull(self):  # git submodule update --init --recursive --remote
        print("entered git submodule pull")
        print("localPath var: ", self.localPath)
        repo = git.Repo(self.localPath)
        print("repo variable: ", repo)

        for submodule in repo.submodules:
            print("submodule of repo.submodules: ", submodule)
            try:
                submodule.update(init=True, recursive=True)
            except Exception as e:
                print(e)
        output = repo.git.submodule("update", "--init", "--recursive", "--remote")

        return output

    def git_repo_update(self):
        git_update_command = git.cmd.Git(self.localPath)
        print("Git Update Command: ", git_update_command)

    def git_assessalonians_pull(self, Assessalonians_Repo, assessmentParent):

        clone_assess = git.Repo.clone_from(Assessalonians_Repo, assessmentParent)

        return clone_assess


class update:
    def __init__(
        self,
        source,
        redParent,
        blueParent,
        purpleParent,
        apocryphaParent,
        assessmentParent,
        localPath,
        ttpParent,
        localDeployment,
        parent,
        safePath,
        id,
        branch,
        domain,
        token,
    ):
        self.source = source  # whoever calls this class must provide the "source"
        self.redParent = redParent
        self.blueParent = blueParent
        self.purpleParent = purpleParent
        self.apocryphaParent = apocryphaParent
        self.assessmentParent = assessmentParent
        self.localPath = localPath
        self.ttpParent = ttpParent
        self.localDeployment = localDeployment
        self.parent = parent
        self.projectId = id
        self.branch = branch
        self.domain = domain
        self.token = token
        self.safePath = safePath
        self.utils = utils(self.localPath)

    def update_json_file(self):
        # Red:
        content = ""
        content += '{"children": ['
        content += self.utils.parse_dir_local(self.localPath + self.redParent)
        content += '],"name": "Redvelations","type": "folder"}'
        json_object = json.loads(content)
        json_formatted_str = json.dumps(json_object, indent=2)
        try:
            with open(self.localPath + "bls_bible/static/red.json", "w+") as f:
                f.write(json_formatted_str)
        except Exception as e:
            print(e)
            print(os.getcwd())
            print("JSON failed to load")

        # Blue:
        content = ""
        content += '{"children": ['
        content += self.utils.parse_dir_local(self.localPath + self.blueParent)
        content += '],"name": "Blue Testament","type": "folder"}'
        json_object = json.loads(content)
        json_formatted_str = json.dumps(json_object, indent=2)
        try:
            with open(self.localPath + "bls_bible/static/blue.json", "w+") as f:
                f.write(json_formatted_str)
        except Exception:
            logging.error(
                "Failed to open " + self.localPath + " bls_bible/static/blue.json"
            )

        # Purple:
        if os.path.exists(self.localPath + self.purpleParent):
            content = ""
            content += '{"children": ['
            content += self.utils.parse_dir_local(self.localPath + self.purpleParent)
            content += '],"name": "Purplippians","type": "folder"}'
            json_object = json.loads(content)
            json_formatted_str = json.dumps(json_object, indent=2)
            try:
                with open(self.localPath + "bls_bible/static/purple.json", "w+") as f:
                    f.write(json_formatted_str)
            except Exception:
                logging.error(
                    "Failed to open " + self.localPath + "bls_bible/static/purple.json"
                )
        else:
            content = ""
            try:
                f = open("bls_bible/static/purple.json", "w+")
                f.write(content)
            finally:
                f.close()

        # Assessments:
        if os.path.exists(self.localPath + self.assessmentParent):
            content = ""
            content += '{"children": ['
            content += self.utils.parse_dir_local(
                self.localPath + self.assessmentParent
            )
            content += '],"name": "Assessalonians","type": "folder"}'
            json_object = json.loads(content)
            json_formatted_str = json.dumps(json_object, indent=2)
            try:
                f = open("bls_bible/static/assessment.json", "w+")
                f.write(json_formatted_str)
            finally:
                f.close()
        else:
            content = ""
            try:
                with open(
                    self.localPath + "bls_bible/static/assessment.json", "w+"
                ) as f:
                    f.write(content)
            except Exception:
                logging.error(
                    "Failed to open "
                    + self.localPath
                    + "bls_bible/static/assessment.json"
                )

        # Apocrypha
        if os.path.exists(self.localPath + self.apocryphaParent):
            content = ""
            content += '{"children": ['
            content += self.utils.parse_dir_local(self.localPath + self.apocryphaParent)
            content += '],"name": "Apocrypha","type": "folder"}'
            json_object = json.loads(content)
            json_formatted_str = json.dumps(json_object, indent=2)
            try:
                with open(
                    self.localPath + "bls_bible/static/apocrypha.json", "w+"
                ) as f:
                    f.write(json_formatted_str)
            except Exception:
                logging.error(
                    "Failed to open "
                    + self.localPath
                    + "bls_bible/static/aprocrypha.json"
                )
        else:
            content = ""
            try:
                f = open("bls_bible/static/apocrypha.json", "w+")
                f.write(content)
            finally:
                f.close()

        # TTPs:

        # We are going to craft this data file in accordance with the other two
        # We will do this by creating the root object under which each of the MITRE phases will reside
        ttp_data = {"children": [], "name": "TTP", "type": "folder"}

        # Next we need to create the MITRE phases and append them to the root object's children
        # a phase object has the tactic externalID, name and description
        # additionally, a phase object will have children (techniques) a type (folder)
        f = open(self.localPath + "bls_bible/static/mitre/enterprise-attack.json")
        mitre = json.load(f)
        f.close()
        mitre_phases = {}
        for obj in mitre["objects"]:
            if obj["type"] == "x-mitre-tactic":
                phase = {
                    "children": [],
                    "name": obj["external_references"][0]["external_id"]
                    + " "
                    + obj["name"],
                    "type": "folder",
                    "externalId": obj["external_references"][0]["external_id"],
                    "description": obj["description"],
                    "short_name": obj["x_mitre_shortname"],
                }
                ttp_data["children"].append(phase)
                mitre_phases[phase["short_name"]] = phase

        # Now we need to iterate through the TTP files we have, take the technique ID,
        # check which phases it belongs to, and add it to those phases children

        # While we are here, we can go ahead and index our TTP files as well:
        # {
        #   '#@Txxxx.yyy': [
        # 	   '/path/to/Txxxx.yyy.md',
        # 	   '/path/to/Txxxx.md',
        # 	   '/path/to/Txxxx_Thing.md',
        # 	   '/path/to/Txxxx.yyy_thing.md'
        #   ],
        #   ...
        # }

        ordering_hack = {
            0: "reconnaissance",
            1: "resource-development",
            2: "initial-access",
            3: "execution",
            4: "persistence",
            5: "privilege-escalation",
            6: "defense-evasion",
            7: "credential-access",
            8: "discovery",
            9: "lateral-movement",
            10: "collection",
            11: "command-and-control",
            12: "exfiltration",
            13: "impact",
        }

        ttp_dir = self.localPath + "Data/TTP/"
        ttp_arr = []
        revoked_arr = []
        for (path, dirs, files) in os.walk(ttp_dir):
            for file in files:
                ttp_is_sub = False
                ttp_sub_title = ""
                ttp_parent_title = ""
                ttp_phases = []
                ttp_platforms = []
                for obj in mitre["objects"]:
                    if obj["type"] == "attack-pattern":
                        try:
                            if obj["revoked"]:
                                if obj not in revoked_arr:
                                    revoked_arr.append(obj)
                                continue
                        except Exception:
                            None
                        if (
                            obj["external_references"][0]["external_id"]
                            == file.replace(".md", "").split("_")[0]
                        ):
                            for entry in obj["kill_chain_phases"]:
                                ttp_phases.append(entry["phase_name"])
                            for platform in obj["x_mitre_platforms"]:
                                ttp_platforms.append(platform.lower())
                            try:
                                if obj["x_mitre_is_subtechnique"]:
                                    ttp_is_sub = True
                            except KeyError:
                                ttp_is_sub = False
                            if ttp_is_sub:
                                ttp_sub_title = obj["name"]
                                for obj2 in mitre["objects"]:
                                    if (
                                        obj2["type"] == "attack-pattern"
                                        and obj2["external_references"][0][
                                            "external_id"
                                        ]
                                        == file.split(".")[0]
                                    ):
                                        ttp_parent_title = obj2["name"]
                                        break
                            else:
                                ttp_parent_title = obj["name"]
                            break
                ttp = {
                    "full_path": os.path.join(path, file),
                    "file_name": file,
                    "technique": file.replace(".md", "").split("_")[0],
                    "tag": "#@" + file.replace(".md", "").split("_")[0],
                    "phases": ttp_phases,
                    "platforms": ttp_platforms,
                    "is_sub": ttp_is_sub,
                    "parent_title": ttp_parent_title,
                    "sub_title": ttp_sub_title,
                }
                ttp_arr.append(ttp)

        # We should have ample data now to do what we need to (and more)

        # Reverse Referencing of TTPs from Guides
        # Initialize to have one dict entry of 'none' for guides that do not reference a TTP
        reverse_references = {
            "none": {
                "platforms": ["none"],
                "phases": [],
                "full_path": "",
                "file_name": "",
                "is_sub": False,
                "parent_title": "",
                "sub_title": "",
                "guides_referencing": [],
            }
        }
        # We will now create a dict entry for each TTP we have in /Data/TTP
        # Dict entries require knowledge of the platforms associated with a TTP
        # The entries will be initialized with empty guides_referencing lists
        for ttp in ttp_arr:
            rev_ref_phases = []
            for ttp_phase in ttp["phases"]:
                rev_ref_phases.append(mitre_phases[ttp_phase])
            # reverse_references[ttp['technique']] = {
            reverse_references[ttp["file_name"].replace(".md", "")] = {
                "platforms": ttp["platforms"],
                "phases": rev_ref_phases,
                "full_path": ttp["full_path"].replace(self.localPath + "Data/", ""),
                "file_name": ttp["file_name"],
                "is_sub": ttp["is_sub"],
                "parent_title": ttp["parent_title"],
                "sub_title": ttp["sub_title"],
                "guides_referencing": [],
            }
        # We will finish this in another function. We need the use of fileIndexer to make this as easy as possible
        # Kick out our structure to a json file for later user
        try:
            f = open(self.localPath + "bls_bible/static/reverse_reference.json", "w+")
            json.dump(reverse_references, f)
            f.close()
        except Exception as e:
            print("Problem writing to reverse_reference.json")
            print(e)

        # Kick out the revoked techniques from MITRE
        try:
            f = open(self.localPath + "bls_bible/static/revoked.json", "w+")
            json.dump(revoked_arr, f)
            f.close()
        except Exception as e:
            print("Problem writing to revoked.json")
            print(e)

        # Tag Search Indexing:
        # The following commented lines were causing old/outdated data to remain intact when forcing a
        # data update
        # Solution is to always create a new searchIndex
        # try:
        # 	f = open(self.localPath + 'bls_bible/static/searchIndex.json')
        # 	searchIndex = json.load(f)
        # 	f.close()
        # except:
        searchIndex = {}

        for ttp in ttp_arr:
            if ttp["tag"].upper() not in searchIndex:
                searchIndex[ttp["tag"].upper()] = [ttp["full_path"]]
            else:
                searchIndex[ttp["tag"].upper()].append(ttp["full_path"])
        with open(self.localPath + "bls_bible/static/searchIndex.json", "w+") as out:
            json.dump(searchIndex, out)

        # UI Data File - Add techniques to appropriate phases:
        for ttp in ttp_arr:
            new_file = {
                "name": ttp["file_name"].replace("_", " "),
                "type": "url",
                "url": "getContent('" + ttp["full_path"] + "')",
            }
            for ttp_phase in ttp["phases"]:
                for phase in ttp_data["children"]:
                    if phase["short_name"] == ttp_phase:
                        if ttp["is_sub"]:

                            # Since we are a sub technique, we need to verify that
                            # 1. The parent folder exists
                            #   1.1 If it does not, create the child folder
                            #   1.2 place our new file in the new child folder
                            #   1.3 create the parent folder with the new child folder
                            #   1.4 add the parent folder to the phase
                            #   1.5 break out of loop
                            # 2. The child folder exists
                            #   2.1 If it does not, create the folder and place our file within it
                            #   2.2 Put the folder in its parent
                            #   2.3 break

                            parentExists = False
                            for parent in phase["children"]:
                                if (
                                    parent["type"] == "folder"
                                    and parent["name"]
                                    == ttp["technique"].split(".")[0]
                                    + " "
                                    + ttp["parent_title"]
                                ):
                                    parentExists = True
                                    # Check to see if child folder already exists
                                    childExists = False
                                    for child in parent["children"]:
                                        if (
                                            child["type"] == "folder"
                                            and child["name"]
                                            == ttp["technique"].split(".")[1]
                                            + " "
                                            + ttp["sub_title"]
                                        ):
                                            # Cool, parent and child folders exist, put file in this folder
                                            childExists = True
                                            child["children"].append(new_file)
                                            break
                                    if not childExists:
                                        # Child folder didn't exist, we need to create it with our new file inside
                                        new_child = {
                                            "children": [new_file],
                                            "name": ttp["technique"].split(".")[1]
                                            + " "
                                            + ttp["sub_title"],
                                            "type": "folder",
                                        }
                                        # Add the new child folder to its parent
                                        parent["children"].append(new_child)
                                        break
                                    break
                            if not parentExists:
                                # Parent folder didn't exist, we need to create it, the child folder within, and the
                                # new file within the child folder
                                new_parent = {
                                    "children": [
                                        {
                                            "children": [new_file],
                                            "name": ttp["technique"].split(".")[1]
                                            + " "
                                            + ttp["sub_title"],
                                            "type": "folder",
                                        }
                                    ],
                                    "name": ttp["technique"].split(".")[0]
                                    + " "
                                    + ttp["parent_title"],
                                    "type": "folder",
                                }
                                phase["children"].append(new_parent)
                        else:

                            # Since we are not a sub technique, we only need to verify that
                            # 1. The parent folder exists
                            #   1.1 If it does not, create the folder with the new file in it
                            #   1.2 break

                            parentExists = False
                            for parent in phase["children"]:
                                if (
                                    parent["type"] == "folder"
                                    and parent["name"]
                                    == ttp["technique"] + " " + ttp["parent_title"]
                                ):
                                    parentExists = True
                                    parent["children"].append(new_file)
                                    break
                            if not parentExists:
                                # Parent folder didn't exist, we need to create it and the file within it
                                new_parent = {
                                    "children": [new_file],
                                    "name": ttp["technique"]
                                    + " "
                                    + ttp["parent_title"],
                                    "type": "folder",
                                }
                                # Add the parent to the phase
                                phase["children"].append(new_parent)
                        break
        # Holy hell we made it
        # We now need to sort our phases
        ttp_data_sorted = {"children": [], "name": "TTP", "type": "folder"}

        for sorted_phase in ordering_hack:
            for phase in ttp_data["children"]:
                if phase["short_name"] == ordering_hack[sorted_phase]:
                    ttp_data_sorted["children"].append(phase)
                    break
        ttp_data = ttp_data_sorted
        # Our phases are sorted.

        # We need to now sort our techniques
        # Parent techniques are sorted alphabetically
        # Sub techniques are sorted numerically
        # Files are sorted above folders
        for phase in ttp_data["children"]:
            phase["children"].sort(
                key=lambda tech: " ".join(tech["name"].split(" ")[1:])
            )
            for parent_tech in phase["children"]:
                # First we make sure our 'folder' files are sorted by their technique id
                parent_tech["children"].sort(key=lambda kid: kid["name"].split(" ")[0])
                # Second we make sure our 'url' files come before our 'folder' files
                parent_tech["children"].sort(key=lambda kid: kid["type"], reverse=True)

        # Write out our ttp_data file
        with open(self.localPath + "bls_bible/static/ttp.json", "w+") as out:
            json.dump(ttp_data, out)

        # Find missing technique files:
        f = open(self.localPath + "bls_bible/static/searchIndex.json")
        searchIndex = json.load(f)
        f.close()
        tech_arr = {}
        for obj in mitre["objects"]:
            if obj["type"] == "attack-pattern":
                try:
                    if obj["revoked"]:
                        continue
                except Exception:
                    None
                ttp_is_sub = False
                ttp_sub_title = ""
                ttp_parent_title = ""
                try:
                    if obj["x_mitre_is_subtechnique"]:
                        ttp_is_sub = True
                except Exception:
                    ttp_is_sub = False
                if ttp_is_sub:
                    ttp_sub_title = obj["name"]
                    for obj2 in mitre["objects"]:
                        if (
                            obj2["type"] == "attack-pattern"
                            and obj2["external_references"][0]["external_id"]
                            == obj["external_references"][0]["external_id"].split(".")[
                                0
                            ]
                        ):
                            ttp_parent_title = obj2["name"]
                            break
                else:
                    ttp_parent_title = obj["name"]
                tech_arr[obj["external_references"][0]["external_id"]] = {
                    "name": obj["name"],
                    "parent_title": ttp_parent_title,
                    "sub_title": ttp_sub_title,
                }
        for ttp in ttp_arr:
            try:
                del tech_arr[ttp["technique"]]
            except Exception as e:
                print(e)
                continue
        with open(
            self.localPath + "bls_bible/static/missing_techniques.json", "w+"
        ) as out:
            json.dump(tech_arr, out)

        return True

    def get_reverse_references(self):
        # Lets grab our model
        f = open(self.localPath + "bls_bible/static/reverse_reference.json")
        reverse_references = json.load(f)
        f.close()

        # Lets grab the file list
        f = open(self.localPath + "bls_bible/static/fileList.json")
        file_list = json.load(f)
        f.close()

        f = open(self.localPath + "bls_bible/static/searchIndex.json")
        searchIndex = json.load(f)
        f.close()

        for file in file_list:
            if self.localPath + "Data/TTP" in file:
                # Skipping TTP files
                continue
            tag = ""
            if "/Active_Directory/" in file:
                tag = "#@ACTIVEDIRECTORY"
            elif "/Windows/" in file:
                tag = "#@WINDOWS"
            elif "/MacOS/" in file:
                tag = "#@MACOS"
            elif "/Linux/" in file:
                tag = "#@LINUX"
            elif "/Cloud/Azure/" in file:
                tag = "#@AZURE"
            elif "/Cloud/Google/" in file:
                tag = "#@GCP"
            elif "/Cloud/O365/" in file:
                tag = "#@O365"
            elif "/Cloud/" in file:
                tag = "#@IAAS"
            elif "/OSINT_and_Prep/" in file:
                tag = "#@PRE"
            elif "/Network/" in file:
                tag = "#@NETWORK"
            elif "/Java/" in file:
                tag = "#@JAVA"

            # Automatically tagging relevant guides in searchIndex.json
            if tag not in searchIndex and tag != "":
                searchIndex[tag] = [file]
            elif tag != "" and file not in searchIndex[tag]:
                searchIndex[tag].append(file)

            f = open(file)
            try:
                lines = f.readlines()
            except UnicodeDecodeError:
                # When reading binary files, we throw an error obviously
                continue
            f.close()
            pattern = r"\/T[0-9]{4}[^\/]*\.md"
            found_reference = False
            for line in lines:
                # Do some regex to find if a technique is being linked to
                matches = re.findall(pattern, line)
                if matches:
                    found_reference = True
                for match in matches:
                    technique = match.replace(".md", "").replace("/", "")
                    guide_os = ""
                    guide_color = ""
                    tag = ""
                    if "/Blue_Testament/" in file:
                        guide_color = "blue"
                    elif "/Redvelations/" in file:
                        guide_color = "red"
                    if "/Active_Directory/" in file:
                        guide_os = "Windows"
                    elif "/Windows/" in file:
                        guide_os = "Windows"
                    elif "/MacOS/" in file:
                        guide_os = "macOS"
                    elif "/Linux/" in file:
                        guide_os = "Linux"
                    elif "/Cloud/Azure/" in file:
                        guide_os = "Azure AD"
                    elif "/Cloud/Google/" in file:
                        guide_os = "Google Workspace"
                    elif "/Cloud/O365/" in file:
                        guide_os = "Office 365"
                    elif "/Cloud/" in file:
                        guide_os = "IaaS"
                    elif "/OSINT_and_Prep/" in file:
                        guide_os = "PRE"
                    elif "/Network/" in file:
                        guide_os = "Network"

                    reverse_references[technique]["guides_referencing"].append(
                        {
                            "guide_name": file.split("/")[-1].replace(".md", ""),
                            "guide_path": file,
                            "guide_os": guide_os.lower(),
                            "guide_color": guide_color,
                        }
                    )
            # If we are here and have not found references, then we need to add
            # this guide to our 'none' entry
            if not found_reference:
                guide_color = ""
                guide_os = ""
                if "/Blue_Testament/" in file:
                    guide_color = "blue"
                elif "/Redvelations/" in file:
                    guide_color = "red"
                if "/Active_Directory/" in file or "/Windows/" in file:
                    guide_os = "Windows"
                elif "/MacOS/" in file:
                    guide_os = "macOS"
                elif "/Linux/" in file:
                    guide_os = "Linux"
                reverse_references["none"]["guides_referencing"].append(
                    {
                        "guide_name": file.split("/")[-1].replace(".md", ""),
                        "guide_path": file,
                        "guide_os": guide_os.lower(),
                        "guide_color": guide_color,
                    }
                )
        # We've gone through all of our files
        # Time to kick out to our reverse_reference.json file
        f = open(self.localPath + "bls_bible/static/reverse_reference.json", "w+")
        json.dump(reverse_references, f)
        f.close()

        # And also kick out to our searchIndex.json file
        f = open(self.localPath + "bls_bible/static/searchIndex.json", "w+")
        json.dump(searchIndex, f)
        f.close()
        return True


class mitre_update:
    def __init__(self, localPath):
        self.localPath = localPath

    def get_apts(self):
        try:
            f = open(self.localPath + "bls_bible/static/profiles.json")
            profiles = json.load(f)
            f.close()
        except Exception:
            profiles = []

        if len(profiles) > 0:
            content = '<span class="apt-filter-sub-heading">CUSTOM</span>'
        else:
            content = ""
        for profile in profiles:
            aptName = profile["name"]
            aptId = profile["id"]
            content += '<div class="form-check">'
            content += (
                '<input onchange="toggleAptUiFilter(this)" class="form-check-input apt-checkbox" '
                'type="checkbox" value="' + aptId + '" id="' + aptId + '-APT">'
            )
            content += '<label for="' + aptId + '-APT">' + aptName + "</label>"
            content += "</div>"

        groupPath = self.localPath + "bls_bible/static/mitre/groups/apts.json"
        f = open(groupPath)
        data = json.load(f)
        f.close()

        content += '<span class="apt-filter-sub-heading">MITRE</span>'
        for group in data:
            if not group:
                continue
            aptName = group["name"].split("(")[0][:-1]
            aptId = group["name"].split(" ")[-1].replace("(", "").replace(")", "")
            content += '<div class="form-check">'
            content += (
                '<input onchange="toggleAptUiFilter(this)" class="form-check-input apt-checkbox" '
                'type="checkbox" value="' + aptId + '" id="' + aptId + '-APT">'
            )
            content += '<label for="' + aptId + '-APT">' + aptName + "</label>"
            content += "</div>"

        return content

    def crawlGroups(self):
        r = requests.get("https://attack.mitre.org/groups/")
        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        links = soup.find_all("a", {"href": re.compile("/groups/G.*")})
        links = list(links)
        groups = {}
        for link in links:
            split1 = str(link).split(">")
            split2 = split1[0].split("/")
            split3 = split1[1].split("<")
            # ID of APT: print(split2[2].strip("\""))
            # Name of APT: print(split3[0].strip())
            groups[split2[2].strip('"')] = split3[0].strip(" ")
        convert = lambda text: int(text) if text.isdigit() else text.upper()
        alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
        groupsSorted = sorted(groups.values(), key=alphanum_key)
        groupsDictSorted = {}
        for value in groupsSorted:
            groupsDictSorted[
                list(groups.keys())[list(groups.values()).index(value)]
            ] = value
        return groupsDictSorted

    def crawlJson(self, id):
        url = (
            "https://attack.mitre.org/groups/"
            + id
            + "/"
            + id
            + "-enterprise-layer.json"
        )
        r = requests.get(url)
        try:
            data = json.loads(r.text)
        except Exception:
            url = (
                "https://attack.mitre.org/groups/"
                + id
                + "/"
                + id
                + "-mobile-layer.json"
            )
            r = requests.get(url)
            try:
                data = json.loads(r.text)
            except Exception as e:
                print(e)
                print("Group crawled: " + id)
                return
        techniques = []
        for item in data["techniques"]:
            for key, value in item.items():
                if key == "techniqueID":
                    techniques.append(value)
                    break
        return techniques

    def crawlJsonForDownload(self, id):
        url = (
            "https://attack.mitre.org/groups/"
            + id
            + "/"
            + id
            + "-enterprise-layer.json"
        )
        r = requests.get(url)
        try:
            data = json.loads(r.text)
        except Exception:
            url = (
                "https://attack.mitre.org/groups/"
                + id
                + "/"
                + id
                + "-mobile-layer.json"
            )
            r = requests.get(url)
            try:
                data = json.loads(r.text)
            except Exception as e:
                print(e)
                print("Group crawled: " + id)
                return
        return data

    def downloadMitreGroups(self):
        groupsCrawled = self.crawlGroups()
        toJson = []
        for key in groupsCrawled.keys():
            toJson.append(self.crawlJsonForDownload(key))
        prefix = self.localPath + "bls_bible/static/mitre/groups/"
        with open(prefix + "apts.json", "w+") as out:
            json.dump(toJson, out)
        return str(toJson)

    def downloadLatestAttack(self):
        r = requests.get(
            "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        )
        data = json.loads(r.text)
        attackPath = self.localPath + "bls_bible/static/mitre/enterprise-attack.json"
        with open(attackPath, "w+") as out:
            json.dump(data, out)
        return str(data)
