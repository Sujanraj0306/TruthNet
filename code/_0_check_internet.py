import requests


def is_internet_on():
    try:
        response = requests.get("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False


if __name__ == "__main__":
    if is_internet_on():
        print("Internet is ON")
    else:
        print("Internet is OFF")
