import os
import shutil
import random
from urllib.parse import urljoin
from bson import ObjectId

from api.models.book import Book
from api.models.page import Page
from api.models.user import User
from api.models.comment import Comment
from api.utils.init_db_helpers import extract_and_distribute_images, extract_and_distribute_cover_images, get_image_paths, read_json_file, divide_list
from api.utils.db import db
from api.config.config import Config
from api.utils.time import now, create_time_intervals, find_surrounding_datetime_indices


def db_init(image_base_folder="./bin", img_zip_file_path="./images.zip", cover_zip_file_path="./covers.zip", json_folder_path="./jsons"):

    collections = db.list_collection_names()

    # drop all collections
    if collections:
        for collection in collections:
            db[collection].drop()
            print(f"Collection: {collection} dropped...")

    # create collections
    collections = ["books", "pages", "users", "comments"]
    for collection in collections:
        db.create_collection(collection)
        print(f"Collection: {collection} created...")

    # read json files
    users_data = read_json_file(os.path.join(json_folder_path, "user.json"))
    books_data = read_json_file(os.path.join(json_folder_path, "book.json"))
    pages_data = read_json_file(os.path.join(json_folder_path, "page.json"))
    comments_data = read_json_file(
        os.path.join(json_folder_path, "comment.json"))
    print("Json files read...")

    # create users
    for user in users_data:
        User(**user, is_verified=True).save()
    print("Users created...")

    # get users
    users = User.get_all()
    users_ids = [str(user["_id"]) for user in users]

    # process images
    if os.path.exists(image_base_folder):
        shutil.rmtree(image_base_folder, ignore_errors=True)

    extract_and_distribute_images(
        img_zip_file_path, image_base_folder, users_ids)
    users_image_paths = {user_id: get_image_paths(
        os.path.join(image_base_folder, user_id)) for user_id in users_ids}
    print("Images processed...")

    # create pages
    for _id in users_image_paths:
        for image_path in users_image_paths[_id]:
            random_title_description = random.choice(pages_data)
            Page(
                image=urljoin(Config.BACKEND_URL,
                              image_path.replace('\\', '/')),
                **random_title_description,
                creator_id=ObjectId(_id),
                # TODO: design create_at
            ).save()
    print("Pages created...")

    # create comments
    for comment in comments_data:
        Comment(
            **comment,
            commenter_id=ObjectId(random.choice(users_ids)),
            # TODO: design create_at
        ).save()
    print("Comments created...")

    # get pages
    pages = Page.get_all()
    # no need to convert to string as we need ObjectId
    pages_ids = [page["_id"] for page in pages]

    # get comments
    comments = Comment.get_all()
    # no need to convert to string as we need ObjectId
    comments_ids = [comment["_id"] for comment in comments]

    # create books
    len_books_data = len(books_data)
    pages_ids_chunks = divide_list(pages_ids, len_books_data)
    comments_ids_chunks = divide_list(comments_ids, len_books_data)

    # create each book
    for i in range(len_books_data):
        vintage_time = -i*Config.INTERVAL_TIME*2.5
        created_at = now(vintage_time)
        interval_ids = create_time_intervals(created_at)

        timestrs = [interval["time_stamp"] for interval in interval_ids]
        target_idx, _ = find_surrounding_datetime_indices(timestrs, now())
        target_stage = interval_ids[target_idx]

        book = Book(
            **books_data[i],
            page_ids=pages_ids_chunks[i],
            comment_ids=comments_ids_chunks[i],
            # TODO: design interval_ids
            interval_ids=interval_ids,
            created_at=created_at,
        )

        book.status = target_stage['status']
        book.round = target_stage['round']

        book.save()
        print(f"Book {i+1} created...")

        # update pages
        # let's say round = 3, hence round 1 and round 2 have winners
        for j in range(int(book.round - 1)):
            Page.update_status(book.page_ids[j], "winner")
            Page.update_created_at(
                book.page_ids[j], book.interval_ids[j*2]["time_stamp"])
        print(f"Status and Created Time of Pages of Book {i+1} is updated...")

    # finally let's assign cover images to books
    books = Book.get_all()
    books_ids = [str(book["_id"]) for book in books]
    extract_and_distribute_cover_images(
        cover_zip_file_path, image_base_folder, books_ids)
    books_covers_paths = {book_id: get_image_paths(os.path.join(
        image_base_folder, book_id))[0] for book_id in books_ids}

    for book_id in books_ids:
        cover_path = books_covers_paths[book_id]
        cover_url = urljoin(Config.BACKEND_URL, cover_path.replace('\\', '/'))
        Book.update_cover(book_id, cover_url)

    print("Cover images of all books are updated...")

    print("All books created...")
