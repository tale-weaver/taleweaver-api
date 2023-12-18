import zipfile
import os
import random
import json


def extract_and_distribute_images(zip_path, base_folder, usernames):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        image_files = [file for file in zip_ref.namelist(
        ) if file.endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(image_files)

        user_folders = {username: os.path.join(
            base_folder, username) for username in usernames}
        for folder in user_folders.values():
            if not os.path.exists(folder):
                os.makedirs(folder)

        while image_files:
            for username in usernames:
                if not image_files:
                    break
                selected_image = image_files.pop()
                image_name = os.path.basename(selected_image)
                destination_path = os.path.join(
                    user_folders[username], image_name)
                with open(destination_path, 'wb') as f:
                    f.write(zip_ref.read(selected_image))


def get_image_paths(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))

    return image_paths


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def divide_list(lst, n, shuffle=True):
    lst = lst.copy()

    if shuffle:
        random.shuffle(lst)

    chunk_size = len(lst) // n
    remainder = len(lst) % n

    chunks = []
    start = 0
    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(lst[start:end])
        start = end

    return chunks
