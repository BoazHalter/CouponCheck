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
            result = response.text.strip().lower()

            if result == "true":
                status = "✅ Valid"
            elif result == "false":
                status = "❌ Invalid"
            elif "expired" in result:
                status = "⏳ Expired"
            elif "<!doctype html>" in result or "error" in result:
                status = "❌ Error page returned"
            else:
                status = f"❓ Unknown response: {result}"

            out.write(f"{code}: {status}\n")
            print(f"{code}: {status}")

        except Exception as e:
            error = f"❌ Request failed - {e}"
            out.write(f"{code}: {error}\n")
            print(f"{code}: {error}")
