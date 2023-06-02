# Dependencies Count

This is a command line tool that counts the number of times each of the dependencies specified in the package.json file of a project are imported in the project's JavaScript or TypeScript code. 

It visualizes the output in excel with a table and a bar chart, which allows you to identify which dependencies are not being used in your code and can potentially be removed or be moving to dev dependencies. 

An option to remove the unused dependencies from the package.json is provided as a part of the script.

<img width="1508" alt="Screenshot 2023-06-02 at 4 41 47 PM" src="https://github.com/markkong30/dependencies-count/assets/94219999/0b466a05-9c5c-4cba-8dba-f34acc463fa1">

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

You will be prompted to provide the root project path, and an option to update the package.json by removing unused dependencies automatically. Please be sure that you are not using them as dev dependencies before removing them.

The tool will search the project directory and its subdirectories for JavaScript and TypeScript files, and count the number of times each dependency is imported. The results will be printed in a table in the console showing the dependency name and the number of times it was imported. 

It also creates an excel file with a table and a bar chart as a better visualization.

## Credits

Thanks [@pauloportella](https://github.com/pauloportella) for the inspiration!
