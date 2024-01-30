import requests
import json

url = "https://www.avito.ru/web/1/js/items?locationId=629990&categoryId=98"
import_file = "import.json"
export_file = "export.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.avito.ru",
}

try:
    # Отправляем GET-запрос по указанной ссылке
    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем JSON из ответа
        json_data = response.json()

        # Записываем JSON в файл (с режимом перезаписи)
        with open(import_file, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)
        print(f"JSON успешно перезаписан в файл '{import_file}'")
    else:
        print(f"Ошибка при запросе: {response.status_code}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
