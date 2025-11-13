import os
import re
from collections import defaultdict

# --- Configuration ---
# Path where the previous run's artifact will be downloaded and unzipped
PREVIOUS_FILE = "./previous_run_data/result.txt" 
# Path where the current run's artifact will be downloaded and unzipped
CURRENT_FILE = "./current_run_data/result.txt" 
REPORT_FILE = "change_report.txt"

# Regex to parse the line: CouponCode: [StatusEmoji] StatusMessage
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
        # Expected for the very first run of the checker (no previous artifact yet)
        print(f"Warning: Results file not found at {file_path}. Proceeding.")
    return results

def analyze_changes(previous_data, current_data):
    """Compares previous and current data and generates the change report."""
    report = []
    
    # Identify all unique coupon codes across both runs
    all_codes = set(previous_data.keys()) | set(current_data.keys())

    # Get baseline summary for report
    prev_valid_count = sum(1 for status in previous_data.values() if status == 'VALID')
    curr_valid_count = sum(1 for status in current_data.values() if status == 'VALID')
    
    for code in sorted(list(all_codes)):
        prev_status = previous_data.get(code)
        curr_status = current_data.get(code)

        if prev_status is None:
            # New Coupon
            report.append(f"[NEW]   {code} has appeared. Current Status: {curr_status}")
        elif curr_status is None:
            # Missing Coupon (Removed from list or check failed to find it)
            report.append(f"[MISSING] {code} was present ({prev_status}) but is missing now.")
        elif prev_status != curr_status:
            # Status Change
            report.append(f"[CHANGE] {code} status changed: {prev_status} -> {curr_status}")
        # If status is the same, no action is needed (Status Quo)
        
    # Write the report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("--- COUPON STATUS CHANGE ANALYSIS REPORT ---\n\n")
        f.write(f"Valid Coupons (Previous Run): {prev_valid_count}\n")
        f.write(f"Valid Coupons (Current Run):  {curr_valid_count}\n")
        f.write(f"Net Change in Valid:          {curr_valid_count - prev_valid_count}\n")
        f.write("-" * 40 + "\n\n")
        
        if not report:
            f.write("✅ No changes in coupon statuses or inventory detected between runs.")
        else:
            f.write(f"Total changes identified: {len(report)}\n\n")
            f.write("\n".join(report))
            
    print(f"Analysis complete. Report written to {REPORT_FILE}")
    
if __name__ == "__main__":
    # Ensure all necessary directories exist
    os.makedirs(os.path.dirname(CURRENT_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(PREVIOUS_FILE), exist_ok=True)
    
    previous_results = parse_results(PREVIOUS_FILE)
    current_results = parse_results(CURRENT_FILE)
    
    analyze_changes(previous_results, current_results)
