# Dependencies Count

This is a command line tool that counts the number of times each of the dependencies specified in the package.json file of a project are imported in the project's JavaScript or TypeScript code. It visualizes the output in excel with a table and a bar chart, which allows you to identify which dependencies are not being used in your code and can potentially be removed. An option to remove the unused dependencies from the package.json is provided as a part of the script.

## Prerequisites

Before using this tool, you will need to have Python3 installed on your machine.

## Installation

To use this tool, clone this repository and build a virtual environment for the project.

```
python -m venv venv
source venv/bin/activate
```

Then, install the required dependencies.

```
pip install -r requirements.txt
```

## Usage

To use the tool, navigate to the `main.py` and run the script.

You will be prompted to provide the root project path, and an option to update the package.json automatically.

The tool will search the project directory and its subdirectories for JavaScript and TypeScript files, and count the number of times each dependency is imported. The results will be printed in a table in the console showing the dependency name and the number of times it was imported. It also creates an excel file with a table and a bar chart as a better visualization.
