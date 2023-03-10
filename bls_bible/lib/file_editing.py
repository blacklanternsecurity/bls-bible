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

import os


class file_editing:
    def __init__(self, localPath, localDeployment, parent, safePath):

        self.localPath = localPath
        self.localDeployment = localDeployment
        self.parent = parent
        self.safePath = safePath

    def edit_file(self, path):

        if self.localDeployment != "True":
            return False
        content = ""
        if os.path.commonprefix(
            (os.path.realpath(path), os.path.realpath(self.safePath))
        ) != os.path.realpath(self.safePath):
            content += "# Stop trying to look at my private parts :P"
        else:
            try:
                f = open(path, "r")
                fileContent = f.read()
                f.close()
            except Exception as e:
                print(e)
                fileContent = ""
            content += fileContent
        return content

    def save_file(self, path, content):

        if self.localDeployment != "True" or os.path.commonprefix(
            (os.path.realpath(path), os.path.realpath(self.safePath))
        ) != os.path.realpath(self.safePath):
            return False
        if not os.path.exists(os.path.realpath(path)):
            return False
        try:
            f = open(path, "w")
            f.write(content)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
