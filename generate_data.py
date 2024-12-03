import random
import json
from datetime import datetime
from faker import Faker

# Ініціалізація Faker
fake = Faker()

# Множини для унікальних ідентифікаторів пристроїв
generated_ids = set()

# Генератор даних IoT для пристроїв у сфері охорони здоров'я
def generate_iot_data():
    device_types = [
        "Heart Rate Monitor",
        "Blood Pressure Monitor",
        "Glucose Meter",
        "Infusion Pump",
        "ECG Monitor",
        "Smart Bed",
        "Ventilator",
        "Wearable Fitness Tracker",
    ]
    manufacturers = [
        "MedTech Inc.",
        "HealthPro Systems",
        "CareTrack Solutions",
        "BioMonitor Co.",
        "LifeFit Devices",
    ]

    # Унікальний ID пристрою
    while True:
        device_id = f"Device_{random.randint(1000, 9999)}"
        if device_id not in generated_ids:
            generated_ids.add(device_id)
            break

    # Випадковий тип пристрою
    device_type = random.choice(device_types)

    # Генерація статусу підключення
    connection_status = "Connected" if random.random() < 0.9 else "Disconnected"

    # Поле останнього оновлення
    last_updated = datetime.now().isoformat()

    # Генерація специфічних даних для кожного типу пристрою, якщо статус підключення "Connected"
    critical_data = {}
    if connection_status == "Connected":
        if device_type == "Heart Rate Monitor":
            critical_data["heart_rate"] = random.randint(40, 180)  # bpm
        elif device_type == "Blood Pressure Monitor":
            critical_data["blood_pressure"] = f"{random.randint(90, 180)}/{random.randint(60, 120)}"  # mmHg
        elif device_type == "Glucose Meter":
            critical_data["glucose_level_mg_dL"] = random.randint(70, 200)  # mg/dL
        elif device_type == "Infusion Pump":
            critical_data["infusion_rate_mL_h"] = round(random.uniform(0.1, 500.0), 2)  # mL/h
        elif device_type == "ECG Monitor":
            critical_data["ecg_readings"] = [round(random.uniform(-1.0, 1.0), 2) for _ in range(10)]  # Simulated ECG readings
        elif device_type == "Smart Bed":
            critical_data["patient_weight_kg"] = random.randint(40, 200)  # kg
            critical_data["bed_angle_deg"] = round(random.uniform(0, 45), 1)  # degrees
        elif device_type == "Ventilator":
            critical_data["oxygen_saturation_percent"] = round(random.uniform(80.0, 100.0), 2)  # %
            critical_data["respiratory_rate_bpm"] = random.randint(10, 30)  # breaths per minute
        elif device_type == "Wearable Fitness Tracker":
            critical_data["steps_count"] = random.randint(0, 20000)  # steps
            critical_data["calories_burned_kcal"] = round(random.uniform(0.0, 5000.0), 2)  # kcal

    # Дані про пристрій
    data = {
        "timestamp": datetime.now().isoformat(),
        "last_updated": last_updated,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "device_id": device_id,
        "device_type": device_type,
        "manufacturer": random.choice(manufacturers),
        "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "mac_address": f"{':'.join(f'{random.randint(0, 255):02x}' for _ in range(6))}",
        "connection_status": connection_status,
        "critical_data": critical_data,
    }
    return data

# Генерація звіту
def generate_report(num_entries=50):
    report = {"iot_report": [generate_iot_data() for _ in range(num_entries)]}
    with open("iot_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print(f"Report generated: {len(report['iot_report'])} entries with unique device IDs.")

# Виконання
if __name__ == "__main__":
    generate_report()
