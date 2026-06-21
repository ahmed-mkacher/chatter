import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        pwd: str = os.path.abspath(working_directory)
        file: str = os.path.normpath(os.path.join(pwd, file_path))
        valid_target_file: bool = os.path.commonpath([pwd, file]) == pwd

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file, "r") as f:
            content: str = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {str(e)}"
