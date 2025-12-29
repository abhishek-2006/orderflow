import json
FILE = "orders.json"

def save_data(queue, served):
    data = {
        "queue": list(queue),
        "served": served
    }
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            return data["queue"], data["served"]
    except:
        return [], []

def export_report(queue, served):
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("📋 Restaurant Report\n\n")
        f.write("Pending Orders:\n")
        for q in queue:
            f.write(q + "\n")

        f.write("\nServed Orders:\n")
        for s in served[::-1]:
            f.write(s + "\n")
