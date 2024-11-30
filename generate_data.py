import random
import json
from datetime import datetime

# Множина для унікальних ідентифікаторів пристроїв
generated_ids = set()

# Генератор даних IoT
def generate_iot_data():
    protocols = ["TCP", "UDP", "HTTP", "MQTT"]
    encryption_methods = ["TLS", "SSL", "None"]
    status = ["Success", "Failure"]
    anomalies = ["None", "High Activity", "Packet Loss", "DoS Attempt"]

    # Унікальний ID пристрою
    while True:
        device_id = f"Device_{random.randint(1000, 9999)}"
        if device_id not in generated_ids:
            generated_ids.add(device_id)
            break

    data = {
        "timestamp": datetime.now().isoformat(),
        "device_id": device_id,
        "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "mac_address": f"{':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))}",
        "protocol": random.choice(protocols),
        "port": random.randint(1024, 49151),
        "encryption": random.choice(encryption_methods),
        "auth_status": random.choice(status),
        "login_attempts": random.randint(1, 10),
        "data_rate_kbps": random.randint(100, 10000),
        "anomaly": random.choice(anomalies),
        "temperature_celsius": round(random.uniform(20.0, 50.0), 2),  # Температура в °C
        "humidity_percent": round(random.uniform(30.0, 90.0), 2),  # Вологість в %
        }
    return data

# Генерація звіту
def generate_report(num_entries=300):
    report = {"iot_report": [generate_iot_data() for _ in range(num_entries)]}
    with open("iot_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print(f"Report generated: {len(report['iot_report'])} entries with unique device IDs")

# Виконання
if __name__ == "__main__":
    generate_report()
