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
# tags.py

import json
import os
import logging
import re
import yaml
import frontmatter
from pathlib import Path


class Tags:

	def __init__(self, local_path, json_file):
		self.local_path = Path(local_path)
		self.json_file = json_file

	# Loose tagging
	# # Create Methods
	def create_filename_tags(self, search_path):
		# Attempts to create 'Loose' tags based on filenames
		whitelist = ['.md', '.markdown', '.yml', '.yaml']
		filename_tags = {}
		for (base, dirs, files) in os.walk(search_path):
			for file in files:
				if file.split('.')[-1] not in whitelist:
					continue  # Whitelisting .md .markdown .yml .yaml
				no_extension = '.'.join(file.split('.')[:-1])  # Removing extension
				if re.search("[0-9]{3}", no_extension.split('_')[0]):
					filename_words = no_extension.split('_')[1:]  # Removing the numbering
				else:
					filename_words = no_extension.split('_')
				for word in filename_words:
					if '#@' + word.upper() in filename_tags:  # If the tag exists
						filename_tags['#@' + word.upper()].append(
							os.path.join(base, file)  # Add our file to the tag's array
						)
					else:  # If the tag doesn't exist yet
						filename_tags['#@' + word.upper()] = [
							os.path.join(base, file)  # Create tag's array with file
						]
		# filename_tags should be fully populated
		# Try to get the current tag_index
		tag_data = self.get_tag_index()

		# Make sure 'Loose' is defined
		if 'Loose' not in tag_data:
			tag_data['Loose'] = {}

		# For each of our tags to add, add the tag and the tags files
		for tag, new_files in filename_tags.items():
			if tag in tag_data['Loose']:
				existing_files = tag_data['Loose'][tag]  # Take the file list present
				combined_files = existing_files.extend(new_files)  # Combine with the new files
				unique_files_set = set(combined_files)  # Convert to set to remove duplicates
			else:  # the tag is not currently in the 'Loose' tag_data
				unique_files_set = set(new_files)
			tag_data['Loose'][tag] = list(unique_files_set)  # Assign the new list to the tag

		# Save the new tag_index
		passing = self.save_tag_index(tag_data)
		return passing

	def create_location_tags(self, search_path):
		# Attempts to create tags and their files based on the name of the Directory they are in
		location_tags = {}
		for (base, dirs, files) in os.walk(search_path):
			base_parts = Path(base).parts  # Returns each directory in the path
			for part in base_parts:
				directory_words = part.split('_')
				for directory_word in directory_words:
					# Clean the word to remove '(' and ')'
					clean_word = directory_word.replace(')', '').replace('(', '')
					if '#@' + clean_word.upper() in location_tags:
						location_tags['#@' + clean_word.upper()].extend(files)
					else:
						location_tags['#@' + clean_word.upper()] = files

		# Now we need to add our collected tags to the tag index
		tag_data = self.get_tag_index()

		# Make sure 'Loose' is defined
		if 'Loose' not in tag_data:
			tag_data['Loose'] = {}

		# For each of our tags to add, add the tag and the tag files
		for tag, new_files in location_tags.items():
			if tag in tag_data['Loose']:
				existing_files = tag_data['Loose'][tag]  # Take the file list present
				combined_files = existing_files.extend(new_files)  # Combine with the new files
				unique_files_set = set(combined_files)  # Convert to set to remove duplicates
			else:  # The tag is not currently in the 'Loose' tag_data
				unique_files_set = set(new_files)
			tag_data['Loose'][tag] = list(unique_files_set)  # Assign the new list to the tag

		# Save the new tag_index
		passing = self.save_tag_index(tag_data)
		return passing

	def create_loose_tags(self):
		# Will attempt to create all 'Loose' type tags
		full_path = self.get_data_path()
		passing = self.create_filename_tags(full_path) and \
			self.create_location_tags(full_path)
		if not passing:
			logging.warning("'Loose' tag creation failed.")
		return passing

	# # Get Methods
	def get_loose_tags(self):
		# Returns all tags and their files for 'Loose' type tags
		tag_data = self.get_tag_index()
		if 'Loose' in tag_data:
			return tag_data['Loose']
		else:
			logging.warning(f"'Loose' tags were not found in {self.json_file}")
			return False

	# Moderate tagging
	# # Create Methods
	def create_caught_by_tags(self, search_path):
		# Creates tags based on YAML field in psalms->files->actions->caught by
		caught_by_tags = {}
		for base, dirs, files in os.walk(search_path):
			for file in files:
				b = Path(base)
				p = b / file
				try:
					with p.open() as f:
						psalm = yaml.load(f, Loader=yaml.Loader)
				except Exception as e:
					logging.warning(f"Unable to load yaml file {str(p)}")
					logging.error(e)
				if 'actions' in psalm:
					for action in psalm['actions']:
						if 'caught by' in action:
							for product in action['caught by']:
								# We are associating the location of the YAML document to the tag
								if '#@' + product.upper() in caught_by_tags:
									caught_by_tags['#@' + product.upper()].append(str(p))
								else:
									caught_by_tags['#@' + product.upper()] = [str(p)]
						else:
							logging.warning(f"'caught by' field missing from an action in {str(p)}")
							continue
				else:
					logging.warning(f"'actions' field missing from {str(p)}")
					continue

		# We should have fully created our Caught By tags
		# Add them to the tag index
		tag_data = self.get_tag_index()

		# Make sure 'Moderate' tags are present
		if 'Moderate' not in tag_data:
			tag_data['Moderate'] = {}

		# Make sure 'Caught By' tags are present
		if 'Caught By' not in tag_data['Moderate']:
			tag_data['Moderate']['Caught By'] = {}

		for tag, files in caught_by_tags.items():
			if tag in tag_data['Moderate']['Caught By']:  # If the tag is already in our collection we need to add the new files
				existing_list = tag_data['Moderate']['Caught By'][tag]
				combined_list = existing_list.extend(files)
				unique_set = set(combined_list)
			else:  # If the tag is not in the collection, then create the tag and the files
				unique_set = set(files)
			tag_data['Moderate']['Caught By'][tag] = list(unique_set)

		# Attempt to save
		passing = self.save_tag_index(tag_data)
		return passing

	def create_uncaught_by_tags(self, search_path):
		# Creates tags based on YAML field in psalms->files->actions->uncaught by
		uncaught_by_tags = {}
		for base, dirs, files in os.walk(search_path):
			for file in files:
				b = Path(base)
				p = b / file
				try:
					with p.open() as f:
						psalm = yaml.load(f, Loader=yaml.Loader)
				except Exception as e:
					logging.warning(f"Unable to load yaml file {str(p)}")
					logging.error(e)
				if 'actions' in psalm:
					for action in psalm['actions']:
						if 'uncaught by' in action:
							for product in action['uncaught by']:
								# We are associating the location of the YAML document to the tag
								if '#@' + product.upper() in uncaught_by_tags:
									uncaught_by_tags['#@' + product.upper()].append(str(p))
								else:
									uncaught_by_tags['#@' + product.upper()] = [str(p)]
						else:
							logging.warning(f"'uncaught by' field missing from an action in {str(p)}")
							continue
				else:
					logging.warning(f"'actions' field missing from {str(p)}")
					continue

		# We should have fully created our Uncaught By tags
		# Add them to the tag index
		tag_data = self.get_tag_index()

		# Make sure 'Moderate' tags are present
		if 'Moderate' not in tag_data:
			tag_data['Moderate'] = {}

		# Make sure 'Uncaught By' tags are present
		if 'Uncaught By' not in tag_data['Moderate']:
			tag_data['Moderate']['Uncaught By'] = {}

		for tag, files in uncaught_by_tags.items():
			# If the tag is already in our collection we need to add the new files
			if tag in tag_data['Moderate']['Uncaught By']:
				existing_list = tag_data['Moderate']['Uncaught By'][tag]
				combined_list = existing_list.extend(files)
				unique_set = set(combined_list)
			else:  # If the tag is not in the collection, then create the tag and the files
				unique_set = set(files)
			tag_data['Moderate']['Uncaught By'][tag] = list(unique_set)

		# Attempt to save
		passing = self.save_tag_index(tag_data)
		return passing

	def create_tool_actions_tags(self, search_path):
		# TODO: This was not fully defined. Each tool should have a collection of
		#  actions that are tagged somehow.
		return False

	def create_moderate_tags(self):
		# Will attempt to create all 'Moderate' type tags
		full_tool_path = self.get_psalms_path()
		passing = self.create_caught_by_tags(full_tool_path) and \
			self.create_uncaught_by_tags(full_tool_path) and \
			self.create_tool_actions_tags(full_tool_path)
		if not passing:
			logging.warning("'Moderate' tag creation failed.")
		return passing

	# # Get Methods
	def get_moderate_tags(self):
		# Returns all 'Moderate' type tags
		tag_data = self.get_tag_index()
		if 'Moderate' in tag_data:
			return tag_data['Moderate']
		else:
			logging.warning(f"'Moderate' tags were not found in {self.json_file}")
			return False

	def get_caught_by_tags(self):
		# Returns tags and their YAML files that are marked 'Caught By'
		tag_data = self.get_tag_index()
		if 'Moderate' in tag_data:
			if 'Caught By' in tag_data['Moderate']:
				return tag_data['Moderate']['Caught By']
			else:
				logging.warning(f"'Caught By' tags were not found in {self.json_file}")
				return False
		else:
			logging.warning(f"'Moderate' tags were not found in {self.json_file}")
			return False

	def get_uncaught_by_tags(self):
		# Returns tags and their YAML files that are marked 'Uncaught By'
		tag_data = self.get_tag_index()
		if 'Moderate' in tag_data:
			if 'Uncaught By' in tag_data['Moderate']:
				return tag_data['Moderate']['Uncaught By']
			else:
				logging.warning(f"'Uncaught By' tags were not found in {self.json_file}")
				return False
		else:
			logging.warning(f"'Moderate' tags were not found in {self.json_file}")
			return False

	def get_tool_actions_tags(self):
		# TODO: This method is a placeholder for when create_tool_actions_tags is defined
		return False

	# Strict tagging
	# # Create Methods
	def create_inclusive_tags(self, search_path):
		# Attempts to gather all of the inclusive tags from the data files
		inclusive_tags = {}
		for base, dirs, files in os.walk(search_path):
			for file in files:
				b = Path(base)
				p = b / file
				with p.open() as f:
					data_file = frontmatter.load(f)
				if 'tags' in data_file:
					if 'inclusive' in data_file['tags']:
						for tag in data_file['tags']['inclusive']:
							if '#@' + tag.upper() in inclusive_tags:
								inclusive_tags['#@' + tag.upper()].append(str(p))
							else:
								inclusive_tags['#@' + tag.upper()] = [str(p)]
					else:
						logging.warning(f"'inclusive' field missing from {str(p)} frontmatter")
						continue
				else:
					logging.warning(f"'tags' field missing from {str(p)} frontmatter")
					continue

		# We should have collected all of our inclusive tags now

		# Pull in the existing tag data
		tag_data = self.get_tag_index()

		# Make sure 'Strict' tags are present
		if 'Strict' not in tag_data:
			tag_data['Strict'] = {}

		# Make sure 'Inclusive' tags are present
		if 'Inclusive' not in tag_data['Strict']:
			tag_data['Strict']['Inclusive'] = {}

		# Combine existing data with new data and remove duplicates
		for tag, files in inclusive_tags.items():
			if tag in tag_data['Strict']['Inclusive']:
				existing_list = tag_data['Strict']['Inclusive'][tag]
				combined_list = existing_list.extend(files)
				unique_set = set(combined_list)
			else:
				unique_set = set(files)
			tag_data['Strict']['Inclusive'][tag] = list(unique_set)

		# Try to save the tag index
		passing = self.save_tag_index(tag_data)
		return passing

	def create_exclusive_tags(self, search_path):
		# Attempts to gather all of the exclusive tags from the data files
		exclusive_tags = {}
		for base, dirs, files in os.walk(search_path):
			for file in files:
				b = Path(base)
				p = b / file
				with p.open() as f:
					data_file = frontmatter.load(f)
				if 'tags' in data_file:
					if 'exclusive' in data_file['tags']:
						for tag in data_file['tags']['exclusive']:
							if '#@' + tag.upper() in exclusive_tags:
								exclusive_tags['#@' + tag.upper()].append(str(p))
							else:
								exclusive_tags['#@' + tag.upper()] = [str(p)]
					else:
						logging.warning(f"'exclusive' field missing from {str(p)} frontmatter")
						continue
				else:
					logging.warning(f"'tags' field missing from {str(p)} frontmatter")
					continue

		# We should have collected all of our exclusive tags now

		# Pull in the existing tag data
		tag_data = self.get_tag_index()

		# Make sure 'Strict' tags are present
		if 'Strict' not in tag_data:
			tag_data['Strict'] = {}

		# Make sure 'Inclusive' tags are present
		if 'Exclusive' not in tag_data['Strict']:
			tag_data['Strict']['Exclusive'] = {}

		# Combine existing data with new data and remove duplicates
		for tag, files in exclusive_tags.items():
			if tag in tag_data['Strict']['Exclusive']:
				existing_list = tag_data['Strict']['Exclusive'][tag]
				combined_list = existing_list.extend(files)
				unique_set = set(combined_list)
			else:
				unique_set = set(files)
			tag_data['Strict']['Exclusive'][tag] = list(unique_set)

		# Try to save the tag index
		passing = self.save_tag_index(tag_data)
		return passing

	def create_tools_tags(self, search_path):
		# TODO: Should create a collection of tag collections. Each category should
		#  be by execution environment (windows/linux/wsl/mono/etc).
		#  Each category should contain tags for the tool names and
		#  the files referencing them. This is not fully ironed out
		return False

	def create_strict_tags(self):
		# Will attempt to create all of the 'Strict' typed tags
		full_data_path = self.get_data_path()
		full_tool_path = self.get_psalms_path()
		passing = self.create_inclusive_tags(full_data_path) and \
			self.create_exclusive_tags(full_data_path) and \
			self.create_tools_tags(full_tool_path)
		if not passing:
			logging.warning("Strict tag creation failed.")
		return passing

	# # Get Methods
	def get_strict_tags(self):
		# Returns all 'Strict' type tags
		tag_data = self.get_tag_index()
		if 'Strict' in tag_data:
			return tag_data['Strict']
		else:
			logging.warning(f"'Strict' tags were not found in {self.json_file}")
			return False

	def get_tools_tags(self):
		# TODO: Placeholder method for when create_tools_tags is defined
		return False

	def get_exclusive_tags(self):
		# Only returns tags and their files that were specified as 'Exclusive'
		tag_data = self.get_tag_index()
		if 'Strict' in tag_data:
			if 'Exclusive' in tag_data['Strict']:
				return tag_data['Strict']['Exclusive']
			else:
				logging.warning(f"'Exclusive' tags were not found in {self.json_file}")
				return False
		else:
			logging.warning(f"'Strict' tags were not found in {self.json_file}")
			return False

	def get_inclusive_tags(self):
		# Only returns tags and their files that were specified as 'Inclusive'
		tag_data = self.get_tag_index()
		if 'Strict' in tag_data:
			if 'Inclusive' in tag_data['Strict']:
				return tag_data['Strict']['Inclusive']
			else:
				logging.warning(f"'Inclusive' tags were not found in {self.json_file}")
				return False
		else:
			logging.warning(f"'Strict' tags were not found in {self.json_file}")
			return False

	# Helpers
	def reinitialize_tag_index(self):
		# WARNING: This will erase the current tag index
		# Following is the tag index skeletal structure
		tag_data = {
			'Loose': {},  # Loose tags are used only for search, comprised of filename and file location based tags
			'Moderate': {  # Used by search and WADCOMs
				'Caught By': {},  # From the 'Caught By' field in Psalms YAML
				'Uncaught By': {},  # From the 'Uncaught By' field in Psalms YAML
				'Actions': {}  # From the Psalms YAML somehow, unsure currently
			}, 'Strict': {  # Used by search, WADCOMs, and Install
				'Inclusive': {},  # From the 'Inclusive' field in Data YAML
				'Exclusive': {},  # From the 'Exclusive' field in Data YAML
				'Tools': {  # From the Psalms YAML somehow, unsure currently
					'Windows': {},
					'Linux': {},
					'WSL': {},
					'mono': {},
					'pwsh': {},
					'c2': {}
				}
			}
		}
		try:
			full_path = self.get_index_path()
			f = open(full_path, 'w+')
			json.dump(tag_data, f)
			f.close()
		except Exception as e:
			logging.warning(f"Unable to serialize data to {self.json_file}")
			logging.error(e)
			return False
		return True

	def populate_tag_index(self):
		# This will attempt to execute all three major tag sections create functionalities
		# This should build out all available tags
		passing = self.create_loose_tags() and \
			self.create_moderate_tags() and \
			self.create_strict_tags()
		if not passing:
			logging.warning(f"Unable to populate tag index.")
		return passing

	def get_tag_index(self):
		# Returns the full tag index
		full_path = self.get_index_path()
		try:
			f = open(full_path)
			tag_data = json.load(f)
			f.close()
		except Exception as e:
			logging.warning(f"Unable to deserialize {self.json_file}")
			logging.error(e)
			return False
		return tag_data

	def save_tag_index(self, tag_data):
		# Attempts to update the existing tag index
		full_path = self.get_index_path()
		try:
			f = open(full_path, 'w+')
			json.dump(tag_data, f)
			f.close()
		except Exception as e:
			logging.warning(f"Unable to serialize tag data to {self.json_file}")
			logging.error(e)
			return False
		return True

	def get_psalms_path(self):
		# Used for finding tags in the Psalms files
		return self.get_data_path() / 'Psalms'

	def get_data_path(self):
		# Used for finding tags in the Data files
		return self.local_path / 'Data' / 'Testaments_and_Books'

	def get_index_path(self):
		# Used for reading from and writing to the tag index
		return self.local_path / 'bls_bible' / 'static' / + self.json_file
