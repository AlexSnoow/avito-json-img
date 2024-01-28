import requests
import json

url = "https://www.avito.ru/web/1/js/items?locationId=629990&categoryId=98"
import_file = "import.json"
export_file = "export.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
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


def transform_item(input_item):
    output_item = {
        "id": input_item["id"],
        "title": input_item["title"],
        "description": input_item["description"],
        "urlPath": "https://www.avito.ru" + input_item["urlPath"],
        "priceValue": input_item.get("priceDetailed", {}).get("value", None),
    }

    # Adding images
    for i, image in enumerate(input_item.get("images", []), start=1):
        output_item[f"images{i}"] = image.get("864x648", None)

    # Adding date payload
    output_item["datePayload"] = next(
        (
            step["payload"]["absolute"]
            for step in input_item.get("iva", {}).get("DateInfoStep", [])
        ),
        None,
    )

    # Получаем информацию о профиле безопасным способом
    user_info_steps = input_item.get("iva", {}).get("UserInfoStep", [])
    if user_info_steps:
        profile_info = user_info_steps[0].get("payload", {})
        output_item["profileLink"] = profile_info.get("profile", {}).get("link", None)
        output_item["profileName"] = profile_info.get("profile", {}).get("title", None)
        output_item["profileRatingScore"] = profile_info.get("rating", {}).get(
            "score", None
        )
        output_item["profileRatingSummary"] = profile_info.get("rating", {}).get(
            "summary", None
        )
    else:
        # Если "UserInfoStep" пуст, устанавливаем значения по умолчанию
        output_item["profileLink"] = None
        output_item["profileName"] = None
        output_item["profileRatingScore"] = None
        output_item["profileRatingSummary"] = None

    # Adding profile closed items text
    output_item["profileClosedItemsText"] = input_item.get("closedItemsText", None)

    return output_item


def transform_json(input_json):
    output_json = {
        "catalog": {
            "items": [
                transform_item(item)
                for item in input_json.get("catalog", {}).get("items", [])
            ]
        }
    }
    return output_json


# Открываем файл с JSON данными
with open("import.json", "r", encoding="utf-8") as file:
    try:
        # Пытаемся загрузить JSON
        input_data = json.load(file)
    except json.JSONDecodeError as e:
        # Если произошла ошибка, выводим ее и выходим
        print(f"Error decoding JSON: {e}")
        exit()

# Преобразуем данные
output_data = transform_json(input_data)

# Записываем выходной JSON в файл
with open(export_file, "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=2)
