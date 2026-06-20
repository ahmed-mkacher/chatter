import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        pwd = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(pwd, directory))

        valid_target_dir = os.path.commonpath([pwd, target_dir]) == pwd
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(target_dir)
        file_info = list(
            map(
                lambda file: (
                    os.path.getsize(f"{target_dir}/{file}"),
                    os.path.isdir(f"{target_dir}/{file}"),
                ),
                files,
            )
        )

        file_details = dict(zip(files, file_info))
        result = "\n".join(
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
