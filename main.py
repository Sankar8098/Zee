import requests
import random
import string
import time

def generate_random_string(length):
    """Generates a random alphanumeric string of given length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_and_verify_code():
    """Generates a Zee5 coupon code and verifies it via API."""
    code_prefix = "Z5APCP25Y"  # Adjust the prefix if needed
    random_suffix = generate_random_string(4)
    code = f"{code_prefix}{random_suffix}"

    url = f"https://securepayment.zee5.com/paymentGateway/coupon/verification?coupon_code={code}&translation=en&country_code=IN"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Mobile Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.zee5.com/"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        msg = result.get("message", "No message provided")
        if msg == "Coupon code applied successfully":
            with open("zee5code.txt", "a") as file:
                file.write(f"Valid Code: {code}\n")
            print(f"[✔] Code: {code} - {msg}")
        else:
            print(f"[✘] Code: {code} - {msg}")
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Error with code {code}: {e}")

def main():
    """Main function to generate multiple codes."""
    try:
        num_codes = int(input("Enter the number of codes to generate: "))
        for _ in range(num_codes):
            generate_and_verify_code()
            time.sleep(1)  # Prevents rapid requests
    except ValueError:
        print("[!] Please enter a valid number.")

if __name__ == "__main__":
    main()

