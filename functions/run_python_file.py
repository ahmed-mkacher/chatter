import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        pwd: str = os.path.abspath(working_directory)
        file: str = os.path.normpath(os.path.join(pwd, file_path))
        valid_target_file: bool = os.path.commonpath([pwd, file]) == pwd

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file]
        command.extend(args or [])

        result: subprocess.CompletedProcess = subprocess.run(
            command, capture_output=True, text=True, timeout=30, check=True
        )

        output = ""

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}."

        if not (result.stderr or result.stdout):
            return "No output produced"

        if result.stderr:
            output += f"STDERR:\n{result.stderr}"

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
