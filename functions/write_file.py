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
