import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ----------- Backend Classes -----------


class Book:
    def __init__(self, title, author, book_id, quantity):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.quantity = quantity

    def __str__(self):
        return f"{self.book_id} | {self.title} | {self.author} | Available: {self.quantity}"

class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.borrowed_books = {}

    def __str__(self):
        return f"{self.user_id} | {self.username}"

    def borrow_book(self, book, return_date):
        if book.quantity > 0:
            self.borrowed_books[book.book_id] = (book, return_date)
            book.quantity -= 1
            return True
        return False

    def return_book(self, book):
        if book.book_id in self.borrowed_books:
            del self.borrowed_books[book.book_id]
            book.quantity += 1
            return True
        return False

    def list_borrowed_books(self):
        return "\n".join([f"{book.title} (Return by: {return_date})"
                          for book, return_date in self.borrowed_books.values()])

class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.logged_in_user = None

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def find_user(self, username):
        return next((user for user in self.users if user.username == username), None)

    def find_book_by_id(self, book_id):
        return next((book for book in self.books if book.book_id == book_id), None)

    def authenticate_user(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            self.logged_in_user = user
            return True
        return False

    def register_user(self, username, password):
        user_id = len(self.users) + 1
        user = User(user_id, username, password)
        self.add_user(user)
        return user

# ----------- Frontend with Tkinter -----------

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")  # Set the window size
        self.center_window()  # Center the window on the screen
        self.root.config(bg="black")  # Set background color of the root window to black
        self.library = Library()
        self.create_sample_data()  # Sample data for testing

        self.create_widgets()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 600
        window_height = 400
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_sample_data(self):
        # Sample Books
        self.library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1, 5))
        self.library.add_book(Book("1984", "George Orwell", 2, 3))
        self.library.add_book(Book("To Kill a Mockingbird", "Harper Lee", 3, 2))
        self.library.add_book(Book("Moby Dick", "Herman Melville", 4, 4))
        self.library.add_book(Book("Pride and Prejudice", "Jane Austen", 5, 6))
        self.library.add_book(Book("The Catcher in the Rye", "J.D. Salinger", 6, 3))
        self.library.add_book(Book("The Hobbit", "J.R.R. Tolkien", 7, 5))
        self.library.add_book(Book("Fahrenheit 451", "Ray Bradbury", 8, 2))
        self.library.add_book(Book("Brave New World", "Aldous Huxley", 9, 4))
        self.library.add_book(Book("The Lord of the Rings", "J.R.R. Tolkien", 10, 1))

        # Sample Users
        if not self.library.users:  # Only add sample users if the file is empty
            user1 = User(1, "alice", "password123")
            user2 = User(2, "bob", "password456")
            self.library.add_user(user1)
            self.library.add_user(user2)

    def create_widgets(self):
        self.login_frame = tk.Frame(self.root, bg="black")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username_label = tk.Label(self.login_frame, text="Username:", fg="white", bg="black")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:", fg="white", bg="black")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="gray40", fg="white")
        self.login_button.grid(row=2, column=0)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register, bg="gray40", fg="white")
        self.register_button.grid(row=2, column=1)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.library.find_user(username):
            messagebox.showerror("Error", "Username already exists.")
        else:
            user = self.library.register_user(username, password)
            messagebox.showinfo("Success", f"User '{username}' registered successfully.")
            self.show_login_screen()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.library.authenticate_user(username, password):
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_login_screen(self):
        if hasattr(self, 'dashboard_frame'):
            self.dashboard_frame.place_forget()

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_dashboard(self):
        self.login_frame.place_forget()
        self.dashboard_frame = tk.Frame(self.root, bg="black")
        self.dashboard_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.welcome_label = tk.Label(self.dashboard_frame, text="Welcome to the Library", fg="white", bg="black")
        self.welcome_label.grid(row=0, columnspan=2)

        self.book_list_label = tk.Label(self.dashboard_frame, text="Available Books:", fg="white", bg="black")
        self.book_list_label.grid(row=1, columnspan=2)

        self.book_listbox = tk.Listbox(self.dashboard_frame, height=10, width=50, bg="gray30", fg="white")
        self.book_listbox.grid(row=2, columnspan=2)

        self.update_book_listbox()

        self.borrow_button = tk.Button(self.dashboard_frame, text="Borrow Book", command=self.borrow_book, bg="gray40", fg="white")
        self.borrow_button.grid(row=3, column=0)

        self.return_button = tk.Button(self.dashboard_frame, text="Return Book", command=self.return_book, bg="gray40", fg="white")
        self.return_button.grid(row=3, column=1)

        self.view_borrowed_button = tk.Button(self.dashboard_frame, text="View Borrowed Books", command=self.view_borrowed_books, bg="gray40", fg="white")
        self.view_borrowed_button.grid(row=4, columnspan=2)

        self.logout_button = tk.Button(self.dashboard_frame, text="Logout", command=self.logout, bg="gray40", fg="white")
        self.logout_button.grid(row=5, columnspan=2)

    def update_book_listbox(self):
        # Clear current listbox
        self.book_listbox.delete(0, tk.END)

        # Populate the listbox with books
        for book in self.library.books:
            self.book_listbox.insert(tk.END, f"{book.title} (ID: {book.book_id}, Available: {book.quantity})")

    def borrow_book(self):
        if self.library.logged_in_user is None:
            messagebox.showerror("Error", "You must be logged in to borrow books.")
            return

        selected_book_index = self.book_listbox.curselection()
        if not selected_book_index:
            messagebox.showerror("Selection Error", "Please select a book to borrow.")
            return

        selected_book = self.library.books[selected_book_index[0]]
        return_date = "2024-11-20"  # Hardcoded return date for simplicity, can be made dynamic with user input

        if self.library.logged_in_user.borrow_book(selected_book, return_date):
            messagebox.showinfo("Success", f"Book '{selected_book.title}' borrowed successfully!")
            self.update_book_listbox()  # Update the book list after borrowing
        else:
            messagebox.showerror("Error", f"Sorry, '{selected_book.title}' is not available.")

    def return_book(self):
        if self.library.logged_in_user is None:
            messagebox.showerror("Error", "You must be logged in to return books.")
            return

        selected_book_index = self.book_listbox.curselection()
        if not selected_book_index:
            messagebox.showerror("Selection Error", "Please select a book to return.")
            return

        selected_book = self.library.books[selected_book_index[0]]

        if self.library.logged_in_user.return_book(selected_book):
            messagebox.showinfo("Success", f"Book '{selected_book.title}' returned successfully!")
            self.update_book_listbox()  # Update the book list after returning
        else:
            messagebox.showerror("Error", "This book is not in your borrowed list.")

    def view_borrowed_books(self):
        if self.library.logged_in_user is None:
            messagebox.showerror("Error", "You must be logged in to view borrowed books.")
            return

        borrowed_books_list = self.library.logged_in_user.list_borrowed_books()
        if borrowed_books_list:
            messagebox.showinfo("Borrowed Books", borrowed_books_list)
        else:
            messagebox.showinfo("No Borrowed Books", "You have not borrowed any books yet.")

    def logout(self):
        self.library.logged_in_user = None
        self.show_login_screen()

# ----------- Main Program -----------

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

import sqlite3

def create_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create table for books
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    quantity INTEGER
                 )''')

    # Create table for users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                 )''')

    # Create table for borrowed books (a junction table)
    c.execute('''CREATE TABLE IF NOT EXISTS borrowed_books (
                    user_id INTEGER,
                    book_id INTEGER,\
                    return_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    FOREIGN KEY(book_id) REFERENCES books(book_id)
                 )''')

    conn.commit()
    conn.close()

# Call this function to set up the database when the program starts
create_db()   
