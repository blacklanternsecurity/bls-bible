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
# args.py

import os
import sys
import argparse
import argcomplete
import textwrap

from termcolor import colored
from pathlib import Path
from argparse import RawTextHelpFormatter, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter, MetavarTypeHelpFormatter


from bls_bible.lib.service import BibleService

Bs = BibleService()

def highlight(text, color='yellow'):
	if color == 'yellow':
		return u'{}'.format(colored(text, 'yellow', attrs=['bold']))
	elif color == 'red':
		return u'{}'.format(colored(text, 'red', attrs=['bold']))

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

with open("pyproject.toml", "r") as fp:
    for line in lines_that_contain("version", fp):
        version = line
        break

version = version.split('"')[1]

VERSION = version
wrapper = textwrap.TextWrapper(width=70)

banner = f"""
	██████╗░██╗░░░░░░██████╗  ██████╗░██╗██████╗░██╗░░░░░███████╗
	██╔══██╗██║░░░░░██╔════╝  ██╔══██╗██║██╔══██╗██║░░░░░██╔════╝
	██████╦╝██║░░░░░╚█████╗░  ██████╦╝██║██████╦╝██║░░░░░█████╗░░
	██╔══██╗██║░░░░░░╚═══██╗  ██╔══██╗██║██╔══██╗██║░░░░░██╔══╝░░
	██████╦╝███████╗██████╔╝  ██████╦╝██║██████╦╝███████╗███████╗
	╚═════╝░╚══════╝╚═════╝░  ╚═════╝░╚═╝╚═════╝░╚══════╝╚══════╝

				{colored(VERSION, "magenta")}

{highlight('Verse of the Day', 'red')}: {highlight(wrapper.fill(Bs.verse_of_the_day()))}

  				by
	
	Thomas Presto (@ThomasPresto1) and Cody Martin (@codymartin)
"""


def parseArgs():
	print(banner)
	print("\n\n")

	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

	subparsers = parser.add_subparsers(dest='subcommand')

	# 'Config' Subparsers
	parser_config_group = subparsers.add_parser('config', help='Configure the application.')
	parser_config_group.add_argument('action', choices=['list', 'new', 'update', 'reset'], help='*list*: List existing configuration. *new*: push an entirely new config. *update*: update a specific config value (combine with -k, optionally -v). *reset*: Overwrite existing config with the defaults.')
	parser_config_group.add_argument("-ni", "--non-interactive", action='store_true', help='Disable interactive app configuration in CLI. Default: Interactive mode.')
	parser_config_group.add_argument("-key", "--config-key-choice", type=str, choices=["domain", "ETM_Domain", "repo", "id", "branch", "parent", "source", "localDeployment", "Assessalonians_Repo"], help='Key config value to update (used with choice: update). You will be prompted for a value if one is not specified.')
	parser_config_group.add_argument("-sec", "--secrets", action='store_true', help='Update all secrets (great in first-time setup).')
	parser_config_group.add_argument("-val", "--config-value-choice", type=str, nargs='?', help='(Optional) Key config value to update (used with choice: update). You will be prompted for a value if one is not specified with -key.')

	# 'Server' Subparsers
	parser_server_group = subparsers.add_parser('server', help='Run server managing commands.')
	parser_server_group.add_argument('action', choices=['start', 'stop'], help='Start or stop a running server. Note: stop functionality not yet implemented.')
	parser_server_group.add_argument('server_type', const='central', nargs="?", choices=['central', 'ops', 'dev'], help='Choose type of server (ordered from most restrictive to least restrictive).')
	parser_server_group.add_argument("-b", "--bind", default="127.0.0.1", help='default: 127.0.0.1')
	parser_server_group.add_argument("-d", "--debug", action='store_true', help='Enable server debug mode. Note: Do not use in production as the server security is reduced. Default: Not enabled')
	# parser_server_group.add_argument("-fg", "--foreground", action='store_true', help='Run the application in the foreground to view live app logs.')

	# 'Update' Subparsers
	parser_update_group = subparsers.add_parser('update', help='Run update commands.')
	parser_update_group.add_argument('action', choices=['local', 'mitre', 'verses', 'integrations', 'git_repo', 'git', 'assessalonians', 'full'], help='Update local (indexes of local files), "mitre" (Remote MITRE ATT&CK data retrieval), or "full" (all aforementioned).')


	if len(sys.argv)==1:
		parser.print_help()
		parser.exit()

	#argcomplete.autocomplete(parser)
	options = parser.parse_args()
	return options

