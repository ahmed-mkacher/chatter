import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write passed in content into the targeted file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the targeted file",
            )
        },
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        pwd: str = os.path.abspath(working_directory)
        file: str = os.path.normpath(os.path.join(pwd, file_path))
        valid_target_file: bool = os.path.commonpath([pwd, file]) == pwd

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file), exist_ok=True)

        with open(file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"error: {str(e)}"
