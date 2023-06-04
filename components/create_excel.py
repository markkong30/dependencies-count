import os
import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
import openpyxl


def create_table(dependency_counts: dict):
    df = pd.DataFrame.from_dict(dependency_counts, orient="index", columns=["Count"])
    df.index.name = "Dependency"
    df_sorted = df.sort_values("Count", ascending=False)
    return df_sorted


def create_excel_file(file_path: str, table: pd.DataFrame):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Add table to Excel file
        table.to_excel(file_path)

        # Create horizontal bar chart
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        create_horizontal_bar_chart(sheet, table)

        # Enable sorting
        table_range = f"A1:B{len(table)+1}"
        data_range = f"B2:B{len(table)+1}"
        sheet.auto_filter.ref = table_range
        sheet.auto_filter.add_sort_condition(data_range)

        # Adjust column widths
        sheet.column_dimensions["A"].width = 30  # Set width for dependencies column
        sheet.column_dimensions["B"].width = 10  # Set width for count column

        # Save Excel file
        workbook.save(file_path)
        workbook.close()

        print("------------------------------------")
        print(f"Excel file saved successfully.")
        print("------------------------------------")

    except Exception as e:
        print(f"Error saving Excel file: {e}")


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
