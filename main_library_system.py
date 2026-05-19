from library_system_oop import Library, Librarian, Member, Book

# 1. Initialize the system
city_library = Library("Metropolis Central Library")

# 2. Create Users (Librarian and Member)
alice_staff = Librarian(user_id="L01", name="Alice Smith", employee_id="EMP992")
bob_member = Member(user_id="M01", name="Bob Jones")

city_library.register_user(alice_staff)
city_library.register_user(bob_member)

# 3. Create Books
book1 = Book("978-0141439518", "Pride and Prejudice", "Jane Austen")
book2 = Book("978-0451524935", "1984", "George Orwell")

print("\n--- Testing Security Restrictions ---")
# Bob (a Member) tries to add a book to the library system
city_library.add_book(bob_member, book1) 

# Alice (a Librarian) adds the books correctly
city_library.add_book(alice_staff, book1)
city_library.add_book(alice_staff, book2)

city_library.display_inventory()

print("\n--- Testing Borrowing and Returning ---")
# Bob checks out Pride and Prejudice
city_library.checkout_book("M01", "978-0141439518")

# Someone else tries to check out the same book
city_library.checkout_book("M01", "978-0141439518")

city_library.display_inventory()

# Bob returns the book
city_library.return_book("M01", "978-0141439518")

city_library.display_inventory()