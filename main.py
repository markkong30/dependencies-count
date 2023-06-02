import os
import sys
import concurrent.futures
from pathlib import Path
from progress.bar import IncrementalBar

from components.dep_count import get_package_dependencies, find_files, process_file
from components.create_excel import (
    create_excel_file,
    create_table,
)
from components.update_json import update_package_json
from components.utils import prompt_yes_no, open_file


def main():
    project_path = Path(input("Enter the path to the project: ").strip())
    repo_name = os.path.basename(project_path)

    if not project_path.exists() or not project_path.is_dir():
        sys.exit(f"{project_path} is not a valid directory")

    dependencies = get_package_dependencies(project_path)

    dependency_counts = {}
    for dependency in dependencies:
        dependency_counts[dependency] = 0

    entries = find_files(project_path)
    total_progress = len(entries)

    pb = IncrementalBar("Processing", max=total_progress)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for entry in entries:
            future = executor.submit(process_file, entry, dependency_counts)
            futures.append(future)
            pb.next()

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

    pb.finish()

    # Create table
    table = create_table(dependency_counts)
    print(table)

    # Create excel file
    output_path = f"output/{repo_name}_dep_counts.xlsx"
    create_excel_file(output_path, table)

    # Update package.json
    update_json = prompt_yes_no(
        "Do you want to remove unused packages from the package.json?"
    )

    if update_json:
        update_package_json(project_path, dependency_counts)

    # Open Excel file
    try:
        open_excel = prompt_yes_no("Do you want to open the Excel file?")
        if open_excel:
            open_file(output_path)
    except:
        pass

    print("------------------------------------")
    print("Done!")


if __name__ == "__main__":
    main()
