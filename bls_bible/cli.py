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
# cli.py
from getpass import getpass

from bls_bible.lib.service import BibleService
from bls_bible.app import application_service
from bls_bible.lib.cli.args import parseArgs
#from bls_bible.lib.installer import DepsInstaller
#from bls_bible.lib.cli.cli_tables import campaign_tables, threat_profile_tables

#campaign_tables = campaign_tables()
#threat_profile_tables = threat_profile_tables()
options = parseArgs()


def main():
	Bs = BibleService()
	# config workflow
	if options.subcommand == 'config':
		if options.action == 'reset':
			Bs.reset_default_configs()
		if options.action == 'new':
			if options.non_interactive == True:
				print("ok")
#				Bs.new_app_config(token, domain, repo, id, branch, parent, source, localPath, localDeployment)
			else:
				print("Please provide the following information.")
				token = input("Token: ")
				domain = input("domain: ")
				repo = input("repo: ")
				id = input("repo id: ")
				branch = input("repo branch: ")
				parent = input("parent: ")
				source = input("source: ")
				Assessalonians_Repo = input("Assessalonians_Repo: ")
				localDeployment = input("localDeployment: ")
				Bs.new_app_config(token, domain, repo, id, branch, parent, source, localDeployment, Assessalonians_Repo)
			print("Results:")
			Bs.list_configs()

		if options.action == 'update':
			if (options.config_value_choice == None) and (options.config_key_choice != None):
				value = input("Enter new value: ")
				Bs.update_app_config(options.config_key_choice, value)
			elif options.secrets:
				print("Leave options blank to not change. Note input is hidden.\n")
				bible_token = getpass("Select value for BLS Bible api key: ")
				ETM_token = getpass("Select value for ETM api key: ")
				if bible_token != '':
					Bs.update_app_config("token", bible_token)
				if ETM_token != '':
					Bs.update_app_config("ETM_api_key", ETM_token)
				print("Configs now: ", Bs.list_configs())
			else:
				try:
	#				Bs.list_configs()
					print(options.action)
					Bs.update_app_config(options.config_key_choice, options.config_value_choice)
	#				Bs.list_configs()
				except Exception as e:
					print("Exceptions: ", e)
				finally:
					print("Results:")
#		if options.action == 'git_repo ':
#			Bs.git_repo_update()
		
		if options.action == 'git_submodules':
			Bs.git_submodule_pull()

		if options.action == 'list':
			Bs.list_configs()
#		print(cfg.config)
	# "app server" workflow
	elif options.subcommand == 'server':
		Application_Service = application_service(options.server_type)
#		if options.action == 'configure':
		#application_service = application_service()
		if options.action == 'start':
			if options.server_type == 'central':
				print("server update frequency: TODO")
			print(f"Starting Serve Type: {options.server_type}")
			Application_Service.appService(options.bind, options.debug)
#		if options.action == 'stop': # TODO!
	# "update" workflow
	elif options.subcommand == 'update':
		if options.action == 'verses':
			print("Attempting verses update")
			Bs.update_verses()
		if options.action == 'local':
			print("Attempting local update")
			Bs.update.update_json_file()
			Bs.fileIndexer()
			Bs.get_reverse_references()
			print("Updated")
		if options.action == 'mitre':
			print("Attempting MITRE update")
			Bs.downloadMitreGroups()
			Bs.downloadLatestAttack()
			print("MITRE Updated")
		if options.action == 'assessalonians':
			Bs.git_assessalonians_pull()
		if options.action == 'git':
			Bs.git_submodule_pull()
#			Bs.git_repo_update()
		if options.action == 'integrations':
			print("Attempting integrations update")
			Bs.ETM_Data_Pull()
#			Bs.ETM_Analyze
		if options.action == 'full':
			print("Attempting full update")
			Bs.update.update_json_file()
			Bs.fileIndexer()
			Bs.get_reverse_references()
			Bs.downloadMitreGroups()
			Bs.downloadLatestAttack()
			print("Updated")
