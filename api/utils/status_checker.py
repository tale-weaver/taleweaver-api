from api.models.book import Book
from api.models.page import Page
from api.utils.time import now, find_surrounding_datetime_indices

# find all submitting books ->
# if book has less than 9 pages -> update book status to voting
# if book  9 pages -> update book status to finished

# find all voting books ->
# if book has less than 9 pages -> update book status to submitting
# choose winner page -> update page status to winner -> update
def check_book_status():
    print("start check_book_status")
    books = Book.find_all_books()

    for book in books:

        interval_ids = book["interval_ids"]
        timestrs = [interval["time_stamp"] for interval in interval_ids]
        target_idx_pre, target_idx_post = find_surrounding_datetime_indices(timestrs, now())
        target_status = book['status']
        next_status = interval_ids[target_idx_post]['status']
        target_round = book['round']
        next_round = interval_ids[target_idx_post]['round']
        if target_status == "finished":
            continue
        

        # book information not equal to target status means it goes to next level            
        if target_status == "voting" and target_status != book["status"]:
            pages = Page.find_pages_by_bookid(book["_id"])

            for page in pages:
                max_vote = 0
                Page.update_status(page, "loser")
                if len(page["voted_by_user_ids"]) >= max_vote:
                    max_vote = len(page["voted_by_user_ids"])
                    winner_page_id = page['_id']
            
            winner_page = Page.find_by_id(winner_page_id)
            Page.update_status(winner_page, "winner")

            winner_pages = book["page_ids"]
            winner_pages.append(winner_page_id)      
            update_dict = {"page_ids": winner_pages, "status": next_status, "round": next_round}
            Book.update(book, update_dict)
            
            print(book["title"] + "update to "+ book["status"]+ "supposed to be "+ next_status)

        elif target_status == "submitting" and target_status != book["status"]:
            update_dict = {"status": next_status, "round": next_round}
            Book.update(book, update_dict)
            
            print(book["title"] + "update to "+ book["status"]+ "supposed to be "+ next_status)
    print("end check_book_status")