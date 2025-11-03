# RAM Compare

A command-line tool to compare RAM usage of system processes between two snapshots. Useful for monitoring memory consumption changes over time.

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