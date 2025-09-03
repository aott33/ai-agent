from google.genai import types 
import os

def write_file(working_directory, file_path, content):
	try:
		fullpath = os.path.join(working_directory, file_path)
	
		working_dir_resolved = os.path.abspath(working_directory)
		fullpath_resolved = os.path.abspath(fullpath)

		if not fullpath_resolved.startswith(working_dir_resolved + os.sep) and fullpath_resolved != working_dir_resolved:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

		with open(fullpath_resolved, "w") as f:
			f.write(content)

		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

	except Exception as e:
		return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Writes content to a file within a specified working directory, ensuring the file path remains within security boundaries.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="Relative path within the working directory where the file should be created or overwritten with the provided content.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="String content to write to the specified file, completely replacing any existing content in the target file.",
			),
		},
	),
)
