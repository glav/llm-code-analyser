import asyncio
from solution_file_reader import SolutionFileReader
from argparse import ArgumentParser
import config


async def main(solution_path):
    reader = SolutionFileReader(solution_path)
    files = await reader.get_all_files()
    for file in files:
        print(f"Reading file: {file}")
        # contents = await reader.read_contents_async(file)


if __name__ == "__main__":
    parser = ArgumentParser(description="Process solution path")
    parser.add_argument(
        "--solutionpath", type=str, required=True, help="Path to the solution files"
    )
    args = parser.parse_args()

    asyncio.run(main(args.solutionpath))
