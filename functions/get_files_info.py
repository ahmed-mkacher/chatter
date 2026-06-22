import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        pwd: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(pwd, directory))

        valid_target_dir: bool = os.path.commonpath([pwd, target_dir]) == pwd
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files: list[str] = os.listdir(target_dir)
        file_info: list[tuple[int, bool]] = list(
            map(
                lambda file: (
                    os.path.getsize(f"{target_dir}/{file}"),
                    os.path.isdir(f"{target_dir}/{file}"),
                ),
                files,
            )
        )

        file_details: dict[str, tuple[int, bool]] = dict(zip(files, file_info))
        result: str = "\n".join(
            list(
                map(
                    lambda file: (
                        f"- {file}: file_size={file_details[file][0]} bytes, is_dir={file_details[file][1]}"
                    ),
                    file_details.keys(),
                )
            )
        )

        return result

    except Exception as e:
        return f"Error: {str(e)}"
