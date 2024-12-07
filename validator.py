import re
import json


def validate_payload(payload):
    """
    Валідатор даних для перевірки перед збереженням у базу даних.

    Аргументи:
    - payload (dict): Дані, які потрібно перевірити.

    Повертає:
    - bool: True, якщо дані валідні, інакше викликає ValueError.
    """
    # Поля, які потрібно перевірити
    required_fields = [
        "timestamp",
        "last_updated",
        "device_id",
        "ip_address",
        "mac_address",
        "connection_status",
        "device_type",
        "manufacturer",
        "first_name",
        "last_name",
        "critical_data",
    ]

    # Перевірка наявності всіх обов'язкових полів
    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Відсутнє обов'язкове поле: {field}")

    # Перевірка на коректність IP-адреси
    ip_regex = (
        r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    )
    if not re.match(ip_regex, payload["ip_address"]):
        raise ValueError("Невалідна IP-адреса")

    # Перевірка на коректність MAC-адреси
    mac_regex = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    if not re.match(mac_regex, payload["mac_address"]):
        raise ValueError("Невалідна MAC-адреса")

    # Перевірка на коректний формат connection_status
    if payload["connection_status"] not in ["Connected", "Disconnected"]:
        raise ValueError("Невалідний статус підключення")

    # Якщо статус Connected, critical_data не повинно бути порожнім
    if payload["connection_status"] == "Connected" and not payload["critical_data"]:
        raise ValueError("Поле critical_data не може бути порожнім для пристрою зі статусом 'Connected'")

    # Перевірка на допустимі символи в текстових полях
    text_fields = ["device_id", "device_type", "manufacturer", "first_name", "last_name"]
    for field in text_fields:
        if not re.match(r"^[a-zA-Z0-9\s\-_,.]*$", payload[field]):
            raise ValueError(f"Невалідні символи в полі {field}")

    # Перевірка на JSON-формат критичних даних
    if not isinstance(payload["critical_data"], dict):
        raise ValueError("Поле critical_data має бути словником")

    # Валідація critical_data залежно від типу пристрою
    device_type_critical_data = {
        "Heart Rate Monitor": {"heart_rate": int},
        "Blood Pressure Monitor": {"blood_pressure": str},
        "Glucose Meter": {"glucose_level_mg_dL": int},
        "Infusion Pump": {"infusion_rate_mL_h": (int, float)},
        "ECG Monitor": {"ecg_readings": list},
        "Smart Bed": {"patient_weight_kg": int, "bed_angle_deg": (int, float)},
        "Ventilator": {
            "oxygen_saturation_percent": (int, float),
            "respiratory_rate_bpm": int,
        },
        "Wearable Fitness Tracker": {"steps_count": int, "calories_burned_kcal": (int, float)},
    }

    device_type = payload["device_type"]
    if device_type in device_type_critical_data:
        required_critical_fields = device_type_critical_data[device_type]
        for key, expected_type in required_critical_fields.items():
            if payload["connection_status"] == "Connected":  # Перевіряємо лише для підключених пристроїв
                if key not in payload["critical_data"]:
                    raise ValueError(f"Поле {key} відсутнє у critical_data для {device_type}")
                if not isinstance(payload["critical_data"][key], expected_type):
                    raise ValueError(
                        f"Поле {key} має невірний тип у critical_data для {device_type}. Очікується {expected_type}"
                    )

    return True
