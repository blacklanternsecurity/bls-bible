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
# devtools.py
import json
import os
import markdown2
from bs4 import BeautifulSoup

from bls_bible.lib.update import update
from bls_bible.lib.threat_profiles import manage_profiles, analyze_profiles
from bls_bible.lib.utils import utils

class developer_tools:
    def __init__(self, source, parent, localPath, safePath, localDeployment):
        self.source = "local"
        self.parent = parent
        self.localPath = localPath
        self.safePath = safePath
        self.accordionKey = 0
        self.localDeployment = localDeployment
        self.utils = utils(self.localPath)
    def devTools(self):
        dev_tools = [
            {
                'description': 'Returns a list of techniques in the MITRE data that are missing from /Data/TTP/',
                'endpoint': '/getMissing'
            },
            {
                'description': 'Returns a list of techniques in the MITRE data that are flagged as "revoked"',
                'endpoint': '/getRevoked'
            },
            {
                'description': 'Returns a list of broken links present in each guide',
                'endpoint': '/getBroken'
            },
            {
                'description': 'Returns a list of guides that do not link to any technique files',
                'endpoint': '/getGuidesNotReferencing'
            },
            {
                'description': 'Returns a list of techniques that either have a mismatched '
                               'parent- or sub-title from current MITRE data',
                'endpoint': '/validateFolderNaming'
            },
            {
                'description': 'Returns a list of techniques that are not linked to by the appropriate guides',
                'endpoint': '/getMissingGuideReferences'
            }
        ]
        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'
        content += '<div class="row"><div class="col-sm-12"><ul>'
        for tool in dev_tools:
            content += '<li>'
            content += '<a href="' + tool['endpoint'] + '">' + tool['endpoint'] + '</a> - ' + tool['description']
            content += '</li>'
        content += '</ul></div></div>'
        content += '</body>' \
                   '</html>'
        return content

    def get_missing_techniques(self):
        f = open(self.localPath + 'bls_bible/static/missing_techniques.json')
        data = json.load(f)
        f.close()
        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'
        content += '<div class="row"><div class="col-sm-2">Not Found:</div></div>'
        content += '<div class="row"><div class="col-sm-12"><ul>'
        for missing in data:
            content += '<li>'
            if data[missing]['sub_title'] == '':
                content += '/Data/TTP/' + missing + '_' + data[missing]['parent_title'].replace(' ', '_') + \
                           '/' + missing + '.md'
            else:
                content += '/Data/TTP/' + missing.split('.')[0] + '_' + \
                           data[missing]['parent_title'].replace(' ', '_') + '/' + missing.split('.')[1] + \
                           '_' + data[missing]['sub_title'].replace(' ', '_') + '/' + missing + '.md'
            content += '</li>'
        content += '</ul></div></div>'
        content += '</body>' \
                   '</html>'
        return content

    def get_revoked_techniques(self):
        f = open(self.localPath + 'bls_bible/static/revoked.json')
        data = json.load(f)
        f.close()
        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'
        content += '<div class="row"><div class="col-sm-2">Revoked:</div></div>'
        content += '<div class="row"><div class="col-sm-12"><ul>'
        for obj in data:
            content += '<li>'
            content += '/Data/TTP/' + obj['external_references'][0]['external_id'] + "_" + \
                       obj['name'].replace(' ', '_') + '/' + \
                       obj['external_references'][0]['external_id'] + '.md'
            content += '</li>'
        content += '</ul></div></div>'
        content += '</body>' \
                   '</html>'
        return content

    def get_guides_not_referencing(self):
        f = open(self.localPath + 'bls_bible/static/reverse_reference.json')
        ref_dict = json.load(f)
        f.close()

        red_guides = []
        blue_guides = []
        apps_services_web_guides = []
        for guide in ref_dict['none']['guides_referencing']:
            if '/Apps_and_Services/Web/' in guide['guide_path']:
                apps_services_web_guides.append(guide)
            elif guide['guide_color'] == 'red':
                red_guides.append(guide)
            elif guide['guide_color'] == 'blue':
                blue_guides.append(guide)
        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'
        content += '<div class="row"><div class="col-sm-12">' \
                   '<details>' \
                   '<summary>Red Guides Lacking References to Techniques:</summary>' \
                   '<ul>'
        for guide in red_guides:
            content += '<li>' + guide['guide_name'] + " : " + guide['guide_path'] + '</li>'
        content += '</ul>' \
                   '</details>' \
                   '</div></div>'
        content += '<div class="row"><div class="col-sm-12">' \
                   '<details>' \
                   '<summary>Blue Guides Lacking References to Techniques:</summary>' \
                   '<ul>'
        for guide in blue_guides:
            content += '<li>' + guide['guide_name'] + " : " + guide['guide_path'] + '</li>'
        content += '</ul>' \
                   '</details>' \
                   '</div></div>'
        content += '<div class="row"><div class="col-sm-12">' \
                   '<details>' \
                   '<summary>Apps and Services - Web Lacking References to Techniques:</summary>' \
                   '<ul>'
        for guide in apps_services_web_guides:
            content += '<li>' + guide['guide_name'] + " : " + guide['guide_path'] + '</li>'
        content += '</ul>' \
                   '</details>' \
                   '</div></div>'
        content += '</body>' \
                   '</html>'
        return content

    def validate_folder_naming(self):
        f = open(self.localPath + 'bls_bible/static/reverse_reference.json')
        ref_dict = json.load(f)
        f.close()

        invalid_folder_names = []

        for ref in ref_dict:
            result = {
                'full-path': '',
                'parent-old': '',
                'parent-new': '',
                'sub-old': '',
                'sub-new': ''
            }
            invalid = False
            technique = ref_dict[ref]
            if technique['parent_title'].replace('/', '-').replace(' ', '_').replace(')', '').replace('(', '') not in technique['full_path']:
                invalid = True
                result['parent-old'] = '_'.join(technique['full_path'].split('/')[1].split('_')[1:])
                result['parent-new'] = technique['parent_title']
            if technique['sub_title'].replace('/', '-').replace(' ', '_').replace(')', '').replace('(', '') not in technique['full_path']:
                invalid = True
                result['sub-old'] = '_'.join(technique['full_path'].split('/')[2].split('_')[1:])
                result['sub-new'] = technique['sub_title']
            if invalid:
                result['full-path'] = technique['full_path']
                invalid_folder_names.append(result)

        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'
        content += '<div class="row"><div class="col-sm-2">Not Found:</div></div>'
        for entry in invalid_folder_names:
            content += '<div class="row"><div class="col-sm-12">'
            content += '<details>' \
                       '<summary>' + entry['full-path'] + '</summary>'
            content += '<ul>'
            content += '<li>Old Parent: ' + entry['parent-old'] + '</li>'
            content += '<li>New Parent: ' + entry['parent-new'].replace(' ', '_') + '</li>'
            content += '<li>Old Sub: ' + entry['sub-old'] + '</li>'
            content += '<li>New Sub: ' + entry['sub-new'].replace(' ', '_') + '</li>'
            content += '</ul>'
            content += '</details>'
            content += '</div></div>'
        content += '</body>' \
                   '</html>'

        return content

    def getBroken(self):
        prefix = self.localPath + "bls_bible/static/"
        files = [prefix+'blue.json', prefix+'red.json', prefix+'ttp.json']
        urls = []
        totalDict = {}
        brokenDict = {}
        # Get all of the files
        for file in files:
            f = open(file)
            data = json.load(f)
            f.close()
            self.utils.getUrls(data, urls)
        # Iterate through each file, pull out the local links
        for url in urls:
            links = []
            try:
                f = open(url)
                fileContent = f.read()
            except:
                continue
            f.close()
            mdContent = markdown2.markdown(fileContent, extras=["fenced-code-blocks", "task_list"])
            soup = BeautifulSoup(mdContent, 'html.parser')
            for link in soup.find_all('a'):  # adjusting Links for relative paths and external paths
                if link.get('href') and len(link.get('href')) >= 4:
                    if link.get('href')[0] != 'h' and link.get('href')[1] != 't' and link.get('href')[
                            2] != 't' and link.get('href')[3] != 'p':
                        links.append(self.localPath + self.parent + link.get('href').replace("../", ""))
            totalDict[url] = links
        # We have a dictionary of files and each key in the dictionary has a
        # corresponding array containing all of the local links within the document
        # We iterate through each key and check it's links. If they are bad,
        # we add the key/value pair to the brokenDict dictionary and remove the bit we add in the application
        # key = list(totalDict.keys())[1]
        # print(key + ": " + str(totalDict[key]))
        # print("Additional bit: " + self.localPath + self.parent)
        for key in totalDict.keys():
            links = totalDict[key]
            broken = []
            for link in links:
                if not os.path.exists(link):
                    broken.append(link.replace(self.localPath + self.parent, "../"))
            if len(broken) > 0:
                brokenDict[key] = broken
        content = "<html><head><link type='text/css' rel='stylesheet' " \
                  "href='css/site.css'></head><body class='getBroken'>"
        for key in brokenDict.keys():
            content += "<h5 class='brokenFile'>" + key + "</h5>"
            content += "<ul>"
            for value in brokenDict[key]:
                content += "<li>" + value + "</li>"
            content += "</ul>"
        return content


    def get_missing_guide_references(self):
        f = open(self.localPath + 'bls_bible/static/reverse_reference.json')
        ref_dict = json.load(f)
        f.close()

        # We want to return a few different things
        # 1. We want to say if the technique is missing references from red or blue guides
        # 2. We want to say if the technique is missing references from platform dependent guides
        # 3. If a guide has linked to a technique, and that guide is for a platform the technique does not support
        trim_dict = ref_dict
        del trim_dict['none']

        supported_platforms = [
            'linux',
            'windows',
            'macos',
            'azure ad',
            'google workspace',
            'iaas',
            'office 365',
            'network',
            'pre'
        ]

        for technique in trim_dict:
            missing_red = []
            missing_blue = []
            incorrect_guides = []
            tech = trim_dict[technique]
            # For the technique, we will accomplish 1 and 2
            for platform in tech['platforms']:
                if platform not in supported_platforms:
                    continue
                has_red = False
                has_blue = False
                for guide in tech['guides_referencing']:
                    if platform == guide['guide_os'] and guide['guide_color'] == 'red':
                        has_red = True
                    elif platform == guide['guide_os'] and guide['guide_color'] == 'blue':
                        has_blue = True
                if not has_red:
                    missing_red.append(platform)
                if not has_blue:
                    missing_blue.append(platform)
            # For the technique we accomplish 3
            for guide in tech['guides_referencing']:
                if guide['guide_os'] not in tech['platforms'] and guide['guide_os'] != '':
                    if guide not in incorrect_guides:
                        incorrect_guides.append(guide)
            trim_dict[technique]['missing_red'] = missing_red
            trim_dict[technique]['missing_blue'] = missing_blue
            trim_dict[technique]['incorrect_guides'] = incorrect_guides

        # At this point we have checked for all of the platforms every technique applies to
        content = '<html>' \
                  '<head>' \
                  '<script type="text/javascript" src="js/jquery-3.5.1.min.js"></script>' \
                  '<script type="text/javascript" src="js/jquery-ui.min.js"></script>' \
                  '<script type="text/javascript" src="js/bootstrap.bundle.min.js"></script>' \
                  '<link type="text/css" rel="stylesheet" href="css/bootstrap.min.css"/>' \
                  '<link type="text/css" rel="stylesheet" href="css/site.css"/>' \
                  '</head>' \
                  '<body class="getBroken">'

        # Example link string
        # ([`Process Injection - Portable Executable Injection` TTP](TTP/T1055_Process_Injection/002_Portable_
        # Executable_Injection/T1055.002.md))

        # Red
        content += '<details><summary>Red:</summary>'
        for technique in trim_dict:
            tech = trim_dict[technique]
            if len(tech['missing_red']) > 0:
                content += '<div class="row"><div class="col-sm-12">'
                content += '<details><summary>' + technique + '</summary>'
                content += '<div class="row"><div class="col-sm-12">'
                if tech['is_sub']:
                    link_str = '([`' + tech['parent_title'] + ' - ' + tech['sub_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               technique.split('.')[1] + '_' + tech['sub_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                else:
                    link_str = '([`' + tech['parent_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                content += '<code>' + link_str + '</code>'
                content += '</div></div>'
                content += '<ul>'
                for plat in tech['missing_red']:
                    content += '<li>' + plat + '</li>'
                content += '</ul>'
                content += '</details></div></div>'
        content += '</details>'

        # Blue
        content += '<details><summary>Blue:</summary>'
        for technique in trim_dict:
            tech = trim_dict[technique]
            if len(tech['missing_blue']) > 0:
                content += '<div class="row"><div class="col-sm-12">'
                content += '<details><summary>' + technique + '</summary>'
                content += '<div class="row"><div class="col-sm-12">'
                if tech['is_sub']:
                    link_str = '([`' + tech['parent_title'] + ' - ' + tech['sub_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               technique.split('.')[1] + '_' + tech['sub_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                else:
                    link_str = '([`' + tech['parent_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                content += '<code>' + link_str + '</code>'
                content += '</div></div>'
                content += '<ul>'
                for plat in tech['missing_blue']:
                    content += '<li>' + plat + '</li>'
                content += '</ul>'
                content += '</details></div></div>'
        content += '</details>'

        # Incorrect
        content += '<details><summary>Incorrect Guides:</summary>'
        for technique in trim_dict:
            tech = trim_dict[technique]
            if len(tech['incorrect_guides']) > 0:
                content += '<div class="row"><div class="col-sm-12">'
                content += '<details><summary>' + technique + '</summary>'
                content += '<div class="row"><div class="col-sm-12">'
                if tech['is_sub']:
                    link_str = '([`' + tech['parent_title'] + ' - ' + tech['sub_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               technique.split('.')[1] + '_' + tech['sub_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                else:
                    link_str = '([`' + tech['parent_title'] + '` TTP](TTP/' + \
                               technique.split('.')[0] + '_' + tech['parent_title'].replace(' ', '_') + '/' + \
                               tech['file_name'] + '))'
                content += '<code>' + link_str + '</code>'
                content += '</div></div>'
                content += '<ul>'
                for guide in tech['incorrect_guides']:
                    content += '<li>' + guide['guide_name'] + " : " + guide['guide_path'] + '</li>'
                content += '</ul>'
                content += '</details></div></div>'
        content += '</details>'

        content += '</body>' \
                   '</html>'
        return content

