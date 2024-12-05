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

    # Перевірка на допустимі символи в текстових полях
    text_fields = ["device_id", "device_type", "manufacturer", "first_name", "last_name"]
    for field in text_fields:
        if not re.match(r"^[a-zA-Z0-9\s\-_,.]*$", payload[field]):
            raise ValueError(f"Невалідні символи в полі {field}")

    # Перевірка на JSON-формат критичних даних
    try:
        json.dumps(payload["critical_data"])
    except (TypeError, ValueError):
        raise ValueError("Поле critical_data не є валідним JSON")

    return True
