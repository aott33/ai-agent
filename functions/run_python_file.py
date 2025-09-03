import subprocess
import os

def run_python_file(working_directory, file_path, args=[]):
	try:

		file_content_string = ""

		fullpath = os.path.join(working_directory, file_path)
	
		working_dir_resolved = os.path.abspath(working_directory)
		fullpath_resolved = os.path.abspath(fullpath)

		if not fullpath_resolved.startswith(working_dir_resolved + os.sep) and fullpath_resolved != working_dir_resolved:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(fullpath_resolved):
			return f'Error: File "{file_path}" not found"'
		if not file_path.endswith('.py'):
			return f'Error: {file_path} is not a python file'
		
		run_process_args = ['python3', fullpath_resolved]

		if len(args) > 0:
			run_process_args += args

		completed_object = subprocess.run(run_process_args, timeout=30, capture_output=True)
				
		return_string = f'STDOUT: str({completed_object.stdout})\n'
		return_string += f'STDERR: str({completed_object.stderr})\n'
		
		return_code = completed_object.returncode 
		if return_code != 0:
			return_string += f'Process exited with code {return_code}'

		if completed_object.stdout == None:
			return 'No output produced.'

		return return_string

	except Exception as e:
		return f"Error: executing Python file {str(e)}"   
