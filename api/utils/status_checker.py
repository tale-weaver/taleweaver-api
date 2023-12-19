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
    # print("============================ start check_book_status ==========================")
    books = Book.find_all_books()
    if not books:
        return {"msg": "No books"}, 400
    
    for book in books:

        if book['status'] == "finished":
            continue

        interval_ids = book["interval_ids"]
        timestrs = [interval["time_stamp"] for interval in interval_ids]
        target_idx_pre, target_idx_post = find_surrounding_datetime_indices(timestrs, now())
        target_status = interval_ids[target_idx_pre]['status']
        target_round = interval_ids[target_idx_pre]['round']
        
        # book information not equal to target status means it goes to next level            
        if book["status"] == "voting" and target_status != book["status"]:
            
            # if no book got candidate?

            # print(book["status"])
            pages = Page.find_pages_by_bookid(book["_id"])
            max_vote = 0
            for page in pages:
                
                page_id = page["page_id"]
                Page.update_status(page_id, "loser")
                target_vote = len(page["voted_by_user_ids"])
                if target_vote >= max_vote:
                    max_vote = target_vote
                    winner_page_id = page_id

            Page.update_status(winner_page_id, "winner")
            
            update_dict = {"status": target_status, "round": target_round, "updated_at": now()}            
            Book.update(book, update_dict)

            # print(book["title"] + " is updated to "+ target_status+ ", original status is "+ book["status"])

        elif book["status"] == "submitting" and target_status != book["status"]:
            
            # print(book["status"])
            update_dict = {"status": target_status, "round": target_round, "updated_at": now()}
            Book.update(book, update_dict)
            
            # print(book["title"] + " is updated to "+ target_status+ ", original status is "+ book["status"])
        
    # print("============================ end check_book_status ============================")
    # print('')