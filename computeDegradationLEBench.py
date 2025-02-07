import pandas as pd

    
#Computes degradation (percentage)for each test case based on baseline and current averages.
def calculate_degradation(baseline_file, current_file, output_directory):

    # Load baseline and current Excel files and extract only "Test Name" and "Average"
    baseline_df = pd.read_excel(baseline_file, usecols=["Test Name", "Average"])
    current_df = pd.read_excel(current_file, usecols=["Test Name", "Average"])

    # Merge both datasets
    merged_df = pd.merge(baseline_df, current_df, on="Test Name", suffixes=("_baseline", "_current"))

    # Compute degradation percentage: (baseline - current) / baseline * 100
    merged_df["Degradation (%)"] = ((merged_df["Average_baseline"] - merged_df["Average_current"]) / merged_df["Average_baseline"]) * 100

    # Define output file path
    output_file = f"{output_directory}/degradation_results.xlsx"

    # Save results to an Excel file
    merged_df.to_excel(output_file, index=False, engine="openpyxl")

    print(f"Degradation results saved to {output_file}")

if __name__ == "__main__":
    # Define paths for baseline and current (to be compared to) configurations
    baseline_path = "/path/to/ouput/folder/CleanedCSV/output_baseline.xlsx"
    current_path = "/path/to/ouput/folder/CleanedCSV/output_current.xlsx"
    
    # Set the output directory to where the degradation results should be saved
    output_directory = "/Users/samal/Desktop/BachelorThesis/Python/6.1.0.26"

    # Run the degradation calculation
    calculate_degradation(baseline_path, current_path, output_directory)
