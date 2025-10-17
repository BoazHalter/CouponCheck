import requests

# Load coupon codes from coupons.txt
with open("cupons.txt", "r") as f:
    coupons = [line.strip() for line in f if line.strip()]

# Prepare output file
with open("results.txt", "w") as out:
    for code in coupons:
        url = f"https://bulenox.com/member/ajax?do=check_coupon&coupon={code}"
        try:
            response = requests.get(url)
            result = response.text.strip()
            print(f"{code}: {result}")
            out.write(f"{code}: {result}\n")
        except Exception as e:
            print(f"{code}: ❌ Error - {e}")
            out.write(f"{code}: ❌ Error - {e}\n")
