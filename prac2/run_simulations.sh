#!/bin/bash

# List of trace files
trace_files=("gcc.trace" "bzip.trace" "sixpack.trace" "swim.trace")

# List of algorithms
algorithms=("rand" "lru" "clock")

# Output CSV file
output_file="simulation_results.csv"

# Write CSV header
echo "Algorithm,Trace File,Page Frames,Total Disk Reads,Total Disk Writes,Page Fault Rate" > $output_file

# Range of page frames (from 1 to 15)
for frames in {1..300}; do
  for trace in "${trace_files[@]}"; do
    for algo in "${algorithms[@]}"; do
      # Construct the command
      cmd="python memsim.py $trace $frames $algo quiet"
      
      # Capture the output of the simulation
      output=$($cmd)
      
      # Extract relevant data from the output
      total_disk_reads=$(echo "$output" | grep "total disk reads" | awk '{print $4}')
      total_disk_writes=$(echo "$output" | grep "total disk writes" | awk '{print $4}')
      page_fault_rate=$(echo "$output" | grep "page fault rate" | awk '{print $4}')
      
      # Write results to CSV file
      echo "$algo,$trace,$frames,$total_disk_reads,$total_disk_writes,$page_fault_rate" >> $output_file
      
      echo "Finished simulation: Algorithm = $algo, Trace = $trace, Frames = $frames"
      echo "------------------------------------------------------------"
    done
  done
done
