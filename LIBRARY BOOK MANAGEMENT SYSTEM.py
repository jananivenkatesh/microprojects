import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from fpdf import FPDF
import matplotlib.pyplot as plt
import hashlib
import datetime
import random

# --- Book Dataset (100 books) ---
real_books = [
    ("Clean Code", "Robert C. Martin"),
    ("The Pragmatic Programmer", "Andrew Hunt"),
    ("Introduction to Algorithms", "Cormen"),
    ("Artificial Intelligence", "Stuart Russell"),
    ("Python Crash Course", "Eric Matthes"),
    ("Cracking the Coding Interview", "Gayle Laakmann McDowell"),
    ("Design Patterns", "Erich Gamma"),
    ("Operating System Concepts", "Silberschatz"),
    ("Computer Networks", "Andrew S. Tanenbaum"),
    ("Deep Learning", "Ian Goodfellow"),
    ("The Mythical Man-Month", "Frederick P. Brooks"),
    ("Refactoring", "Martin Fowler"),
    ("Structure and Interpretation of Computer Programs", "Abelson & Sussman"),
    ("Code Complete", "Steve McConnell"),
    ("Fluent Python", "Luciano Ramalho"),
    ("Head First Design Patterns", "Eric Freeman"),
    ("Learning Python", "Mark Lutz"),
    ("Grokking Algorithms", "Aditya Bhargava"),
    ("Effective Java", "Joshua Bloch"),
    ("Algorithms", "Robert Sedgewick"),
    ("Machine Learning", "Tom M. Mitchell"),
    ("Elements of Programming Interviews", "Adnan Aziz"),
    ("You Don’t Know JS", "Kyle Simpson"),
    ("Computer Organization", "Carl Hamacher"),
    ("Let Us C", "Yashavant Kanetkar"),
    ("Digital Design", "M. Morris Mano"),
    ("Database System Concepts", "Abraham Silberschatz"),
    ("Operating Systems: Three Easy Pieces", "Remzi Arpaci-Dusseau"),
    ("Modern Operating Systems", "Andrew Tanenbaum"),
    ("Introduction to the Theory of Computation", "Michael Sipser"),
    ("C Programming Language", "Kernighan and Ritchie"),
    ("Introduction to Machine Learning", "Ethem Alpaydin"),
    ("Java: The Complete Reference", "Herbert Schildt"),
    ("JavaScript: The Good Parts", "Douglas Crockford"),
    ("Data Structures and Algorithms Made Easy", "Narasimha Karumanchi"),
    ("Computer Architecture", "David Patterson"),
    ("Automate the Boring Stuff with Python", "Al Sweigart"),
    ("The C++ Programming Language", "Bjarne Stroustrup"),
    ("Effective C++", "Scott Meyers"),
    ("Linux Command Line", "William E. Shotts"),
    ("Learning SQL", "Alan Beaulieu"),
    ("Head First Java", "Kathy Sierra"),
    ("Beginning Python", "Magnus Lie Hetland"),
    ("Python Data Science Handbook", "Jake VanderPlas"),
    ("Think Python", "Allen B. Downey"),
    ("The Art of Computer Programming", "Donald Knuth"),
    ("AI: A Modern Approach", "Russell & Norvig"),
    ("Data Science from Scratch", "Joel Grus"),
    ("Hands-On Machine Learning", "Aurélien Géron"),
    ("Network Security Essentials", "William Stallings"),
] * 2  

books = []
for i, (title, author) in enumerate(real_books[:100], 1):
    books.append({"id": i, "title": title, "author": author, "available": True})

# --- Users Dataset (readers) ---
usernames = [
    "meredith", "john", "priya", "kiran", "rohit", "ayesha", "raj", "fatima","arjun", "neha", "vikram", "meera", "rahul", "anjali", "sneha","siddharth", "nisha", "tanvi", "aman", "isha", "karan", "deepak", "ravi", "sara", "naveen", "pallavi", "anil", "shreya", "vishal", "priya", "akshay", "isha", "sahil", "neeraj", "divya", "rohan", "kavita", "manish", "pooja", "suresh", "geeta", "ashok", "rani", "sunil", "komal", "arvind", "jyoti", "amit", "pradeep", "neelam", "suman", "vinay", "anita", "gagan", "shyam"
]
users = {}
for uname in usernames:
    borrowed = random.sample(range(1, 101), random.randint(1, 5))
    renewal = (datetime.datetime.now() + datetime.timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')
    users[uname] = {"borrowed_books": borrowed, "renewal_date": renewal}

for u in users.values():
    for bid in u["borrowed_books"]:
        for b in books:
            if b["id"] == bid:
                b["available"] = False

accounts = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "viewer": hashlib.sha256("viewer123".encode()).hexdigest()
}
roles = {"admin": "admin", "viewer": "viewer"}

# --- GUI Class ---
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Book Management System")
        self.role = None
        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children(): widget.destroy()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()
        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        uname = self.username.get()
        pwd = self.password.get()
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        if uname in accounts and accounts[uname] == hashed:
            self.role = roles[uname]
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def main_menu(self):
        for widget in self.root.winfo_children(): widget.destroy()
        tk.Label(self.root, text=f"Welcome ({self.role.title()})", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="View Books", command=self.view_books).pack(pady=5)
        if self.role == "admin":
            ttk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=5)
            ttk.Button(self.root, text="Renew Book", command=self.renew_book).pack(pady=5)
        ttk.Button(self.root, text="Generate PDF Report", command=self.generate_pdf).pack(pady=5)
        ttk.Button(self.root, text="Visualize Borrowed Books", command=self.visualize_data).pack(pady=5)
        ttk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def view_books(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("📖 Book List")
        tree = ttk.Treeview(view_win, columns=("ID", "Title", "Author", "Status"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        for book in books:
            status = "Available" if book["available"] else "Issued"
            tree.insert("", "end", values=(book["id"], book["title"], book["author"], status))
        tree.pack(expand=True, fill='both')

    def add_book(self):
        title = simpledialog.askstring("Input", "Enter book title:")
        author = simpledialog.askstring("Input", "Enter author name:")
        if title and author:
            book_id = max(book["id"] for book in books) + 1
            books.append({"id": book_id, "title": title, "author": author, "available": True})
            messagebox.showinfo("Success", f"Book '{title}' added.")
        else:
            messagebox.showwarning("Cancelled", "Book not added.")

    def renew_book(self):
        uname = simpledialog.askstring("Input", "Enter username to renew:")
        if uname in users:
            new_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')
            users[uname]["renewal_date"] = new_date
            messagebox.showinfo("Success", f"Renewed for {uname} till {new_date}")
        else:
            messagebox.showerror("Error", "User not found.")

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Library Book Report", ln=True, align='C')
        pdf.ln(5)
        for book in books:
            status = "Available" if book["available"] else "Issued"
            pdf.cell(200, 10, txt=f"{book['id']} - {book['title']} by {book['author']} [{status}]", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt="User Borrow Details", ln=True)
        for user, info in users.items():
            book_ids = ', '.join(map(str, info["borrowed_books"]))
            pdf.cell(200, 10, txt=f"{user}: {book_ids} | Renew: {info['renewal_date']}", ln=True)
        pdf.output("Library_Report.pdf")
        messagebox.showinfo("PDF Created", "Saved as 'Library_Report.pdf'")

    def visualize_data(self):
        user_names = list(users.keys())
        book_counts = [len(info["borrowed_books"]) for info in users.values()]
        plt.figure(figsize=(10, 5))
        plt.bar(user_names, book_counts, color='darkcyan')
        plt.xticks(rotation=45)
        plt.title("📊 Books Borrowed by Users")
        plt.xlabel("User")
        plt.ylabel("Books Borrowed")
        plt.tight_layout()
        plt.show()

# --- Run App ---
root = tk.Tk()
root.geometry("400x450")
app = LibraryApp(root)
root.mainloop()
