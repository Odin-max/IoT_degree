import json
from matplotlib import pyplot as plt

def load_data(file_path):
    """
    Завантаження даних із JSON-файлу.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        if 'iot_report' not in data:
            raise ValueError("JSON-файл не містить ключа 'iot_report'.")
        return data['iot_report']

def analyze_data(data):
    """
    Аналізує зібрані дані IoT.
    """
    if not data:
        raise ValueError("Дані порожні.")

    device_ids = [entry['device_id'] for entry in data]
    activity_levels = [entry['data_rate_kbps'] for entry in data]
    anomalies = [entry['anomaly'] for entry in data if entry['anomaly'] != "None"]

    # Підрахунок кількості унікальних пристроїв
    unique_devices = len(set(device_ids))

    # Аналіз рівнів активності
    average_data_rate = sum(activity_levels) / len(activity_levels)
    high_activity_devices = [entry for entry in data if entry['data_rate_kbps'] > 8000]

    return {
        "total_devices": len(device_ids),
        "unique_devices": unique_devices,
        "average_data_rate": average_data_rate,
        "anomalies_detected": anomalies,
        "high_activity_devices": high_activity_devices
    }

def visualize_results(analysis_results):
    """
    Візуалізує результати аналізу даних IoT.
    """
    labels = ['Total Devices', 'Unique Devices']
    values = [analysis_results['total_devices'], analysis_results['unique_devices']]

    # Бар-графік для кількості пристроїв
    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title("Кількість пристроїв в IoT-мережі")
    plt.ylabel("Кількість")
    plt.show()

    # Гістограма для швидкості передачі даних
    plt.hist(
        [entry['data_rate_kbps'] for entry in analysis_results['high_activity_devices']],
        bins=10,
        color='green',
        alpha=0.7
    )
    plt.title("Швидкість передачі даних для пристроїв з високою активністю")
    plt.xlabel("Швидкість передачі даних (kbps)")
    plt.ylabel("Кількість пристроїв")
    plt.show()

def main():
    file_path = 'iot_report.json'  # Шлях до JSON-файлу
    data = load_data(file_path)
    analysis_results = analyze_data(data)

    print("Результати аналізу:")
    print(f"Загальна кількість пристроїв: {analysis_results['total_devices']}")
    print(f"Кількість унікальних пристроїв: {analysis_results['unique_devices']}")
    print(f"Середня швидкість передачі даних: {analysis_results['average_data_rate']} kbps")
    print(f"Виявлено аномалії: {len(analysis_results['anomalies_detected'])}")
    print("Пристрої з високою активністю:")
    for device in analysis_results['high_activity_devices']:
        print(f"- ID: {device['device_id']}, Швидкість передачі даних: {device['data_rate_kbps']} kbps")

    visualize_results(analysis_results)

if __name__ == "__main__":
    main()
