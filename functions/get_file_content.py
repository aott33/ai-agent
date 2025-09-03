from google.genai import types
import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
	try:
		file_content_string = ""

		fullpath = os.path.join(working_directory, file_path)
	
		working_dir_resolved = os.path.abspath(working_directory)
		fullpath_resolved = os.path.abspath(fullpath)

		if not fullpath_resolved.startswith(working_dir_resolved + os.sep) and fullpath_resolved != working_dir_resolved:
			return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(fullpath_resolved):
			return f'Error: File not found or is not a regular file: "{file_path}"'

		with open(fullpath_resolved, "r") as f:
			file_content_string = f.read(MAX_CHARS)
			
			current_position = f.tell()
			f.seek(0, os.SEEK_END)
			end_position = f.tell()
			
			if end_position > MAX_CHARS:
				file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
				
		return file_content_string

	except Exception as e:
		return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Returns the contents of the file. Truncates if the file has 10,000 or more characterse",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The filepath to read content from, relative to the working directory. If not provided, returns error message.",
			),
		},
	),
)
