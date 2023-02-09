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
# utils.py

import json
import os
import markdown2
import re
import markupsafe
import yaml
import logging
from bs4 import BeautifulSoup


class utils:
    def __init__(self, localPath):
        self.localPath = localPath

    def parse_dir_local(self, parent):
        top = parent
        if top[-1] != "/":
            top += "/"
        content = ""
        fileArr = []
        dirArr = []
        for (path, dirs, files) in os.walk(top):
            fileArr.extend(files)
            fileArr = sorted(fileArr)
            dirArr.extend(dirs)
            dirArr = sorted(dirArr)
            break
        for idx, folder in enumerate(dirArr):
            content += '{"children": ['
            content += self.parse_dir_local(top + folder)
            if idx < len(dirArr) - 1 or len(fileArr) > 0:
                content += (
                    '],"name": "'
                    + folder.replace("_", " ").replace("\\", "\\\\")
                    + '","type": "folder"},'
                )
            else:
                content += (
                    '],"name": "'
                    + folder.replace("_", " ").replace("\\", "\\\\")
                    + '","type": "folder"}'
                )
        for idx, file in enumerate(fileArr):
            if idx < len(fileArr) - 1:
                content += (
                    '{"name": "'
                    + file.replace("_", " ").replace("\\", "\\\\")
                    + '","type": "url","url": "'
                    + "getContent('"
                    + top
                    + file
                    + "')"
                    + '"},'
                )
            else:
                content += (
                    '{"name": "'
                    + file.replace("_", " ").replace("\\", "\\\\")
                    + '","type": "url","url": "'
                    + "getContent('"
                    + top
                    + file
                    + "')"
                    + '"}'
                )
        return content

    def get_ttp_content(self, file):
        jsonPath = self.localPath + "bls_bible/static/mitre/enterprise-attack.json"
        f = open(jsonPath)
        mitre = json.load(f)["objects"]
        f.close()
        phases = []
        platforms = []
        name = ""
        description = ""
        detection = ""
        mitreSource = []
        allSources = []
        externalId = file.split("_")[0]
        found = False
        for entry in mitre:
            if entry["type"] == "attack-pattern":
                if entry["external_references"]:
                    for ref in entry["external_references"]:
                        if ref["source_name"] == "mitre-attack":
                            if ref["external_id"] == externalId:
                                mitreSource = ref
                                found = True
                                break
            if found:
                try:
                    phases = entry["kill_chain_phases"]
                except Exception:
                    phases = "none"
                try:
                    platforms = entry["x_mitre_platforms"]
                except Exception:
                    platforms = "none"
                name = entry["name"]
                try:
                    description = entry["description"]
                except Exception:
                    description = "none"
                try:
                    detection = entry["x_mitre_detection"]
                except Exception:
                    detection = "none"
                allSources = entry["external_references"]
                break
        if not found:
            return False
        ttp = {
            "phases": phases,
            "platforms": platforms,
            "name": name,
            "description": description,
            "detection": detection,
            "mitreSource": mitreSource,
            "allSources": allSources,
        }
        return ttp

    def getUrls(self, data, urls):
        try:
            if data["type"] == "url":
                path = data["url"].split("'")[1]
                urls.append(path)
            elif data["type"] == "folder":
                for child in data["children"]:
                    self.getUrls(child, urls)
        except KeyError:
            logging.debug("Attempted to execute utils.getUrls with an empty dataset")
            pass
        return urls

    def get_content(self, path, safePath, localDeployment, parent):
        if os.path.commonprefix(
            (os.path.realpath(path), os.path.realpath(safePath))
        ) != os.path.realpath(safePath):
            return "<h1>Stop trying to look at my private parts :P</h1>"

        fileContent = ""
        guideRefcontent = ""
        # Set up your modal parts

        # Header
        content = '<div class="modal-header">'
        content += '<div class="row">'
        content += "<div onclick=\"$('#file-content').modal('hide');\" class=\"material-icons col-sm-1\">cancel</div>"
        content += '<div onclick="history.back();" class="material-icons col-sm-1">arrow_back</div>'
        content += '<div onclick="history.forward();" class="material-icons col-sm-1">arrow_forward</div>'
        content += (
            "<div onclick=\"openInNewTab('"
            + str(markupsafe.escape(path))
            + '\')" class="material-icons col-sm-1">open_in_new</div>'
        )
        if localDeployment:
            content += (
                '<div id="file-edit-btn" onclick="editFile(\''
                + str(markupsafe.escape(path))
                + '\')" class="material-icons col-sm-1">edit</div>'
            )
            content += (
                '<div id="file-save-btn" onclick="saveFile(\''
                + str(markupsafe.escape(path))
                + '\')" style="display:none;" class="material-icons col-sm-1">save</div>'
            )
            content += (
                '<div id="file-undo-btn" onclick="cancelEditFile(\''
                + str(markupsafe.escape(path))
                + '\')" style="display:none;"'
                ' class="material-icons col-sm-1">undo</div>'
            )
            content += '<div class="col-sm-5"></div>'
        else:
            content += '<div class="col-sm-8"></div>'
        content += '</div><div class="row">'
        content += (
            '<span class="col-sm-12 file-content-header"><h4><b>'
            + str(markupsafe.escape(path.replace(safePath, "/")))
            + "</b></h4></span>"
        )
        content += "</div></div>"
        finalContent = content
        finalContent += '<div class="row">'

        # Body
        content = '<div class="modal-body" id="file-content-body">'

        # Inject MITRE data if file is TTP
        if len(os.path.basename(path).split(".")) > 2:
            filename = (
                os.path.basename(path).split(".")[0]
                + "."
                + os.path.basename(path).split(".")[1]
            )
        else:
            filename = os.path.basename(path).split(".")[0]
        if re.search("(T[0-9]{4}\.{1}[0-9]{3}|T[0-9]{4})", filename):
            ttp = self.get_ttp_content(filename)

            # Get the guides that reference this technique
            obj = self.get_guides_referencing_technique(filename)
            files = []
            for guide in obj["guides_referencing"]:
                files.append(
                    {
                        "name": guide["guide_path"].split("/")[-2].replace("_", " ")
                        + "/"
                        + guide["guide_name"].replace("_", " "),
                        "path": guide["guide_path"],
                    }
                )

            # Name
            content += '<a target="_blank" href="' + ttp["mitreSource"]["url"] + '">'
            content += (
                "<h1>"
                + str(markupsafe.escape(filename))
                + " - "
                + ttp["name"]
                + "</h1>"
            )
            content += "</a>"
            # Description
            mdDescription = markdown2.markdown(
                ttp["description"],
                extras=["task_list", "fenced-code-blocks", "target-blank-links"],
            )
            soupDescription = BeautifulSoup(mdDescription, "html.parser")
            content += str(soupDescription)

            # Guides Referencing
            # guideRefcontent += '<div class="col-sm-2 toc-sidebar">'
            guideRefcontent += "<h5>Guides Referencing</h5>"
            guideRefcontent += '<ul class="guides-referencing-ul">'
            for file in files:
                guideRefcontent += "<li>"
                guideRefcontent += (
                    '<a id="local-a" href="javascript:undefined" onclick="getContent(\''
                    + file["path"]
                    + "')\">"
                )
                guideRefcontent += file["name"]
                guideRefcontent += "</a>"
                guideRefcontent += "</li>"
            guideRefcontent += "</ul>"
            # guideRefcontent += "</div>"

            # Platforms
            content += "<h3>Platforms</h3>"
            content += "<p>" + ttp["platforms"][0]
            for platform in ttp["platforms"][1:]:
                content += ", " + platform
            content += "</p>"
            # Phases
            content += "<h3>ATT&CK Phases</h3>"
            content += "<p>" + ttp["phases"][0]["phase_name"].replace("-", " ").title()
            for phase in ttp["phases"][1:]:
                content += ", " + phase["phase_name"].replace("-", " ").title()
            content += "</p>"
            # Detection
            content += "<h3>Detection</h3>"
            mdDetection = markdown2.markdown(
                ttp["detection"],
                extras=["task_list", "fenced-code-blocks", "target-blank-links"],
            )
            soupDetection = BeautifulSoup(mdDetection, "html.parser")
            content += str(soupDetection)
            # References
            content += "<h3>References</h3>"
            if len(ttp["allSources"]) > 1:
                content += "<ul>"
                for source in ttp["allSources"]:
                    if source["source_name"] == "mitre-attack":
                        continue
                    try:
                        content += (
                            "<li><a target='_blank' href='" + source["url"] + "'>"
                        )
                    except Exception:
                        content += (
                            "<li><a target='_blank' href='"
                            + "javascript:void(0)"
                            + "'>"
                        )
                    try:
                        content += source["description"]
                    except Exception:
                        try:
                            content += source["external_id"]
                        except Exception:
                            try:
                                content += source["source_name"]
                            except Exception:
                                content += "Call your friendly developer and tell him the link is broken."
                    content += "</a></li>"
                content += "</ul>"

        # Actual file contents
        try:
            f = open(path, "r")
            fileContent = f.read()
            f.close()
            if path[-1] == "d" and path[-2] == "m":
                mdContent = markdown2.markdown(
                    fileContent,
                    extras=[
                        "task_list",
                        "fenced-code-blocks",
                        "header-ids",
                        "tables",
                        "toc",
                    ],
                )
                soup = BeautifulSoup(mdContent, "html.parser")
                # adjusting Links for relative paths and external paths
                for link in soup.find_all("a"):
                    if link.get("href"):
                        if len(link.get("href")) >= 4:
                            if (
                                link.get("href")[0] != "h"
                                and link.get("href")[1] != "t"
                                and link.get("href")[2] != "t"
                                and link.get("href")[3] != "p"
                            ):
                                # this is a relative link
                                link["onclick"] = (
                                    "getContent('"
                                    + self.localPath
                                    + parent
                                    + link.get("href").replace("../", "")
                                    + "')"
                                )
                                link["href"] = "javascript:undefined"
                                link["id"] = "local-a"
                            else:  # we're heading elsewhere
                                link["target"] = "_blank"
                # Injecting ToC to file
                try:
                    toc = BeautifulSoup(mdContent.toc_html, "html.parser")
                    details_tag = toc.new_tag("details")
                    details_tag["open"] = ""
                    summary_tag = toc.new_tag("summary")
                    strong_tag = toc.new_tag("strong")
                    strong_tag.append("Table of Contents")
                    summary_tag.append(strong_tag)
                    details_tag.append(summary_tag)
                    details_tag.append(toc)
                    # h1 = soup.find("h1")
                    # if h1:
                    # 	h1.insert_after(details_tag)
                    toc_content = str(details_tag)
                    finalContent += (
                        '<div class="col-sm-2 toc-sidebar">'
                        + toc_content
                        + guideRefcontent
                        + "</div>"
                    )
                except Exception as e:
                    print(e)
                    try:
                        finalContent += guideRefcontent
                    except Exception as e:
                        print(e)
                codeblock_counter = 0
                for pre in soup.find_all("pre"):
                    if pre.find("code"):
                        new_div = soup.new_tag("div")
                        new_div["class"] = "codeblock-wrapper"
                        new_div["id"] = "codeblock-wrapper-" + str(codeblock_counter)
                        code = pre.find("code")
                        code["id"] = "codeblock-content-" + str(codeblock_counter)
                        new_btn = soup.new_tag("button")
                        new_btn["onclick"] = "copyCode(" + str(codeblock_counter) + ")"
                        new_btn["class"] = "btn btn-danger btn-copy"
                        new_btn.append("Copy")
                        pre.wrap(new_div)
                        pre.parent.insert_before(new_btn)
                        codeblock_counter += 1
                content += str(soup)
            else:
                # Jan 24 2022 - We're going to construct a markdown file around the file contents
                # First, get the extension
                extension = "." + path.split(".")[-1]
                syntax = ""
                matched = False
                # We are going to use languages.yaml maintained by Github to match our extension to a known language
                yamlPath = self.localPath + "bls_bible/static/languages.yml"
                with open(yamlPath) as f:
                    langDict = yaml.safe_load(f)
                for language in langDict:
                    try:
                        for ext in langDict[language]["extensions"]:
                            if extension == ext:
                                syntax = str(language.lower())
                                matched = True
                                break
                    except Exception:
                        continue
                    if matched:
                        break
                # Hopefully we matched, if not there will not be syntax highlighting
                mdContent = "```" + syntax + "\n"
                mdContent += fileContent
                mdContent += "\n```"
                html = markdown2.markdown(
                    mdContent, extras=["fenced-code-blocks", "task_list"]
                )
                soup = BeautifulSoup(html, "html.parser")
                codeblock_counter = 0
                for pre in soup.find_all("pre"):
                    if pre.find("code"):
                        new_div = soup.new_tag("div")
                        new_div["class"] = "codeblock-wrapper"
                        new_div["id"] = "codeblock-wrapper-" + str(codeblock_counter)
                        code = pre.find("code")
                        code["id"] = "codeblock-content-" + str(codeblock_counter)
                        new_btn = soup.new_tag("button")
                        new_btn["onclick"] = "copyCode(" + str(codeblock_counter) + ")"
                        new_btn["class"] = "btn btn-danger btn-copy"
                        new_btn.append("Copy")
                        pre.wrap(new_div)
                        pre.parent.insert_before(new_btn)
                        codeblock_counter += 1
                content += str(soup)
        except Exception as e:
            print(e)
            content += "<h1>File Not Found</h1>"

        finalContent += '<div class="col-sm-10">' + content + "</div>"
        finalContent += "</div></div>"
        # return modal content
        return finalContent

    def get_guides_referencing_technique(self, technique):
        f = open(self.localPath + "bls_bible/static/reverse_reference.json")
        ref_dict = json.load(f)
        f.close()
        return ref_dict[technique]
