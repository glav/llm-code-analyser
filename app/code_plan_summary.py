import json

import aiofiles


class CodePlanSummary:
    def __init__(self, result_json_file):
        self.result_json_file = result_json_file

    async def aggregate_dependency_actions(self):
        async def read_json_file(file_path):
            async with aiofiles.open(file_path, "r") as f:
                contents = await f.read()
                return json.loads(contents)

        dependency_list = []
        change_list = []
        json_data = await read_json_file(self.result_json_file)

        for result in json_data["Details"]:
            if result["Dependencies"] == "None":
                continue
            temp_dep_list = [dep.strip() for dep in result["Dependencies"].split(",")]
            for dep in temp_dep_list:
                if dep not in dependency_list:
                    dependency_list.append(dep)

        tmp_list = []
        for result in json_data["Details"]:
            if (
                "Changes" not in result
                or not result["Changes"]
                or result["Changes"] == "None"
            ):
                continue

            for chg in result["Changes"]:
                if chg["Dependency"] not in tmp_list:
                    change_list.append(
                        {
                            "Dependency": chg["Dependency"],
                            "Action": chg["Action"],
                        }
                    )
                    tmp_list.append(chg["Dependency"])

        return dependency_list, change_list
