#!/usr/bin/env python3

import os
import argparse
from typing import Dict
import psutil

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def get_process_ram() -> Dict[str, float]:
    ram_dict: Dict[str, float] = {}
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            name = proc.info['name']
            ram_mb = proc.info['memory_info'].rss / 1024 / 1024
            if name in ram_dict:
                ram_dict[name] += ram_mb
            else:
                ram_dict[name] = ram_mb
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return ram_dict

def save_data(filename: str, data: Dict[str, float]) -> None:
    with open(filename, 'w') as f:
        for name, ram in data.items():
            f.write(f"{ram:.2f} {name}\n")

def load_data(filename: str) -> Dict[str, float]:
    data: Dict[str, float] = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                ram = float(parts[0])
                name = ' '.join(parts[1:])
                data[name] = ram
    return data

def main():
    parser = argparse.ArgumentParser(description="Compare RAM usage of processes between two snapshots.")
    parser.add_argument('--base', default='base.txt', help='Base snapshot file (default: base.txt)')
    parser.add_argument('--next', default='next.txt', help='Next snapshot file (default: next.txt)')
    parser.add_argument('--threshold', type=float, default=1.0, help='Minimum RAM in MB to display processes (default: 1.0)')
    parser.add_argument('--reset', action='store_true', help='Regenerate base snapshot')
    args = parser.parse_args()

    if args.reset or not os.path.exists(args.base):
        print(f"Generating {args.base}...")
        data = get_process_ram()
        save_data(args.base, data)
        print(f"{args.base} created.")
    else:
        print(f"Generating {args.next}...")
        data = get_process_ram()
        save_data(args.next, data)
        print(f"{args.next} created.")
        print("")
        print("Report:")
        print("========")
        try:
            base = load_data(args.base)
            next_data = load_data(args.next)
        except FileNotFoundError as e:
            print(f"Error: {e}. Make sure snapshots exist.")
            exit(1)
        # Collect all processes
        all_procs = set(base.keys()) | set(next_data.keys())
        rows = []
        for name in all_procs:
            old = base.get(name, 0)
            new = next_data.get(name, 0)
            if new < args.threshold:
                continue
            change = new - old
            if old > 0:
                pct = (change / old) * 100
            else:
                pct = float('nan')  # N/A for new processes
            rows.append((name, old, new, change, pct))
        # Sort by new RAM descending
        rows.sort(key=lambda x: x[2], reverse=True)
        # Print table
        print(f"{'Process':<30} {'Old RAM (MB)':>12} {'New RAM (MB)':>12} {'Change (MB)':>12} {'% Change':>10}")
        print("-" * 80)
        for name, old, new, change, pct in rows:
            if change > 0:
                color = RED
            elif change < 0:
                color = GREEN
            else:
                color = BLUE
            pct_str = f"{pct:+.2f}%" if not (pct != pct) else "N/A"  # nan check
            print(f"{name:<30} {old:>12.2f} {new:>12.2f} {color}{change:>+12.2f}{RESET} {pct_str:>10}")

if __name__ == "__main__":
    main()