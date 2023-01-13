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
# file_editing.py
import gitlab
import os
from bls_bible.lib.utils import utils


class file_editing:

    def __init__(self, localPath, localDeployment, parent, safePath):

        self.localPath = localPath
        self.localDeployment = localDeployment
        self.parent = parent
        self.safePath = safePath

    def edit_file(self, path):

        if not self.localDeployment:
            return False
        content = ""
        content += "<textarea id='edit_textarea'>"
        if os.path.commonprefix((os.path.realpath(path), self.safePath)) != self.safePath:
            content += "# Stop trying to look at my private parts :P"
        else:
            try:
                f = open(path, "r")
                fileContent = f.read()
                f.close()
            except Exception as e:
                print(e)
                fileContent = ''
            content += fileContent
        content += "</textarea>"
        return content

    def save_file(self, path, content):

        if not self.localDeployment or os.path.commonprefix((os.path.realpath(path), self.safePath)) != self.safePath:
            return False
        try:
            f = open(path, "w")
            f.write(content)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
