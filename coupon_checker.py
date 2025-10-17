import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://bulenox.com/member/signup"
}

with open("cupons.txt", "r") as f:
    coupons = [line.strip() for line in f if line.strip()]

with open("results.txt", "w") as out:
    for code in coupons:
        url = f"https://bulenox.com/member/ajax?do=check_coupon&coupon={code}"
        try:
            response = requests.get(url, headers=headers)
            result = response.text.strip()

            # Check for known error message
            if "An Error has occurred" in result:
                result = "❌ Error page returned"

            print(f"{code}: {result}")
            out.write(f"{code}: {result}\n")
        except Exception as e:
            print(f"{code}: ❌ Request failed - {e}")
            out.write(f"{code}: ❌ Request failed - {e}\n")
