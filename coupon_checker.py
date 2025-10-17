import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://bulenox.com/member/signup"
}

with open("coupons.txt", "r") as f:
    coupons = [line.strip() for line in f if line.strip()]

with open("results.txt", "w") as out:
    for code in coupons:
        url = f"https://bulenox.com/member/ajax?do=check_coupon&coupon={code}"
        try:
            response = requests.get(url, headers=headers)
            result = response.text.strip().lower()

            if result == "true":
                status = "✅ Valid"
            elif result == "false":
                status = "❌ Invalid"
            elif "expired" in result:
                status = "⏳ Expired"
            elif "error" in result or "<!DOCTYPE html>" in result:
                status = "❌ Error page returned"
            else:
                status = f"❓ Unknown response: {result}"

            print(f"{code}: {status}")
            out.write(f"{code}: {status}\n")

        except Exception as e:
            print(f"{code}: ❌ Request failed - {e}")
            out.write(f"{code}: ❌ Request failed - {e}\n")
