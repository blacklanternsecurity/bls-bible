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
# app.py

from flask import Flask, request, url_for, g, redirect
from functools import wraps
import urllib3, os
import json

# from bls_bible.lib.app.api import api_service
from bls_bible.lib.app.app_core import app_core
from bls_bible.lib.app.app_ops import app_ops
from bls_bible.lib.app.app_dev import app_dev
from bls_bible.lib.app.api import api_service
from bls_bible.lib.service import BibleService


# from bls_bible.config.args import parseArgs
# from bls_bible.lib.verse_of_the_day import verse_of_the_day


class application_service:
    def __init__(self, server_type="central"):

        self.app = Flask(__name__, static_url_path="", static_folder="static")

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.Bs = BibleService()
        self.server_type = server_type

    def appService(self, host, debug=False):
        def checkAppKey(fn):
            return False

        # def inner(*args, **kwargs): #appkey should be in kwargs
        # try:
        # Bs.API_Key_Validation(api_key)
        # except KeyError:
        # Whatever other errors can raise up such as db inaccessible
        # We were able to access that API key, so pass onward.
        # If you know nothing else will use the appkey after this, you can unset it.
        # return fn(*args, **kwargs)
        # return inner

        current_user = None

        @self.app.before_request
        def before_request():
            g.user = current_user

        def login_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if g.user is None:
                    return redirect(url_for("login_page", next=request.url))
                return f(*args, **kwargs)

            return decorated_function

        def server_type_central_required(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if self.server_type != "central":
                    return redirect(url_for("login_page", next=request.url))
                return f(*args, **kwargs)

            return decorated_function

        @self.app.route("/login")
        def login_page():
            return self.app.send_static_file("login.html")

        @self.app.route("/")
        def index():
            if self.server_type == "central":
                return self.app.send_static_file("index_central.html")
            else:
                return self.app.send_static_file("index.html")

        if not os.path.exists("static/ttp.json"):
            self.Bs.update.update_json_file()
            self.Bs.fileIndexer()
            self.Bs.get_reverse_references()

        self.app_core = app_core(self.app)
        self.app_core.app_core_content()

        if (self.server_type == "ops") or (self.server_type == "dev"):
            self.app_ops = app_ops(self.app)
            self.app_ops.app_ops_content()
            self.api_service = api_service(self.app)
            self.api_service.api_routing()
            with open("./app_config.json", "r") as f:
                j_dat = json.load(f)
            j_dat["localDeployment"] = "True"
            with open("./app_config.json", "w") as f:
                json.dump(j_dat, f)
        else:
            with open("./app_config.json", "r") as f:
                j_dat = json.load(f)
            j_dat["localDeployment"] = "False"
            with open("./app_config.json", "w") as f:
                json.dump(j_dat, f)

        if self.server_type == "dev":
            self.app_dev = app_dev(self.app)
            self.app_dev.app_dev_content()

        self.app.run(host=host, debug=debug)
