# RAM Compare

A command-line tool to compare RAM usage of system processes between two snapshots. Useful for monitoring memory consumption changes over time.

```bash
./ram-compare.py                
Generating next.txt...
next.txt created.

Report:
========
Process                        Old RAM (MB) New RAM (MB)  Change (MB)   % Change
--------------------------------------------------------------------------------
brave                                  0.00      3309.08     +3309.08        N/A
opencode                             209.50       498.52      +289.02   +137.96%
gnome-shell                          327.23       253.78       -73.45    -22.45%
kgx                                  113.96       147.09       +33.13    +29.07%
nautilus                             208.57       135.80       -72.77    -34.89%
syncthing                             72.06        53.19       -18.87    -26.19%
python                                52.40        51.79        -0.61     -1.16%
Xwayland                              84.76        47.07       -37.69    -44.47%
localsearch-extractor-3               46.55        44.38        -2.17     -4.66%
containerd                            45.36        41.93        -3.43     -7.56%

```

## Installation

### Prerequisites
- Python 3.9 or higher
- `psutil` library

### Install with uv (recommended)
```bash
uv pip install .
```

### Or with pip
```bash
pip install .
```

## Usage

Run the tool to capture snapshots and compare RAM usage.

### First Run (Create Base Snapshot)
```bash
python ram-compare.py
```
This creates `base.txt` with current RAM usage.

### Subsequent Runs (Compare with Base)
```bash
python ram-compare.py
```
This creates `next.txt` and displays a comparison report.

### Command-Line Options
- `--base FILE`: Specify base snapshot file (default: `base.txt`)
- `--next FILE`: Specify next snapshot file (default: `next.txt`)
- `--threshold MB`: Minimum RAM in MB to display processes (default: 1.0)
- `--reset`: Regenerate base snapshot

### Examples
```bash
# Use custom file names
python ram-compare.py --base before.txt --next after.txt

# Only show processes using more than 10 MB
python ram-compare.py --threshold 10.0

# Reset base snapshot
python ram-compare.py --reset
```

## Output
The tool displays a table with:
- Process name
- Old RAM usage (MB)
- New RAM usage (MB)
- Change in RAM (MB) - colored red for increase, green for decrease
- Percentage change

Processes with RAM usage below the threshold are filtered out.

## License
MIT License