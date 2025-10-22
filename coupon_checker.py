import requests
from datetime import datetime

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://bulenox.com/member/signup",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

with open("coupons.txt", "r") as f:
    coupons = [line.strip() for line in f if line.strip()]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("results.txt", "w") as out:
    out.write(f"Checked at: {timestamp}\n\n")

    for code in coupons:
        url = f"https://bulenox.com/member/ajax?do=check_coupon&coupon={code}"
        try:
            response = session.get(url, headers=headers)
            result = response.text.strip()

            # Normalize for comparison
            result_lower = result.lower()

            if result_lower == "true":
                status = "✅ Valid"
            elif "expired" in result_lower:
                status = "⏳ Expired"
            elif "no coupons found" in result_lower:
                status = "❌ Invalid"
            elif "<!doctype html>" in result_lower or "error" in result_lower:
                status = "❌ Error page returned"
            else:
                status = f"❓ Unrecognized response: {result}"

            out.write(f"{code}: {status}\n")
            print(f"{code}: {status}")

        except Exception as e:
            error = f"❌ Request failed - {e}"
            out.write(f"{code}: {error}\n")
            print(f"{code}: {error}")
