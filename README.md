This repository contains benchmarking results generated for my bachelor's thesis. The results were obtained using the LEBench benchmark tool available on GitHub, and the output files are stored as CSV files. Each branch corresponds to a different kernel configuration. Browse the branches to view the result files for each configuration.
Any modifications to the benchmarking tool's code can be viewed in my forked version of the original repository (also available on my GitHub account).

Scripts:
- The computeStatsLEBench script processes benchmark data from CSV files by cleaning them, and only extracts the "average" values and saves the cleaned CSV files to a folder. It also computes mean, median, and standard deviation and saves the results an Excel file.
- The computeDegradationLEBench script takes two such Excel files as inputs and calculates performance degradation as a percentage. It compares the "average" values from both files, determining how much performance has changed, and saves the results in an Excel file. The two input Excel files should be created using computeStatsLEBench. 

- The run_and_commit script automates running the LEBench benchmark multiple times and collecting the results in a GitHub repository. Manual adjustments are required for file paths, directory locations, and repository branches.
