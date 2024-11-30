import random
import json
from datetime import datetime

# Множини для унікальних ідентифікаторів пристроїв та портів
generated_ids = set()
generated_ports = set()

# Генератор даних IoT
def generate_iot_data():
    protocols = ["TCP", "UDP", "HTTP", "MQTT"]
    encryption_methods = ["TLS", "SSL", "None"]
    anomalies = ["None", "High Activity", "Packet Loss", "DoS Attempt"]

    # Унікальний ID пристрою
    while True:
        device_id = f"Device_{random.randint(1000, 9999)}"
        if device_id not in generated_ids:
            generated_ids.add(device_id)
            break

    # Унікальний порт
    while True:
        port = random.randint(1024, 49151)
        if port not in generated_ports:
            generated_ports.add(port)
            break

    # Генерація статусу з можливістю додавання "Failure" в майбутньому
    auth_status = "Success"

    # Генерація login_attempts з 90% шансом отримати 1, інші випадки — від 2 до 10
    login_attempts = 1 if random.random() < 0.9 else random.randint(2, 10)

    # Генерація аномалії з 90% шансом отримати "None", інші випадки — випадкові аномалії
    anomaly = "None" if random.random() < 0.9 else random.choice(anomalies)

    # Поле останнього оновлення
    last_updated = datetime.now().isoformat()

    data = {
        "timestamp": datetime.now().isoformat(),
        "last_updated": last_updated,
        "device_id": device_id,
        "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "mac_address": f"{':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))}",
        "protocol": random.choice(protocols),
        "port": port,
        "encryption": random.choice(encryption_methods),
        "auth_status": auth_status,
        "login_attempts": login_attempts,
        "data_rate_kbps": random.randint(100, 10000),
        "anomaly": anomaly,
        "temperature_celsius": round(random.uniform(20.0, 50.0), 2),  # Температура в °C
        "humidity_percent": round(random.uniform(30.0, 90.0), 2),  # Вологість в %
        
    }
    return data

# Генерація звіту
def generate_report(num_entries=300):
    report = {"iot_report": [generate_iot_data() for _ in range(num_entries)]}
    with open("iot_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print(f"Report generated: {len(report['iot_report'])} entries with unique device IDs and ports.")

# Виконання
if __name__ == "__main__":
    generate_report()
