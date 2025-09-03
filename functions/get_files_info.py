import os

def get_files_info(working_directory, directory="."):
    try:

        folder_contents = ""

        fullpath = os.path.join(working_directory, directory)
    
        working_dir_resolved = os.path.abspath(working_directory)
        fullpath_resolved = os.path.abspath(fullpath)

        if not fullpath_resolved.startswith(working_dir_resolved + os.sep) and fullpath_resolved != working_dir_resolved:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(fullpath_resolved):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(fullpath_resolved)

        for item in dir_contents:
            filename = item
            filepath = os.path.join(fullpath_resolved, filename)

            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)

            folder_contents = folder_contents + f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}\n"
        
        return folder_contents

    except Exception as e:
        return f"Error: {str(e)}"
