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
# search.py


import os
import json
import logging
import re
import markupsafe


class search:
    def __init__(self, source, localPath):

        self.source = source  # whoever calls this class must provide the "source"
        self.localPath = localPath

    def search_advanced(self, regex, context):

        if regex == "":
            return ""
        if context > 5:
            return "Context cannot exceed 5.\nIf you want more, submit a request."
        if context < 0:
            return "Why would you want a negative context?"
        root = self.localPath + "Data/"
        fileList = {"results": []}
        for root, subdirs, files in os.walk(root):
            for file in files:
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    with open(path, "r") as f:
                        try:
                            if re.search(regex, f.read()) is not None:
                                f.seek(0)
                                matches = []
                                lines = f.readlines()
                                for lineNum, lineVal in enumerate(lines):
                                    result = re.search(regex, lineVal)
                                    if result is not None:
                                        contextRange = list(
                                            range(-context, context + 1)
                                        )
                                        print(contextRange)
                                        finalResult = ""
                                        for c in contextRange:
                                            if (
                                                lineNum + c < 0
                                                or lineNum + c > len(lines) - 1
                                            ):
                                                continue
                                            finalResult += lines[lineNum + c]
                                        safeString = str(markupsafe.escape(finalResult))
                                        highlightString = safeString.replace(
                                            result.group(),
                                            '<span class="highlight-regex"><b>'
                                            + result.group()
                                            + "</b></span>",
                                        )
                                        highlightString = highlightString.replace(
                                            "\n", "<br/>"
                                        )
                                        matches.append(highlightString)
                                match = {"path": path, "matches": matches}
                                fileList["results"].append(match)
                        except Exception as e:
                            print(e)
                            continue
        return fileList

    def search_local(
        self,
        term,
        osTags,
        onpremTags,
        cloudTags,
        applicationTags,
        specialTags,
        guideTtpTags,
        aptTags,
    ):
        if term == "":
            return ""
        if not all(t.isalnum() or t.isspace() for t in term):
            return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if osTags:
            for tag in osTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if onpremTags:
            for tag in onpremTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if cloudTags:
            for tag in cloudTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if applicationTags:
            for tag in applicationTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if specialTags:
            for tag in specialTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if guideTtpTags:
            for tag in guideTtpTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"
        if aptTags:
            for tag in aptTags:
                if not tag.isalnum():
                    return "<ul class='search-ul'><li class='search-li'>Bad Input - Special Characters</li></ul>"

        # First, collect the files that contain the search term as a special tag
        # tag = "#@" + term
        # Split term to support multiple terms, AND logic
        search_terms = term.split(" ")
        prefix = self.localPath + "bls_bible/static/"
        f = open(prefix + "searchIndex.json")
        data = json.load(f)
        f.close()
        files = []
        has_all_terms = True
        for term in search_terms:
            if not "#@" + term.upper() in data:
                has_all_terms = False
                break
        if has_all_terms:
            temp_set = set(data["#@" + search_terms[0].upper()])
            for term in search_terms[1:]:
                temp_set = temp_set.intersection(set(data["#@" + term.upper()]))
            temp_list = list(temp_set)
            for file in temp_list:
                files.append(file)

        # for key in data:
        #    if "#@" + term.upper() in key:
        #        for i in data[key]:
        #            files.append(i)

        # Second, collect the files that contain the search term in their name
        f = open(prefix + "fileList.json")
        data = json.load(f)
        f.close()
        for file in data:
            has_all_terms = True
            for term in search_terms:
                if term.upper() in file.upper():
                    continue
                else:
                    has_all_terms = False
                    break
            if has_all_terms:
                files.append(file)

        # Third, remove repeats
        fileSet = set(files)
        fileList = list(fileSet)

        # Fourth, run the list through our filters and create unique filter group sets
        # Then, intersect those sets with our original file set
        f = open(prefix + "searchIndex.json")
        data = json.load(f)
        f.close()
        if osTags:
            osTagFiles = []
            for filt in osTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                osTagFiles.append(file)
                                break
            osTagFileSet = set(osTagFiles)
            fileSet = fileSet.intersection(osTagFileSet)
        if onpremTags:
            onpremTagFiles = []
            for filt in onpremTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                onpremTagFiles.append(file)
                                break
            onpremTagFileSet = set(onpremTagFiles)
            fileSet = fileSet.intersection(onpremTagFileSet)
        if cloudTags:
            cloudTagFiles = []
            for filt in cloudTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                cloudTagFiles.append(file)
                                break
            cloudTagFileSet = set(cloudTagFiles)
            fileSet = fileSet.intersection(cloudTagFileSet)
        if applicationTags:
            applicationTagFiles = []
            for filt in applicationTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                applicationTagFiles.append(file)
                                break
            applicationTagFileSet = set(applicationTagFiles)
            fileSet = fileSet.intersection(applicationTagFileSet)
        if specialTags:
            specialTagFiles = []
            for filt in specialTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                specialTagFiles.append(file)
                                break
            specialTagFileSet = set(specialTagFiles)
            fileSet = fileSet.intersection(specialTagFileSet)
        if guideTtpTags:
            guideTtpTagFiles = []
            for filt in guideTtpTags:
                for file in fileList:
                    tag = "#@" + filt
                    if tag.upper() in data:
                        for entry in data[tag.upper()]:
                            if file == entry:
                                guideTtpTagFiles.append(file)
                                break
            guideTtpTagFileSet = set(guideTtpTagFiles)
            fileSet = fileSet.intersection(guideTtpTagFileSet)
        if aptTags:
            aptTagFiles = []
            for filt in aptTags:
                aptTechniques = []
                md5_pattern = r"([a-fA-F\d]{32})"
                if re.match(md5_pattern, filt):
                    try:
                        f = open(self.localPath + "bls_bible/static/profiles.json")
                        profiles = json.load(f)
                        f.close()
                    except Exception:
                        profiles = []
                    for profile in profiles:
                        if profile["id"] == filt:
                            for ttp in profile["ttps"]:
                                techId = (
                                    ttp["ttp_file"].replace(".md", "").split("_")[0]
                                )
                                aptTechniques.append(techId)
                            break
                else:
                    f = open(self.localPath + "bls_bible/static/mitre/groups/apts.json")
                    data = json.load(f)
                    f.close()
                    for apt in data:
                        try:
                            if apt["name"].split("(")[1].replace(")", "") == filt:
                                for technique in apt["techniques"]:
                                    aptTechniques.append(technique["techniqueID"])
                                break
                        except TypeError as e:
                            logging.error(str(e))
                            pass
                f = open(self.localPath + "bls_bible/static/fileList.json")
                data = json.load(f)
                f.close()
                for file in data:
                    if any(tech in file for tech in aptTechniques):
                        aptTagFiles.append(file)

            aptTagFileSet = set(aptTagFiles)
            fileSet = fileSet.intersection(aptTagFileSet)

        fileList = list(fileSet)

        # Fifth, build out the HTML list
        content = '<ul class="search-ul">\n'
        for file in fileList:
            name = file.split("/")
            name = name[-2] + "/" + name[-1]
            # name = file[file.rfind("/").rfind("/")+1:]
            name = name[: name.rfind(".md")]
            name = name.replace("_", " ")
            oncontextmenu = ""
            if "/Data/TTP/" in file:
                oncontextmenu = (
                    'oncontextmenu="context(event, '
                    "'" + file + "', 'ttp-search', this)\" "
                )
            content += (
                "<li class='search-li' "
                + oncontextmenu
                + "onclick='getContent(\""
                + file.replace("\n", "")
                + "\")'>\n\t"
                + name
                + "</li>\n"
            )
        content += "</ul>"
        content += "</ul>"
        return content


class search_filter:
    def __init__(self, localPath):
        self.localPath = localPath

    def filter_apts(self, apt):
        md5_pattern = r"([a-fA-F\d]{32})"
        dataStr = ""
        if re.match(md5_pattern, apt):
            selected_profile = {}
            try:
                f = open(self.localPath + "bls_bible/static/profiles.json")
                profiles = json.load(f)
                f.close()
            except Exception:
                profiles = []
            for profile in profiles:
                if profile["id"] == apt:
                    selected_profile = profile
                    break
            techId = (
                selected_profile["ttps"][0]["ttp_file"].replace(".md", "").split("_")[0]
            )
            dataStr = techId
            for ttp in selected_profile["ttps"][1:]:
                techId = ttp["ttp_file"].replace(".md", "").split("_")[0]
                dataStr += "|" + techId
        else:
            f = open(self.localPath + "bls_bible/static/mitre/groups/apts.json")
            data = json.load(f)
            f.close()
            apt_obj = {}
            for obj in data:
                try:
                    if obj["name"].split("(")[1].split(")")[0] == apt:
                        apt_obj = obj
                        break
                except Exception as e:
                    print(e)
            techniques = []
            for tech in apt_obj["techniques"]:
                for key, value in tech.items():
                    if key == "techniqueID":
                        techniques.append(value)
                        break
            ttps = techniques
            final = ttps
            for ttp in ttps:
                if ttp.find(".") >= 0:
                    parent = ttp.split(".")[0]
                    if parent in final:
                        final.remove(parent)
            dataStr = final[0]
            for fin in final[1:]:
                dataStr += "|" + fin
        return dataStr
