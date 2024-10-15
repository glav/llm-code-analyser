import os
from datetime import datetime

import aiofiles


class ResultStore:
    def __init__(self, results_dir: str = "./_results/", descriptive_suffix: str = ""):
        self.results_dir: str = (
            results_dir if results_dir.endswith("/") else results_dir + "/"
        )
        self.result_name_suffix: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.descriptive_suffix: str = f"{descriptive_suffix}_" if not None else ""
        self.result_file_name = f"{self.results_dir}results_{self.descriptive_suffix}{self.result_name_suffix}.txt"

    async def add_result_to_store_async(self, result: str):
        await self._ensure_results_dir_exists_async()
        async with aiofiles.open(self.result_file_name, "a") as f:
            # for result in results:
            await f.write(f"{result}\n\n")

    async def _ensure_results_dir_exists_async(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    async def get_results_from_store_async(self):
        async with aiofiles.open(self.result_file_name, "r") as f:
            return await f.read()
