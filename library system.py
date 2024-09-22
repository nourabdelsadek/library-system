import bisect
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, number):
        self.title = title
        self.author = author
        self.number = number
        self.available_copies = number
        self.borrowed_by = []

    def __str__(self):
        return f"'{self.title}' by {self.author} (Available: {self.available_copies}/{self.number})"

    def is_available(self):
        return self.available_copies > 0

    def borrow(self):
        if self.is_available():
            self.available_copies -= 1
        else:
            raise ValueError(f"Oops! No available copies of '{self.title}'.")

    def return_copy(self):
        if self.available_copies < self.number:
            self.available_copies += 1
        else:
            raise ValueError(f"All copies of '{self.title}' are already returned.")

    def add_borrower(self, account, due_date):
        self.borrowed_by.append((account, due_date))

    def next_available_date(self):
        if not self.borrowed_by:
            return None
        return min(due_date for _, due_date in self.borrowed_by)

class account:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book, days):
        if book.is_available():
            book.borrow()
            due_date = datetime.now() + timedelta(days=days)
            self.borrowed_books.append((book, due_date))
            book.add_borrower(self.name, due_date)
            print(f"{self.name} borrowed '{book.title}'. Due date: {due_date.date()}.")
        else:
            next_available = book.next_available_date()
            if next_available:
                print(f"Sorry, no copies of '{book.title}' available. Next available on: {next_available.date()}.")
            else:
                print(f"Sorry, no copies of '{book.title}' available.")

    def return_book(self, book, library):
        for borrowed_book, _ in self.borrowed_books:
            if borrowed_book == book:
                borrowed_book.return_copy()
                self.borrowed_books.remove((borrowed_book, _))
                print(f"{self.name} returned '{book.title}'.")
                if not self.borrowed_books:
                    rating = int(input(f"Rate your experience (1-5) after returning '{book.title}': "))
                    library.add_rating(rating)
                return
        print(f"{self.name} hasn't borrowed '{book.title}'.")

    def display(self):
        if not self.borrowed_books:
            print(f"{self.name} has no borrowed books.")
        else:
            print(f"{self.name} has borrowed:")
            for book, due_date in self.borrowed_books:
                print(f"- '{book.title}' (Due: {due_date.date()})")
            print(f"Total borrowed: {len(self.borrowed_books)}")

    def __str__(self):
        borrowed_titles = ', '.join([f"{book.title} by {book.author}" for book, _ in self.borrowed_books]) or "None"
        return f"account: {self.name}, Borrowed Books: {borrowed_titles}"

class Library:
    def __init__(self):
        self.books = []
        self.accounts = []
        self.ratings = []

    def add_book(self, title, author, number):
        existing_book = self.find_book(title, author)
        if existing_book:
            existing_book.number += number
            existing_book.available_copies += number
            print(f"Updated '{title}' by {author}. Total copies: {existing_book.number}.")
        else:
            new_book = Book(title, author, number)
            bisect.insort(self.books, new_book, key=lambda x: (x.title, x.author))
            print(f"Added '{title}' by {author} with {number} copies.")

    def remove_book(self, title, author):
        book = self.find_book(title, author)
        if book:
            self.books.remove(book)
            print(f"Removed '{title}' by {author} from the library.")
        else:
            print(f"'{title}' by {author} not found.")

    def add_account(self, name):
        account = account(name)
        self.accounts.append(account)
        print(f"Welcome, {name}! You've been added to the library.")

    def find_account(self, name):
        for account in self.accounts:
            if account.name == name:
                return account
        return None

    def find_book(self, title, author):
        l, r = 0, len(self.books) - 1
        while l <= r:
            mid = (l + r) // 2
            if (self.books[mid].title.ler(), self.books[mid].author.ler()) == (title.ler(), author.ler()):
                return self.books[mid]
            elif (self.books[mid].title.ler(), self.books[mid].author.ler()) < (title.ler(), author.ler()):
                l = mid + 1
            else:
                r = mid - 1
        return None

    def borrow_book(self, account_name, book_title, book_author, days):
        account = self.find_account(account_name)
        book = self.find_book(book_title, book_author)
        if not account:
            print(f"account '{account_name}' not found.")
            return
        if not book:
            print(f"Book '{book_title}' by {book_author} not found.")
            return
        account.borrow_book(book, days)

    def return_book(self, account_name, book_title, book_author):
        account = self.find_account(account_name)
        book = self.find_book(book_title, book_author)
        if not account:
            print(f"account '{account_name}' not found.")
            return
        if not book:
            print(f"Book '{book_title}' by {book_author} not found.")
            return
        account.return_book(book, self)

    def search_books(self, title=None, author=None):
        results = []
        if title and author:
            book = self.find_book(title, author)
            if book:
                results.append(book)
        elif title:
            for book in self.books:
                if title.ler() in book.title.ler():
                    results.append(book)
        elif author:
            for book in self.books:
                if author.ler() in book.author.ler():
                    results.append(book)
        return results

    def show_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            for book in self.books:
                print(book)

    def show_accounts(self):
        if not self.accounts:
            print("No accounts registered.")
        else:
            for account in self.accounts:
                print(account)

    def show_borrowedbooks(self, account_name):
        account = self.find_account(account_name)
        if account:
            account.display()
        else:
            print(f"account '{account_name}' not found.")

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.ratings.append(rating)
            print(f"Thanks for your feedback! You rated: {rating}.")
        else:
            print("Invalid rating. Please provide a number between 1 and 5.")

    def average_rating(self):
        if not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)

def interactive_menu():
    library = Library()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Add account")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Search Books")
        print("7. Show All Books")
        print("8. Show All accounts")
        print("9. Show account's Borrowed Books")
        print("10. Average Library Rating")
        print("11. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            title = input("Book title: ")
            author = input("Book author: ")
            number = int(input("Number of copies: "))
            library.add_book(title, author, number)
        elif choice == '2':
            title = input("Title to remove: ")
            author = input("Author: ")
            library.remove_book(title, author)
        elif choice == '3':
            name = input("New account name: ")
            library.add_account(name)
        elif choice == '4':
            account_name = input("account name: ")
            book_title = input("Title to borrow: ")
            book_author = input("Author: ")
            days = int(input("Days to borrow: "))
            library.borrow_book(account_name, book_title, book_author, days)
        elif choice == '5':
            account_name = input("account name: ")
            book_title = input("Title to return: ")
            book_author = input("Author: ")
            library.return_book(account_name, book_title, book_author)
        elif choice == '6':
            search_by = input("Search by title (t) or author (a)?: ").ler()
            if search_by == 't':
                title = input("Enter book title: ")
                results = library.search_books(title=title)
            elif search_by == 'a':
                author = input("Enter author name: ")
                results = library.search_books(author=author)
            else:
                print("Invalid choice.")
                continue
            if results:
                print("\nResults:")
                for book in results:
                    print(book)
            else:
                print("No books found !!")
        elif choice == '7':
            print("\nAll Books in the Library:")
            library.show_books()
        elif choice == '8':
            print("\nAll accounts in the Library:")
            library.show_accounts()
        elif choice == '9':
            account_name = input("account name for borrowed books: ")
            library.show_borrowedbooks(account_name)
        elif choice == '10':
            avg = library.average_rating()
            print(f"library rating: {avg:.2f}")
        elif choice == '11':
            print("bye bye.")
            break
        else:
            print("Please choose a right choice.")

if __name__ == "__main__":
    interactive_menu()
