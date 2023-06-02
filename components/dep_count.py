import json
import os


def get_package_dependencies(project_path: str):
    package_json_path = project_path / "package.json"
    with open(package_json_path) as file:
        package_json_data = json.load(file)
        return package_json_data.get("dependencies", {})


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
