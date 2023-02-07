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
# config.py
import os
import json


class config_management:
    def __init__(self):

        self.localPath = os.path.abspath(os.path.join(os.getcwd())) + "/"
        self.config_file = self.localPath + "bls_bible/app_config.json"
        self.default_config_file = (
            self.localPath + "bls_bible/default_app_config.json"
        )
        self.config = self.load_app_config()

    def list_configs(self):

        config_file_read = open(self.config_file, "r")
        config_file_jsondata = json.load(config_file_read)
        config_file_read.close()

        for configs, values in config_file_jsondata.items():
            print(configs, "\n", values, "\n")

        return True

    def new_app_config(
        self,
        newToken,
        newDomain,
        newRepo,
        newId,
        newBranch,
        newParent,
        newSource,
        newLocalDeployment,
        Assessalonians_Repo,
        bitwarden_server,
        bls_bible_server,
    ):

        json_data = {
            "token": newToken,
            "repo": newRepo,
            "branch": newBranch,
            "parent": newParent,
            "source": newSource,
            "localDeployment": newLocalDeployment,
            "Assessalonians_Repo": Assessalonians_Repo,
            "id": newId,
            "domain": newDomain,
            "bitwarden_server": bitwarden_server,
            "bls_bible_server": bls_bible_server,
        }

        with open(self.config_file, "w+") as outfile:
            json.dump(json_data, outfile, indent=4)
        return True

    def update_app_config(self, key, value):
        file_jsondata = json.load(open(self.config_file))
        file_jsondata[key] = value
        with open(self.config_file, "w+") as file:
            json.dump(file_jsondata, file, indent=4)
        return file_jsondata

    def load_app_config(self):
        with open(self.config_file, "r") as infile:
            data = json.load(infile)
        return data

    def reset_default_configs(self):
        with open(self.default_config_file, "r") as infile:
            data = json.load(infile)

        with open(self.config_file, "w+") as outfile:
            json.dump(data, outfile, indent=4)

        return True
