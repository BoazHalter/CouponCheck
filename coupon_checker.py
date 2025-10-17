import requests

# Replace with actual endpoint if known
url = "https://bulenox.com/member/signup"

# Load coupons
with open("cupons.txt", "r") as f:
    coupons = [line.strip() for line in f if line.strip()]

# Simulate form data (adjust as needed)
form_data = {
    "account_type": "25000",  # Example account
    "email": "test@example.com",
    "password": "Test1234",
    "coupon": "",  # Will be filled in loop
}

# Test each coupon
for code in coupons:
    form_data["coupon"] = code
    print(f"Testing coupon: {code}...")
    response = requests.post(url, data=form_data)
    
    # Print a snippet of the response to understand what's happening
    snippet = response.text[:300]  # Show first 300 characters
    print(f"Response snippet:\n{snippet}\n")

    if "invalid" in response.text.lower():
        print(f"{code}: ❌ Invalid\n")
    elif "applied" in response.text.lower() or "discount" in response.text.lower():
        print(f"{code}: ✅ Valid\n")
    else:
        print(f"{code}: 🤔 Unknown response\n")
