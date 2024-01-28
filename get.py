# get.py

import os
import requests
import json
import subprocess
from config import SAVE_PATH, SAVE_PATH_PC, SAVE_PATH_NB, FILE_EXPORT_JSON  # Импортируем переменные из config.py

def get_save_path(category_id):
    if category_id == 31:
        return SAVE_PATH_PC
    elif category_id == 98:
        return SAVE_PATH_NB
    else:
        return SAVE_PATH

def save_images(item):
    item_id = str(item["id"])
    category_id = item.get("categoryId")

    # Получаем путь в зависимости от categoryId
    folder_path = os.path.join(get_save_path(category_id), item_id)

    # folder_path = os.path.join(SAVE_PATH, item_id)

    # Создаем папку с именем id, если ее нет
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Сохраняем изображения в папке
    for i in range(1, 11):
        image_key = f"images{i}"
        if image_key in item:
            image_url = item[image_key]
            image_name = f"image_{i}.jpg"
            image_path = os.path.join(folder_path, image_name)

            # Проверяем, существует ли файл
            if not os.path.exists(image_path):
                # Загружаем изображение
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, "wb") as image_file:
                        image_file.write(response.content)
                        print(f"Изображение {image_name} сохранено по пути: {image_path}")
            else:
                print(f"Изображение {image_name} уже существует по пути: {image_path}")


def write_id_description_to_text(items, output_file):
    with open(output_file, "w", encoding="utf-8") as text_file:
        for item in items:
            item_id = item.get("id")
            description = item.get("description")

            if item_id and description:
                text_file.write(f"ID: {item_id}\n")
                text_file.write(f"Description: {description}\n\n")


if __name__ == "__main__":
    try:
        # Теперь вызываем json_convert.py
        subprocess.run(["python", "json_convert.py"])

        with open(FILE_EXPORT_JSON, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        items = json_data.get("catalog", {}).get("items", [])

        for item in items:
            save_images(item)
        
        # Записываем id и description в текстовый файл
        output_text_file = "id_description_output.txt"
        write_id_description_to_text(items, output_text_file)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
