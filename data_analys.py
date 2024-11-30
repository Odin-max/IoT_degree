import json
from matplotlib import pyplot as plt
from collections import Counter

# Завантаження даних із JSON-файлу
def load_report(file_name="iot_report.json"):
    with open(file_name, "r") as f:
        return json.load(f)

# Аналіз даних
def analyze_data(data):
    auth_statuses = Counter(item["auth_status"] for item in data)
    anomalies = Counter(item["anomaly"] for item in data)
    protocols = Counter(item["protocol"] for item in data)
    encryptions = Counter(item["encryption"] for item in data)
    data_rates = [item["data_rate_kbps"] for item in data]
    
    return {
        "auth_statuses": auth_statuses,
        "anomalies": anomalies,
        "protocols": protocols,
        "encryptions": encryptions,
        "data_rates": data_rates,
    }

# Побудова графіків
def plot_analysis(analysis):
    # Авторизація
    plt.figure()
    plt.bar(analysis["auth_statuses"].keys(), analysis["auth_statuses"].values(), color="skyblue")
    plt.title("Auth Status Distribution")
    plt.xlabel("Auth Status")
    plt.ylabel("Count")
    plt.savefig("auth_status_distribution.png")
    plt.show()

    # Аномалії
    plt.figure()
    plt.pie(analysis["anomalies"].values(), labels=analysis["anomalies"].keys(), autopct="%1.1f%%")
    plt.title("Anomalies Distribution")
    plt.savefig("anomalies_distribution.png")
    plt.show()

    # Протоколи
    plt.figure()
    plt.bar(analysis["protocols"].keys(), analysis["protocols"].values(), color="orange")
    plt.title("Protocol Usage")
    plt.xlabel("Protocol")
    plt.ylabel("Count")
    plt.savefig("protocol_usage.png")
    plt.show()

    # Шифрування
    plt.figure()
    plt.pie(analysis["encryptions"].values(), labels=analysis["encryptions"].keys(), autopct="%1.1f%%")
    plt.title("Encryption Methods")
    plt.savefig("encryption_methods.png")
    plt.show()

    # Швидкість передачі даних
    plt.figure()
    plt.hist(analysis["data_rates"], bins=10, color="green", alpha=0.7)
    plt.title("Data Rate Distribution")
    plt.xlabel("Data Rate (kbps)")
    plt.ylabel("Frequency")
    plt.savefig("data_rate_distribution.png")
    plt.show()

# Виконання аналізу
if __name__ == "__main__":
    report = load_report()
    analysis = analyze_data(report["iot_report"])
    plot_analysis(analysis)
