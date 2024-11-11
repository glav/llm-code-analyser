import asyncio
from argparse import ArgumentParser

from code_query_engine import CodeQueryEngine
from config import show_config
from image_comparison_engine import ImageComparisonEngine


async def main(args):
    if args.solution_path:
        engine = CodeQueryEngine(args.solution_path)
        await engine.execute_async()
    else:
        engine = ImageComparisonEngine(args.ref_image_path, args.target_image_path)
        await engine.execute_async()


if __name__ == "__main__":
    parser = ArgumentParser(description="Process solution path")
    parser.add_argument(
        "--solution-path", type=str, required=False, help="Path to the solution files"
    )
    parser.add_argument(
        "--ref-image-path",
        type=str,
        required=False,
        help="The reference architecture image to compare with",
    )
    parser.add_argument(
        "--target-image-path",
        type=str,
        required=False,
        help="The target architecture image to compare against the reference architecture image",
    )

    args = parser.parse_args()
    if not args.solution_path and not (args.ref_image_path and args.target_image_path):
        parser.print_help()
        exit(1)
    if args.solution_path and (args.ref_image_path or args.target_image_path):
        parser.print_help()
        exit(1)

    show_config(args)

    asyncio.run(main(args))
