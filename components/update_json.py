import json


def update_package_json(project_path: str, dependency_counts: dict):
    package_json_path = project_path / "package.json"
    with open(package_json_path) as file:
        package_json_data = json.load(file)

    modified_package_json_data = package_json_data.copy()
    modified_dependencies = modified_package_json_data.get("dependencies", {})

    for dependency, count in dependency_counts.items():
        if count == 0 and dependency in modified_dependencies:
            del modified_dependencies[dependency]

    modified_package_json_data["dependencies"] = modified_dependencies

    with open(package_json_path, "w") as file:
        json.dump(modified_package_json_data, file, indent=2)
