from api.models.book import Book
from api.models.page import Page
from api.models.user import User
from api.models.comment import Comment
from api.utils.time import now
from api.utils.db import db

def initialize_data():
    collections = ["books", "pages", "users","comments"]
    list_of_collections = db.list_collection_names()
    if ("books" in list_of_collections) and ("pages" in list_of_collections) and ("users" in list_of_collections) and ("comments" in list_of_collections):
        print("Data already initialized")
        return
    if any(collection in list_of_collections for collection in collections):
        for collection in collections:
            db[collection].drop()
            print(f"{collection} dropped")
    user = [
        {
            "username": "user100",
            "password": "123",
            "email": "123@gmail.com",
            "role": "user",
            "source": "?",
        },
        {
            "username": "user200",
            "password": "223",
            "email": "223@gmail.com",
            "role": "premium",
            "source": "?",
        },
        {
            "username": "user300",
            "password": "323",
            "email": "323@gmail.com",
            "role": "premium",
            "source": "?",
        },
        {
            "username": "user400",
            "password": "423",
            "email": "423@gmail.com",
            "role": "premium",
            "source": "?",
        },
        {
            "username": "user500",
            "password": "523",
            "email": "523@gmail.com",
            "role": "premium",
            "source": "?",
        },
    ]
    interval_ids = [
        [
            "interval11",
            "interval12",
            "interval13",
            "interval14",
            "interval15",
            "interval16",
            "interval17",
            "interval18",
        ],
        [
            "interval21",
            "interval22",
            "interval23",
            "interval24",
            "interval25",
            "interval26",
            "interval27",
            "interval28",
        ],
    ]
    comment_ids = [
        [],
        [],
    ]
    book_status = ["submitting", "finished"]
    current_interval_id = ["interval18", "interval28"]
    like_lists = [[], []]
    books = [
        Book(
            title=f"book{i+1}",
            status=book_status[i],
            comment_ids=comment_ids[i],
            liked_by_user_ids=like_lists[i],
            interval_ids=interval_ids[i],
            current_interval_id=current_interval_id[i],
            created_at=now(),
            updated_at=now(),
        )
        for i in range(2)
    ]
    userlist = [
        User(
            username=user[i]["username"],
            password=user[i]["password"],
            email=user[i]["email"],
            role=user[i]["role"],
            source=user[i]["source"],
            liked_book_ids=[],
        )
        for i in range(len(user))
    ]  
    for user in userlist:
        user.save()
    comment = [
        {
            "commenter_id":userlist[0]._id, 
            "content":"hello1", 
        },
        {
            "commenter_id":userlist[2]._id, 
            "content":"hello2", 
        },
        {
            "commenter_id":userlist[3]._id, 
            "content":"hello3", 
        },
        {
            "commenter_id":userlist[0]._id, 
            "content":"hello4", 
        },
        {
            "commenter_id":userlist[2]._id, 
            "content":"hello5", 
        },
    ]
    commentlist = [
        Comment(
            commenter_id=comment[i]["commenter_id"],
            content=comment[i]["content"]
        )for i in range(len(comment))
    ]
    for comment in commentlist:
        comment.save()
    vote_list = [
        [userlist[1]._id, userlist[3]._id, userlist[0]._id],
        [userlist[2]._id, userlist[0]._id, userlist[1]._id, userlist[3]._id],
        [],
    ]
    descriptions = [
        "description1",
        "description2",
        "description3",
        "description4",
        "description5",
        "description6",
        "description7",
        "description8",
    ]
    creator_ids = [
        userlist[0]._id,
        userlist[1]._id,
        userlist[1]._id,
        userlist[1]._id,
        userlist[2]._id,
        userlist[3]._id,
        userlist[2]._id,
        userlist[0]._id,
        userlist[0]._id,
    ]
    for book in books:
        book.save()
    image_urls = [
        f"http://127.0.0.1:5000/data/{i+1}-{j+1}.png"
        for i in range(2)
        for j in range(8)
    ]
    for i in range(len(image_urls)):
        page = Page(
            image=image_urls[i],
            description=descriptions[i // 8],
            creator_id=creator_ids[i % 8],
            book_id=books[i // 8]._id,
            created_at=now(),
            interval_id=interval_ids[i // 8][i % 8],
            status="winner",
        )
        page.save()
        if i // 8 == 0:
            Book.push_new_page(books[0]._id, page._id)
        else:
            Book.push_new_page(books[1]._id, page._id)
    Page(
        image="http://127.0.0.1:5000/data/2-9.png",
        description="description9",
        creator_id="user9",
        book_id=books[1]._id,
        created_at=now(),
        updated_at=now(),
        interval_id="interval29",
        status="winner",
        voted_by_user_ids=[],
    ).save()
    Book.push_new_page(books[1]._id, page._id)
    for i in range(3):
        voting_page = Page(
            image=f"http://127.0.0.1:5000/data/1-9-{i+1}.png",
            description=f"description9-{i+1}",
            creator_id=f"user9-{i+1}",
            book_id=books[0]._id,
            created_at=now(),
            updated_at=now(),
            interval_id="interval19",
            status="ongoing",
            voted_by_user_ids=vote_list[i],
        )
        voting_page.save()
        Book.push_new_page(books[0]._id, voting_page._id)
    for comment in commentlist:
        Book.push_comment(books[0]._id,comment._id)
    Book.liked_by_user(books[0]._id, userlist[0]._id)
    Book.liked_by_user(books[1]._id, userlist[2]._id)
    books[0].save()
    print("Data initialized with 2 users 2 books and 20 pages!")