#!/usr/bin/env python3
import zipfile, re, glob, os
from collections import defaultdict, Counter

# The workflow now puts the big zip in downloaded/bundle.zip and extracts to downloaded/
# So we look there for the extracted result.txt files
EXTRACTED_DIR = "downloaded"

print(f"Looking for result.txt files in ./{EXTRACTED_DIR}/")

txt_files = glob.glob(f"{EXTRACTED_DIR}/*result.txt")
if not txt_files:
    print("No result.txt files found! Did the download step work?")
    exit(1)

print(f"Found {len(txt_files)} result.txt files – starting analysis...")

valid_per_day = defaultdict(int)
invalid_per_day = defaultdict(int)
expired_per_day = defaultdict(int)
error_per_day = defaultdict(int)
all_coupons = Counter()
valid_codes = set()
total_checks = 0
date_pattern = re.compile(r"Checked at: (\d{4}-\d{2}-\d{2})")

for txt_file in txt_files:
    with open(txt_file, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    current_date = "unknown"
    for line in lines:
        line = line.strip()
        if line.startswith("Checked at:"):
            m = date_pattern.search(line)
            if m:
                current_date = m.group(1)
            continue
        if ":" not in line:
            continue

        coupon, status = line.split(":", 1)
        coupon = coupon.strip()
        status = status.strip()

        total_checks += 1
        all_coupons[coupon] += 1

        if "Valid" in status:
            valid_per_day[current_date] += 1
            valid_codes.add(coupon)
        elif "Invalid" in status:
            invalid_per_day[current_date] += 1
        elif "Expired" in status:
            expired_per_day[current_date] += 1
        elif "Error" in status:
            error_per_day[current_date] += 1

# Generate report
report = f"""# Coupon Results — Full Historical Analysis

**Total checks:** {total_checks:,}  
**Unique codes tested:** {len(all_coupons):,}  
**Codes that were valid at least once:** {len(valid_codes):,}

## Daily Success Rate
Date       | Valid | Invalid | Expired | Error | Success%
---------- | ----- | ------- | ------- | ----- | --------
"""
for date in sorted(valid_per_day.keys(), reverse=True):
    if date == "unknown":
        continue
    v = valid_per_day[date]
    i = invalid_per_day[date]
    e = expired_per_day[date]
    r = error_per_day[date]
    total = v + i + e + r or 1
    pct = v / total * 100
    report += f"{date} | {v:5} | {i:7} | {e:7} | {r:5} | {pct:6.1f}%\n"

report += f"\n## Top 15 Most Tested Codes\n"
for code, count in all_coupons.most_common(15):
    status = "Valid" if code in valid_codes else "Never valid"
    report += f"- `{code}` → {count} times → {status}\n"

report += f"\n## All Valid Codes Ever ({len(valid_codes)} total)\n\n```\n"
report += "  ".join(sorted(valid_codes))
report += "\n```\n"

os.makedirs("results", exist_ok=True)
with open("results/FULL_REPORT.md", "w") as f:
    f.write(report)
with open("results/VALID_CODES.txt", "w") as f:
    f.write("\n".join(sorted(valid_codes)))

print("Analysis complete – report ready!")
