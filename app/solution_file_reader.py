import pathlib

import aiofiles

file_type_exclusion_list = [
    ".env",
    ".gitignore",
    ".git",
    ".idea",
    ".pyc",
    ".DS_Store",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".venv",
    ".cache",
    ".egg-info",
    ".eggs",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    "__pycache__",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".conf",
    ".xml",
    ".yaml",  # May want to change this and include YAMl to describe any infra
]

directory_exclusion_list = [
    ".git",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".cache",
    ".devcontainer",
    ".vscode",
    "_results",
]

file_exclusion_list = ["requirements.txt", "requirements-dev.txt", "requirements.in"]


class SolutionFileReader:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    async def get_all_files_async(self):
        base_dir = pathlib.Path(self.base_dir)
        return [
            str(file)
            for file in base_dir.rglob("*")
            if file.suffix not in file_type_exclusion_list
            and not any(
                excluded_dir in file.parts for excluded_dir in directory_exclusion_list
            )
            and not any(
                file_type_exclude in file.parts
                for file_type_exclude in file_type_exclusion_list
            )
            and not any(
                file_exclude in file.parts for file_exclude in file_exclusion_list
            )
            and not file.is_dir()
        ]

    async def read_contents_async(self, file_path) -> str:
        async with aiofiles.open(file_path, "r") as file:
            return await file.read()
