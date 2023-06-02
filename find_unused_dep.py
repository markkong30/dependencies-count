import json
import os
import sys
import concurrent.futures
from pathlib import Path
from progress.bar import IncrementalBar
import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
import openpyxl


def get_package_dependencies(project_path: str):
    package_json_path = project_path / "package.json"
    with open(package_json_path) as file:
        package_json_data = json.load(file)
        return package_json_data["dependencies"]


def find_files(project_path: str):
    file_suffixes = [".js", ".jsx", ".ts", ".tsx"]
    remove_suffixes = [".d.ts"]
    exclude_dirs = ["node_modules", "dist", ".next"]

    files = []

    for root, _, filenames in os.walk(project_path):
        if any(dir_name in root for dir_name in exclude_dirs):
            continue

        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in file_suffixes and ext not in remove_suffixes:
                files.append(os.path.join(root, filename))

    return files


def process_file(entry: str, dependency_counts: dict):
    with open(entry) as file:
        contents = file.read()

    for dependency in dependency_counts:
        if dependency in contents:
            dependency_counts[dependency] += 1


def create_excel_file(file_path: str, table: pd.DataFrame):
    # Save table to excel file
    table.to_excel(file_path)

    # Create horizontal bar chart
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    create_horizontal_bar_chart(sheet, table)

    # Adjust column widths
    sheet.column_dimensions["A"].width = 30  # Set width for dependencies column
    sheet.column_dimensions["B"].width = 10  # Set width for count column

    workbook.save(file_path)


def create_table(dependency_counts):
    df = pd.DataFrame.from_dict(dependency_counts, orient="index", columns=["Count"])
    df.index.name = "Dependency"
    df_sorted = df.sort_values("Count", ascending=False)
    return df_sorted


def create_horizontal_bar_chart(sheet, table):
    chart = BarChart(barDir="bar", grouping="standard")
    chart.title = "Dependency Counts"
    chart.x_axis_title = "Count"
    chart.y_axis_title = "Dependency"

    data = Reference(sheet, min_col=2, min_row=1, max_row=len(table) + 1, max_col=2)
    categories = Reference(sheet, min_col=1, min_row=2, max_row=len(table) + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    chart.legend = None

    # Display count on the bar
    data_labels = DataLabelList()
    data_labels.showVal = True
    chart.dataLabels = data_labels

    # Set chart size
    num_items = len(table)
    chart.width = 45
    chart.height = num_items * 0.7

    # Add chart to the worksheet
    sheet.add_chart(chart, "D2")


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

    table = create_table(dependency_counts)
    print(table)

    # Create excel file
    output_path = f"output/{repo_name}_dep_counts.xlsx"
    create_excel_file(output_path, table)

    print("------------------------------------")
    print("Done!")


if __name__ == "__main__":
    main()
