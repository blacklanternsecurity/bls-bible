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
# ui.py

import json
import os
import markdown2
import re
import hashlib
import markupsafe
import yaml

from bs4 import BeautifulSoup
from bls_bible.lib.utils import utils


class ui:
    def __init__(self, localPath, parent, safePath):
        self.localPath = localPath
        self.parent = parent
        self.safePath = safePath
        self.utils = utils(self.localPath)
        self.accordionKey = 1

    def get_theme(self):
        try:
            prefix = self.localPath + "bls_bible/static/"
            f = open(prefix + "theme.json")
            themeJson = json.load(f)
            f.close()
            return "css/" + themeJson["theme"] + ".css"
        except Exception as e:
            print(e)
            return "css/red.css"

    def change_theme(self, color):
        if color not in ["red", "blue", "cyan", "gold", "purple"]:
            return False
        theme = {"theme": color}
        prefix = self.localPath + "bls_bible/static/"
        try:
            f = open(prefix + "theme.json", "w")
            json.dump(theme, f)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    def highlight_ttps(self, path):
        if os.path.commonprefix(
            (os.path.realpath(path), os.path.realpath(self.safePath))
        ) != os.path.realpath(self.safePath):
            return False
        arr = []
        f = open(path)
        fileContent = f.read()
        f.close()
        mdContent = markdown2.markdown(
            fileContent, extras=["fenced-code-blocks", "task_list"]
        )
        soup = BeautifulSoup(mdContent, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href").replace("../", "")
            if href[0:4] == "TTP/":
                arr.append(href)
            else:
                continue
        results = ""
        if arr:
            setOfFiles = set(arr)
            uniqFiles = list(setOfFiles)
            f = open(self.localPath + "bls_bible/static/reverse_reference.json")
            ref_dict = json.load(f)
            f.close()
            finalFiles = []
            for file in uniqFiles:
                technique_id = file.split("/")[-1].replace(".md", "").split("_")[0]
                if not re.match("T[0-9]{4}", technique_id):
                    continue
                technique = ref_dict[technique_id]
                for phase in technique["phases"]:
                    finalFiles.append(
                        file.split("/")[0]
                        + "/"
                        + phase["name"].replace(" ", "_")
                        + "/"
                        + "/".join(file.split("/")[1:])
                    )
            uniqFiles = finalFiles
            if not len(uniqFiles) > 0:
                return results
            results += uniqFiles[0]
            print("\n\n" + str(uniqFiles) + "\n\n")
            for uniqFile in uniqFiles[1:]:
                results += "|" + uniqFile
        return results

    def endpoint_blocked(self):
        print("user endpoint blocked")
        return "<h1>Endpoint not available on this server type. But if you can reach it anyway, let us know.</h1>"

    def getTabContent(self, path):

        content = ""

        if os.path.commonprefix(
            (os.path.realpath(path), os.path.realpath(self.safePath))
        ) != os.path.realpath(self.safePath):
            return "<h1>Stop trying to look at my private parts :P</h1>"

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
            ttp = self.utils.get_ttp_content(filename)

            # Get the guides that reference this technique
            obj = self.utils.get_guides_referencing_technique(filename)
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
                extras=["fenced-code-blocks", "target-blank-links", "task_list"],
            )
            soupDescription = BeautifulSoup(mdDescription, "html.parser")
            content += str(soupDescription)

            # Guides Referencing
            content += '<h3 class="guides-referencing-h3">Guides Referencing</h3>'
            content += '<ul class="guides-referencing-ul">'
            for file in files:
                content += "<li>"
                content += (
                    '<a id="local-a" href="javascript:undefined" onclick="getContent(\''
                    + file["path"]
                    + "')\">"
                )
                content += file["name"]
                content += "</a>"
                content += "</li>"
            content += "</ul>"

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
                    content += "<li><a target='_blank' href='" + source["url"] + "'>"
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

        # Actual File Contents
        try:
            f = open(path, "r")
            fileContent = f.read()
            f.close()
        except Exception as e:
            print(e)
            fileContent = ""

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
            js_script = soup.new_tag("script")
            js_script["src"] = "js/site.js"
            js_script["type"] = "text/javascript"
            css_link = soup.new_tag("link")
            css_link["href"] = "css/site.css"
            css_link["type"] = "text/css"
            css_link["rel"] = "stylesheet"
            native_link = soup.new_tag("link")
            native_link["href"] = "css/native.css"
            native_link["type"] = "text/css"
            native_link["rel"] = "stylesheet"
            bs_link = soup.new_tag("link")
            bs_link["href"] = "css/bootstrap.min.css"
            bs_link["type"] = "text/css"
            bs_link["rel"] = "stylesheet"
            jq_script = soup.new_tag("script")
            jq_script["src"] = "js/jquery-3.5.1.min.js"
            jq_script["type"] = "text/javascript"
            bs_script = soup.new_tag("script")
            bs_script["src"] = "js/bootstrap.bundle.min.js"
            bs_script["type"] = "text/javascript"
            for link in soup.find_all(
                "a"
            ):  # adjusting Links for relative paths and external paths
                if len(link.get("href")) >= 4:
                    if (
                        link.get("href")[0] != "h"
                        and link.get("href")[1] != "t"
                        and link.get("href")[2] != "t"
                        and link.get("href")[3] != "p"
                    ):
                        # this is a relative link
                        link["onclick"] = (
                            "openInNewTab('"
                            + self.localPath
                            + self.parent
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
                summary_tag = toc.new_tag("summary")
                strong_tag = toc.new_tag("strong")
                strong_tag.append("Table of Contents")
                summary_tag.append(strong_tag)
                details_tag.append(summary_tag)
                details_tag.append(toc)
                h1 = soup.find("h1")
                if h1:
                    h1.insert_after(details_tag)
            except Exception:
                pass
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
            body_tag = soup.new_tag("body")
            body_tag["class"] = "body_tab"
            heading_tag = soup.new_tag("h4")
            b_tag = soup.new_tag("b")
            b_tag.append(
                str(markupsafe.escape(path.split(self.localPath + self.parent)[1]))
            )
            heading_tag.append(b_tag)
            heading_tag["class"] = "file-content-header"
            body_tag.append(heading_tag)
            ruler_tag = soup.new_tag("hr")
            body_tag.append(ruler_tag)
            body_tag.append(soup)
            head_tag = soup.new_tag("head")
            html_tag = soup.new_tag("html")
            title_tag = soup.new_tag("title")
            title_tag.append(path.split("/")[-1])
            head_tag.append(title_tag)
            head_tag.append(jq_script)
            head_tag.append(bs_script)
            head_tag.append(js_script)
            head_tag.append(bs_link)
            head_tag.append(css_link)
            head_tag.append(native_link)
            html_tag.append(head_tag)
            html_tag.append(body_tag)
            content += str(html_tag)
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
                    pass
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
            js_script = soup.new_tag("script")
            js_script["src"] = "js/site.js"
            js_script["type"] = "text/javascript"
            css_link = soup.new_tag("link")
            css_link["href"] = "css/site.css"
            css_link["type"] = "text/css"
            css_link["rel"] = "stylesheet"
            native_link = soup.new_tag("link")
            native_link["href"] = "css/native.css"
            native_link["type"] = "text/css"
            native_link["rel"] = "stylesheet"
            bs_link = soup.new_tag("link")
            bs_link["href"] = "css/bootstrap.min.css"
            bs_link["type"] = "text/css"
            bs_link["rel"] = "stylesheet"
            jq_script = soup.new_tag("script")
            jq_script["src"] = "js/jquery-3.5.1.min.js"
            jq_script["type"] = "text/javascript"
            bs_script = soup.new_tag("script")
            bs_script["src"] = "js/bootstrap.bundle.min.js"
            bs_script["type"] = "text/javascript"
            body_tag = soup.new_tag("body")
            body_tag["class"] = "body_tab"
            heading_tag = soup.new_tag("h4")
            b_tag = soup.new_tag("b")
            b_tag.append(
                str(markupsafe.escape(path.split(self.localPath + self.parent)[1]))
            )
            heading_tag.append(b_tag)
            heading_tag["class"] = "file-content-header"
            body_tag.append(heading_tag)
            ruler_tag = soup.new_tag("hr")
            body_tag.append(ruler_tag)
            body_tag.append(soup)
            head_tag = soup.new_tag("head")
            html_tag = soup.new_tag("html")
            title_tag = soup.new_tag("title")
            title_tag.append(path.split("/")[-1])
            head_tag.append(title_tag)
            head_tag.append(jq_script)
            head_tag.append(bs_script)
            head_tag.append(js_script)
            head_tag.append(bs_link)
            head_tag.append(css_link)
            head_tag.append(native_link)
            html_tag.append(head_tag)
            html_tag.append(body_tag)
            content += str(html_tag)
        return content

    def parseJsonData(self, json, type):
        content = ""
        for child in json:
            self.accordionKey += 1
            accordionId = hashlib.md5(
                (type + child["name"] + str(self.accordionKey)).encode()
            ).hexdigest()
            if child["type"] == "folder":
                # Create the normal child accordion
                content += '<div class="child-container accordion-container col-4" data-apt-filter="0" >'
                content += '<div class="accordion" id="accordionPanelsStayOpenExample">'
                content += '<div class="accordion-item">'
                content += (
                    '<h2 data-ttp-toggle-count="0" data-blue-toggle-count="0" data-red-toggle-count="0" '
                    'class="accordion-header" id="panelsStayOpen-heading'
                    + accordionId
                    + '">'
                )
                content += (
                    '<button class="accordion-button collapsed" type="button" '
                    'data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse'
                    + accordionId
                    + '" aria-expanded="false" aria-controls="panelsStayOpen-collapse'
                    + accordionId
                    + '">'
                )
                content += child["name"]
                content += (
                    '<span data-toggle-count="0" class="material-icons no-border highlighter-'
                    + str(markupsafe.escape(type))
                    + '">highlight</span>'
                )
                content += "</button>"
                content += "</h2>"
                content += (
                    '<div id="panelsStayOpen-collapse'
                    + accordionId
                    + '" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading'
                    + accordionId
                    + '">'
                )
                content += '<div class="accordion-body">'
                # Recursion
                content += self.parseJsonData(child["children"], type)
                # Close out the accordion
                content += "</div>"
                content += "</div>"
                content += "</div>"
                content += "</div>"
                content += "</div>"
            elif child["type"] == "url":
                # Create the smaller file container, no recursion necessary
                content += '<div class="child-container accordion-container col-4" data-apt-filter="0">'
                content += '<div class="accordion-item">'
                filePath = child["url"].split("'")[1]
                indent = "file-indent-1"
                fileName = filePath.split("/")[-1]
                one_half_pattern = r"^000\-[1-9]*\_"
                second_pattern = r"^([0-9]{2}[1-9]{1}|[1-9]{1}[0-9]{2}|[0-9]{1}[1-9]{1}[0-9]{1})(\-0)?\_"
                third_pattern = r"^([0-9]{2}[1-9]{1}|[1-9]{1}[0-9]{2}|[0-9]{1}[1-9]{1}[0-9]{1})\-[1-9]*\_"
                if re.match(one_half_pattern, fileName):
                    indent = "file-indent-1-2"
                elif re.match(second_pattern, fileName):
                    indent = "file-indent-2"
                elif re.match(third_pattern, fileName):
                    indent = "file-indent-3"
                if type.lower() == "red" or type.lower() == "blue":
                    content += (
                        "<span oncontextmenu=\"context(event, '"
                        + filePath
                        + "', '"
                        + str(markupsafe.escape(type.lower()))
                        + '\', this)" data-ttp-toggle-count="0" onclick="'
                        + child["url"]
                        + '" class="accordion-header file '
                        + indent
                        + '" id="panelsStayOpen-heading'
                        + accordionId
                        + '">'
                    )
                else:
                    content += (
                        "<span oncontextmenu=\"context(event, '"
                        + filePath
                        + "', '"
                        + str(markupsafe.escape(type.lower()))
                        + '\', this)" data-blue-toggle-count="0" data-red-toggle-count="0" onclick="'
                        + child["url"]
                        + '" class="accordion-header file '
                        + indent
                        + '" id="panelsStayOpen-heading'
                        + accordionId
                        + '">'
                    )
                content += child["name"]
                content += (
                    '<span data-toggle-count="0" class="material-icons no-border highlighter-'
                    + str(markupsafe.escape(type))
                    + '">highlight</span>'
                )
                content += "</span>"
                content += "</div>"
                content += "</div>"
        return content

    def getAccordion(self, file, type):
        self.accordionKey += 1
        f = open(file)
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Problem decoding json file: " + file)
            return ""
        f.close()
        accordionId = hashlib.md5(
            (type + data["name"] + str(self.accordionKey)).encode()
        ).hexdigest()
        content = ""
        content += '<div class="accordion" id="accordionPanelsStayOpenExample">'
        content += '<div class="accordion-item">'
        content += (
            '<h2 class="accordion-header" id="panelsStayOpen-heading'
            + accordionId
            + '">'
        )
        content += (
            '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" '
            'data-bs-target="#panelsStayOpen-collapse'
            + accordionId
            + '" aria-expanded="false" aria-controls="panelsStayOpen-collapse'
            + accordionId
            + '">'
        )
        content += data["name"]
        content += "</button>"
        content += "</h2>"
        content += (
            '<div id="panelsStayOpen-collapse'
            + accordionId
            + '" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading'
            + accordionId
            + '">'
        )
        content += '<div class="accordion-body">'
        if type == "Red":
            file_children = []
            folder_children = []
            for child in data["children"]:
                if child["type"] == "folder":
                    folder_children.append(child)
                else:
                    file_children.append(child)
            final_children = []
            final_children.extend(file_children)
            final_children.extend(folder_children)
            data["children"] = final_children
        content += self.parseJsonData(data["children"], type)
        content += "</div>"
        content += "</div>"
        content += "</div>"
        content += "</div>"
        return content

    def fileIndexer(self):
        prefix = self.localPath + "bls_bible/static/"
        files = ["red.json", "blue.json", "ttp.json"]
        urls = []
        f = open(self.localPath + "bls_bible/static/searchIndex.json")
        try:
            searchIndex = json.load(f)
        except Exception as e:
            print(e)
            searchIndex = {}
        f.close()
        for file in files:
            f = open(prefix + file)
            data = json.load(f)
            f.close()
            self.utils.getUrls(data, urls)
        with open(prefix + "fileList.json", "w+") as out:
            json.dump(urls, out)
        # Iterate through each file. Find the tags in the file
        # Add the file to a dictionary using the tags as keys
        tag_pattern = "#@\w+"
        for url in urls:
            f = open(url)
            try:
                for line in f:
                    if "#@" in line:
                        tags = re.findall(tag_pattern, line)
                        for tag in tags:
                            if tag.upper() not in searchIndex:
                                searchIndex[tag.upper()] = [url]
                            else:
                                searchIndex[tag.upper()].append(url)
            except Exception:
                continue
            f.close()
        with open(prefix + "searchIndex.json", "w+") as out:
            json.dump(searchIndex, out)
        return str(json.dumps(searchIndex, indent=4))
