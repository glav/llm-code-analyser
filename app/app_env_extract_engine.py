import os
import re

import config
from result_store import ResultStore
from solution_file_reader import SolutionFileReader


class AppEnvExtractEngine:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        # self.llm_client = LlmClient()

    async def execute_async(self):
        src_main_resources_path = os.path.join(
            self.base_dir, "src", "main", "resources"
        )
        if not os.path.exists(src_main_resources_path):
            print(f"ERROR: Directory {src_main_resources_path} does not exist.")
            return
        solution_file_reader = SolutionFileReader(base_dir=src_main_resources_path)

        files = await solution_file_reader.get_all_files_async()
        num_files = len(files)
        print(f"..First pass\n..Found {num_files} files")

        result_store = ResultStore(
            descriptive_suffix=f"{config.LOCAL_LLM_MODEL_NAME}_env"
            if config.LLM_MODE == "local"
            else f"{config.LLM_MODE}_{config.AZURE_LLM_MODEL_NAME}_env",
            results_file_extension="json",
        )
        await result_store.add_result_to_store_async("{\n")

        cnt = 0
        for file in files:
            cnt += 1
            print(f"..Reading file: {file}")

            ## need to chunk here
            # content_to_submit = f"Filename: [{file}]\n{contents}"

            print(f".. [{cnt}/{num_files}] Querying code in file: {file}")
            if not file.endswith(".properties"):
                continue

            if "._application" in file:
                continue

            # Remove '.application-' and '.properties' from the file name
            match = re.search(r"application-([^.]+)\.properties$", file)

            if match:
                env_name = match.group(1)
            else:
                env_name = "application"

            contents = await solution_file_reader.read_contents_async(file)
            json_element = f'"{env_name}": [\n'
            if cnt > 1:
                json_element = "," + json_element
            await result_store.add_result_to_store_async(json_element)

            line_cnt = 0
            for line in contents.splitlines():
                if not line.strip().startswith("#"):
                    if "=" in line:
                        line_cnt += 1
                        key, value = line.split("=", 1)
                        json_element = f'"{key.strip()}": "{value.strip()}"'
                        json_element = "{" + json_element + "}"
                        if line_cnt > 1:
                            json_element = f",\n{json_element}"
                        await result_store.add_result_to_store_async(json_element)

            await result_store.add_result_to_store_async("]\n")

        await result_store.add_result_to_store_async("}\n")
        print(f"..Results stored in: {result_store.result_file_name}")
        self.result_file = result_store.result_file_name
