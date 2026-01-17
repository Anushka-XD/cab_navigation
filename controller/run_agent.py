import subprocess
import os

def run_macro(name):
    print(f"[ACTION] Running macro: {name}")
    subprocess.run(
        ["droidrun", "macro", "run", name],
        check=True
    )

def read_fare(app):
    path = f"/tmp/{app}_fare.txt"
    if not os.path.exists(path):
        raise RuntimeError(f"Fare file missing for {app}")
    with open(path) as f:
        return int(f.read().strip())

def main():
    destination = input("Enter destination: ").strip()
    print(f"[INFO] Destination set to: {destination}")

    # Step 1: Get fares
    for app in ["uber", "ola", "rapido"]:
        run_macro(f"{app}_fare")

    fares = {
        "uber": read_fare("uber"),
        "ola": read_fare("ola"),
        "rapido": read_fare("rapido"),
    }

    print("[INFO] Fares collected:", fares)

    # Step 2: Choose cheapest
    cheapest_app = min(fares, key=fares.get)
    cheapest_price = fares[cheapest_app]

    print(f"[DECISION] Booking {cheapest_app} at ₹{cheapest_price}")

    # Step 3: Book
    run_macro(f"book_{cheapest_app}")

    print(
        f"✅ Cab booked via {cheapest_app.upper()} "
        f"for ₹{cheapest_price}"
    )

if __name__ == "__main__":
    main()
