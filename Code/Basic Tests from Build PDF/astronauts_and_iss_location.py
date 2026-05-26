# -----------------------------
# Created with CoPilot Assistance 5/21/2026
# Pulls API json data from: http://open-notify.org/Open-Notify-API/
# -----------------------------
import network
import urequests
import time
import secrets

# -----------------------------
# Wi-Fi Connect Helper
# -----------------------------
def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)

        # Wait up to ~10 seconds
        for _ in range(20):
            if wlan.isconnected():
                break
            time.sleep(0.5)

    if wlan.isconnected():
        print("Connected:", wlan.ifconfig()[0])
    else:
        raise RuntimeError("Wi-Fi connection failed")

    return wlan

# -----------------------------
# Fetch and Print Astronauts
# -----------------------------
def show_astronauts():
    print("\n=== Current Astronauts in Space ===\n")

    try:
        r = urequests.get("http://api.open-notify.org/astros.json")
        data = r.json()
        r.close()
    except Exception as e:
        print("Error fetching data:", e)
        return

    people = data.get("people", [])
    number = data.get("number", 0)

    print("Total astronauts:", number)
    print("-" * 32)

    for p in people:
        name = p.get("name", "Unknown")
        craft = p.get("craft", "Unknown")
        print("{:<22} {}".format(name, craft))

    print("-" * 32)
    
# -----------------------------
# Fetch and Print ISS Location
# -----------------------------
def iss_location():
    print("\n=== Current ISS Location ===\n")

    while True:
        try:
            r = urequests.get("http://api.open-notify.org/iss-now.json")
            data = r.json()
            r.close()

            lat = data['iss_position']['latitude']
            lon = data['iss_position']['longitude']

            # Table header
            print("+----------------+----------------+")
            print("| Latitude       | Longitude      |")
            print("+----------------+----------------+")

            # Table row
            print("| {:<14} | {:<14} |".format(lat, lon))

            print("+----------------+----------------+\n")

        except Exception as e:
            print("Connection error:", e)
            print("Wi-Fi status:", wlan.status())

            if wlan.status() < 0 or wlan.status() >= 3:
                print("Reconnecting Wi-Fi...")
                wlan.disconnect()
                wlan.connect(secrets.SSID, secrets.PASSWORD)

                if wlan.status() == 3:
                    print("Reconnected")
                else:
                    print("Reconnect failed")

        time.sleep(1)

# -----------------------------
# MAIN PROGRAM
# -----------------------------
wlan = wifi_connect(secrets.SSID, secrets.PASSWORD)
show_astronauts()
iss_location()