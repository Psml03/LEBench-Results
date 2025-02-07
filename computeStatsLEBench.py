import os
import pandas as pd
import numpy as np

#Cleans CSVs by removing 'kbest' lines and rounding numbers to 10 decimals
def clean_csv_files(input_directory, output_directory):
    
    # Make sure the output folder exists
    if not os.path.exists(output_directory):  
        os.makedirs(output_directory)  

    for filename in os.listdir(input_directory):  
        if filename.endswith(".csv"):  # Process only .csv files
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename)

            with open(input_filepath, 'r') as file:
                rows = file.readlines()  # Read each line of the file

            cleaned_rows = []
            for row in rows:
                if 'kbest' not in row:  # Skip rows for 'kbest'
                    parts = row.split(':')  
                    if len(parts) > 1:  
                        try:
                            value = float(parts[1].strip().strip(','))  # Convert to float
                            rounded_value = f"{value:.10f}"  # Round to 10 decimals
                            cleaned_rows.append(f"{parts[0]}: {rounded_value},\n")  
                        except ValueError:  
                            cleaned_rows.append(row)  
                    else:
                        cleaned_rows.append(row)  

            with open(output_filepath, 'w') as file:
                file.writelines(cleaned_rows)  # Save the cleaned file

            print(f"Cleaned {filename} and saved to {output_directory}")

    
#Reads cleaned CSVs, extracts 'average' values, calculates stats, and saves to Excel
def create_xlsx_from_csv(directory, output_file):
    
    data = {}  

    for filename in os.listdir(directory):  
        if filename.endswith(".csv"):  
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r') as file:
                for line in file:
                    if 'average:' in line:  # Find lines with 'average'
                        test_name, value = line.split(':')
                        test_name = test_name.strip()
                        value = value.strip().strip(',')

                        try:
                            value = float(value)  # Convert to float
                        except ValueError:
                            print(f"Skipping invalid value: {value} in file {filename}")
                            continue

                        if test_name not in data:
                            data[test_name] = []
                        data[test_name].append(value)

    test_names = sorted(data.keys())  # oder test names
    excel_data = {"Test Name": test_names}

    # Add iteration columns dynamically
    max_iterations = max(len(values) for values in data.values())
    for i in range(max_iterations):
        column_name = f"Iteration {i + 1}"
        excel_data[column_name] = [
            f"{data[test_name][i]:.10f}" if i < len(data[test_name]) else None 
            for test_name in test_names
        ]

    # Compute mean, median, and standard deviation
    excel_data["Average"] = [f"{np.mean(data[test_name]):.10f}" for test_name in test_names]
    excel_data["Median"] = [f"{np.median(data[test_name]):.10f}" for test_name in test_names]
    excel_data["Standard Deviation"] = [f"{np.std(data[test_name]):.10f}" for test_name in test_names]
    
    # Save to an Excel file
    df = pd.DataFrame(excel_data)
    df.to_excel(output_file, index=False)  

    print(f"Excel file created: {output_file}")

if __name__ == "__main__":
    
    # Folders for input and output
    input_directory = "/path/to/csv/files"
    cleaned_directory = "/path/to/output/folder/CleanedCSV"
    output_xlsx_path = "/path/to/output/folder/CleanedCSV/output.xlsx"
    
     # Step 1: Clean CSV files
    clean_csv_files(input_directory, cleaned_directory) 
    # Step 2: Generate Excel
    create_xlsx_from_csv(cleaned_directory, output_xlsx_path) 

    print("Processing completed.")
