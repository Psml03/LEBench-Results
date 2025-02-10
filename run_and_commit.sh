#!/bin/bash

# Define benchmark directories and output file path 
LEBENCH_DIR=""

# Run the loop 12 times
for i in {1..12}; do
    echo "Starting iteration $i..."

    # Navigate to LEBench
    cd "$LEBENCH_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to navigate to $LEBENCH_DIR. Exiting."
        exit 1
    fi

    # Run the required scripts
    sudo taskset -c  0-11,24-35 python3 get_kern.py
    if [ $? -ne 0 ]; then
        echo "Error running get_kern.py. Exiting."
        exit 1
    fi

    sudo taskset -c  0-11,24-35 python3 run.py
    if [ $? -ne 0 ]; then
        echo "Error running run.py. Exiting."
        exit 1
    fi

    # Commit and push changes in LEBench
    git add .
    git commit -m "Run $i"
    git push 


    echo "Completed iteration $i."

    # Wait for 1 minute before proceeding to the next iteration
    if [ $i -lt 12 ]; then
        echo "Waiting for 1 minute before the next iteration..."
        sleep 60
    fi
done

echo "All iterations completed."

