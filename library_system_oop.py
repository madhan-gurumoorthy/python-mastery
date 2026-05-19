from abc import ABC, abstractmethod

# ==========================================
# 1. ABSTRACTION (Abstract Base Class)
# ==========================================
class User(ABC):
    """
    Abstract Base Class representing a template for all users.
    This class cannot be instantiated directly.
    """
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self) -> str:
        """
        Abstract Method: Every subclass MUST implement this method
        to define its unique role permissions.
        """
        pass


# ==========================================
# 2. ENCAPSULATION (Data Protection)
# ==========================================
class Book:
    """Represents a book in the library, encapsulating its borrow state."""
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_borrowed = False  # Protected attribute (Encapsulation)

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


# ==========================================
# 3. INHERITANCE & POLYMORPHISM
# ==========================================
class Member(User):  # Inheritance
    """A library member who can check out and return books."""
    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name)
        self.borrowed_books = []  # Composition: Holds Book objects

    def get_role(self) -> str:  # Polymorphism: Overriding abstract method
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


class Librarian(User):  # Inheritance
    """A staff member authorized to manage library inventory."""
    def __init__(self, user_id: str, name: str, employee_id: str):
        super().__init__(user_id, name)
        self.employee_id = employee_id

    def get_role(self) -> str:  # Polymorphism: Overriding abstract method
        return "Librarian"


# ==========================================
# 4. ORCHESTRATION (The Library Facade)
# ==========================================
class Library:
    """Central orchestration object to manage books and users."""
    def __init__(self, name: str):
        self.name = name
        self.books = {}    # ISBN -> Book mapping
        self.users = {}    # User_ID -> User mapping

    def add_book(self, librarian: Librarian, book: Book):
        """Strictly enforces that only Librarians can add inventory."""
        if isinstance(librarian, Librarian):
            self.books[book.isbn] = book
            print(f"[Success] Librarian {librarian.name} added: {book.title}")
        else:
            print("[Access Denied] Only authorized librarians can add inventory.")

    def register_user(self, user: User):
        """Accepts any valid subclass of User."""
        self.users[user.user_id] = user
        print(f"[Success] Registered {user.get_role()}: {user.name}")

    def checkout_book(self, member_id: str, isbn: str):
        member = self.users.get(member_id)
        book = self.books.get(isbn)

        if not isinstance(member, Member):
            print("[Error] Access Denied: User is not an active library Member.")
            return

        if not book:
            print("[Error] Inventory Error: Book not found.")
            return

        if member.borrow_book(book):
            print(f"[Success] {member.name} checked out '{book.title}'.")
        else:
            print(f"[Failure] '{book.title}' is currently unavailable.")

    def return_book(self, member_id: str, isbn: str):
        member = self.users.get(member_id)
        book = self.books.get(isbn)

        if isinstance(member, Member) and book:
            if member.return_book(book):
                print(f"[Success] {member.name} successfully returned '{book.title}'.")
            else:
                print(f"[Error] {member.name} does not hold a reservation for this book.")
        else:
            print("[Error] Action failed. Verify member ID and book ISBN.")

    def display_inventory(self):
        print(f"\n--- {self.name} Current Inventory ---")
        if not self.books:
            print("No catalog items found.")
        for book in self.books.values():
            print(f" - {book}")
        print("-" * 40)