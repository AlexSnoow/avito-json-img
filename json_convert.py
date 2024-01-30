# json_convert.py
import json


def transform_item(input_item):
    output_item = {
        "id": input_item["id"],
        "categoryId": input_item["categoryId"],
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
        try:
            output_item["profileRatingScore"] = profile_info.get("rating", {}).get("score", None)
            output_item["profileRatingSummary"] = profile_info.get("rating", {}).get("summary", None)
        except:
            pass
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


# Открываем файл list-spij.txt и читаем уже имеющиеся значения "id"
existing_ids = set()
with open("list-spij.txt", "r", encoding="utf-8") as list_file:
    for line in list_file:
        existing_ids.add(int(line.strip()))

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

# Записываем выходной JSON в файл export.json только с уникальными id
with open("export.json", "w", encoding="utf-8") as file:
    for item in output_data.get("catalog", {}).get("items", []):
        item_id = item.get("id")
        if item_id is not None and item_id not in existing_ids:
            json.dump(item, file, ensure_ascii=False)
            file.write("\n")

# Дополняем файл list-spij.txt новыми значениями "id"
with open("list-spij.txt", "a", encoding="utf-8") as list_file:
    for item in output_data.get("catalog", {}).get("items", []):
        item_id = item.get("id")
        if item_id is not None:
            list_file.write(str(item_id) + "\n")