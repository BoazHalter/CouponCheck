import os
import re
from collections import defaultdict

# --- Configuration ---
PREVIOUS_FILE = "./previous_run/result.txt"
CURRENT_FILE = "./current_run_data/result.txt"
REPORT_FILE = "change_report.txt"

# Regex to parse the line: CouponCode: [StatusEmoji] StatusMessage
# We treat '❌' as INVALID and any other leading emoji (or lack thereof) as VALID for simplicity
LINE_PATTERN = re.compile(r'(\w+):\s*(?:(❌)|(.+?))\s*(.+)')

def parse_results(file_path):
    """Parses the result.txt file into a dictionary: {code: status}"""
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = LINE_PATTERN.match(line)
                if match:
                    code, invalid_emoji, valid_emoji, message = match.groups()
                    # If '❌' is present, the status is 'INVALID'. Otherwise, we assume 'VALID'.
                    status = 'INVALID' if invalid_emoji == '❌' else 'VALID'
                    results[code] = status
    except FileNotFoundError:
        # This is expected for the first run or if the previous commit data is missing
        print(f"Warning: Previous results file not found at {file_path}. Proceeding without comparison.")
    return results

def analyze_changes(previous_data, current_data):
    """Compares previous and current data and generates the change report."""
    report = []
    
    # Identify all unique coupon codes across both runs
    all_codes = set(previous_data.keys()) | set(current_data.keys())

    for code in sorted(list(all_codes)):
        prev_status = previous_data.get(code)
        curr_status = current_data.get(code)

        if prev_status is None:
            # New Coupon
            report.append(f"[NEW]   {code} has appeared. Current Status: {curr_status}")
        elif curr_status is None:
            # Missing Coupon
            report.append(f"[MISSING] {code} was in previous run ({prev_status}) but is missing now.")
        elif prev_status != curr_status:
            # Status Change
            report.append(f"[CHANGE] {code} status changed: {prev_status} -> {curr_status}")
        # If status is the same, no action is needed (Status Quo)
        
    # Write the report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("--- COUPON STATUS CHANGE ANALYSIS REPORT ---\n\n")
        if not report:
            f.write("✅ No changes in coupon statuses or inventory detected between runs.")
        else:
            f.write(f"Total changes identified: {len(report)}\n\n")
            f.write("\n".join(report))
            
    print(f"Analysis complete. Report written to {REPORT_FILE}")
    
if __name__ == "__main__":
    # Ensure the directory for current data exists (from unzip step in YAML)
    os.makedirs(os.path.dirname(CURRENT_FILE), exist_ok=True)
    
    previous_results = parse_results(PREVIOUS_FILE)
    current_results = parse_results(CURRENT_FILE)
    
    analyze_changes(previous_results, current_results)
