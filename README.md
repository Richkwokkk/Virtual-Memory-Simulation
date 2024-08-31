Here's how you would run the simulator from the command line:

python memsim.py trace1 4 rand quiet

The simulator accepts four arguments:
- Memory trace file: The trace file to use (e.g., trace1).
- Number of page frames: The number of available page frames in the simulated memory.
- Page replacement algorithm: The replacement algorithm to use: rand, lru, or clock.
- Mode: The mode to run the simulator: quiet or debug.
