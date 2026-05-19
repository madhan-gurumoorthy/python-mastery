class Book:
    """Represents a book in the library."""
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_borrowed = False  # Encapsulation: Protected attribute

    def is_available(self) -> bool:
        return not self._is_borrowed

    def borrow(self) -> bool:
        if self.is_available():
            self._is_borrowed = True
            return True
        return False

    def return_book(self):
        self._is_borrowed = False

    def __str__(self) -> str:
        status = "Available" if self.is_available() else "Borrowed"
        return f"'{self.title}' by {self.author} [ISBN: {self.isbn}] - {status}"


class User:
    """Base class representing a general user (Inheritance)."""
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    def get_role(self) -> str:
        return "General User"


class Member(User):
    """Derived class representing a library member who can borrow books."""
    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name)
        self.borrowed_books = []  # Composition: Stores Book objects

    def get_role(self) -> str:  # Polymorphism: Overriding base method
        return "Member"

    def borrow_book(self, book: Book) -> bool:
        if book.borrow():
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book: Book) -> bool:
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        return False


class Librarian(User):
    """Derived class representing a staff member who manages the library."""
    def __init__(self, user_id: str, name: str, employee_id: str):
        super().__init__(user_id, name)
        self.employee_id = employee_id

    def get_role(self) -> str:  # Polymorphism
        return "Librarian"


class Library:
    """The central management system (The 'Facade' object)."""
    def __init__(self, name: str):
        self.name = name
        self.books = {}    # Stores ISBN -> Book object
        self.users = {}    # Stores User_ID -> User object

    # --- Librarian Actions ---
    def add_book(self, librarian: Librarian, book: Book):
        """Only librarians are allowed to add books."""
        if isinstance(librarian, Librarian):
            self.books[book.isbn] = book
            print(f"[Success] Librarian {librarian.name} added: {book.title}")
        else:
            print("[Access Denied] Only librarians can add books.")

    def register_user(self, user: User):
        self.users[user.user_id] = user
        print(f"[Success] Registered {user.get_role()}: {user.name}")

    # --- Member Actions ---
    def checkout_book(self, member_id: str, isbn: str):
        member = self.users.get(member_id)
        book = self.books.get(isbn)

        if not isinstance(member, Member):
            print("[Error] Invalid member ID or user is not a regular Member.")
            return

        if not book:
            print("[Error] Book not found in library inventory.")
            return

        if member.borrow_book(book):
            print(f"[Success] {member.name} successfully checked out '{book.title}'.")
        else:
            print(f"[Failure] '{book.title}' is already checked out.")

    def return_book(self, member_id: str, isbn: str):
        member = self.users.get(member_id)
        book = self.books.get(isbn)

        if isinstance(member, Member) and book:
            if member.return_book(book):
                print(f"[Success] {member.name} returned '{book.title}'.")
            else:
                print(f"[Error] {member.name} does not have this book checked out.")
        else:
            print("[Error] Invalid member or book details.")

    # --- System Status ---
    def display_inventory(self):
        print(f"\n--- {self.name} Current Inventory ---")
        if not self.books:
            print("The library is currently empty.")
        for book in self.books.values():
            print(f" - {book}")
        print("-" * 35)




"""
OOP Principles Applied:
Encapsulation: The Book class protects its state (_is_borrowed). Outside objects cannot change it directly; they must use the borrow() or return_book() methods, enforcing safety rules.

Inheritance: Member and Librarian inherit common traits like user_id and name from the User superclass, eliminating redundant code.

Polymorphism: The get_role() method is implemented in the parent class but overridden differently by both child classes. The library system handles them dynamically based on their specific behavior type. 
"""