import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
import random

# ---  People Dataset ---
people = [
    "mer", "rock", "sam", "David", "Eve", "Fay", "Grace", "Hank", "Ivy",
    "Jake", "Kiran", "Lily", "Meera", "Nina", "Oscar", "Priya", "Quinn",
    "Ravi", "Sita", "Tom", "Uma", "Vikram", "Wendy", "Xander", "Yara", "Zara", "Diana", "Ethan", "Fiona", "George", "Holly",
    "Ian", "Jasmine", "Kevin", "Laura", "Mike", "Nora", "Oliver", "Paula",
    "Quincy", "Rachel", "Steve", "Tina", "Umar", "Vera", "Will", "Xena", "Yusuf", "Zoe",
    "Aaron", "Bella", "Carter", "Daisy", "Eli", "Felicity", "Gavin", "Hannah", "Isaac", "Jade",
    "Kyle", "Luna", "Mason", "Nadia", "Owen", "Piper", "Quinn", "Riley", "Sean", "Tara",
    "Ulysses", "Violet", "Wyatt", "Xena", "Yara", "Zane", "Alice", "Brandon", "Cathy", "Derek", "Ella",
    "Frank", "Gina", "Henry", "Iris", "Jack", "Kathy", "Leo", "Maya", "Nate", "Olivia",
    "Paul", "Quinn", "Rita", "Sammy", "Tessa", "Ursula", "Victor", "Wendy", "Xander", "Yara", "Zoe"
]

# --- Random Friendships (undirected edges) ---
friendships = set()
while len(friendships) < len(people) * 2:  
    a, b = random.sample(people, 2)
    if a != b:
        friendships.add(tuple(sorted((a, b))))

# --- Create Graph ---
G = nx.Graph()
G.add_nodes_from(people)
G.add_edges_from(friendships)

# --- GUI App ---
class SocialNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Social Network Graph Analyzer")
        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children(): widget.destroy()
        tk.Label(self.root, text="Social Network Graph Analyzer", font=("Arial", 14)).pack(pady=10)

        ttk.Button(self.root, text="📌 Show Network Graph", command=self.show_graph).pack(pady=5)
        ttk.Button(self.root, text="📊 View Network Statistics", command=self.show_stats).pack(pady=5)
        ttk.Button(self.root, text="🔍 Analyze User Connections", command=self.analyze_user).pack(pady=5)
        ttk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)

    def show_graph(self):
        plt.figure(figsize=(10, 6))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=1000, edge_color='gray', font_size=10)
        plt.title("🌐 Social Network Graph")
        plt.tight_layout()
        plt.show()

    def show_stats(self):
        num_users = G.number_of_nodes()
        num_connections = G.number_of_edges()
        degrees = [val for (node, val) in G.degree()]
        avg_deg = sum(degrees) / num_users

        messagebox.showinfo("📊 Network Statistics", 
            f"Total Users: {num_users}\n"
            f"Total Connections: {num_connections}\n"
            f"Average Connections/User: {avg_deg:.2f}"
        )

    def analyze_user(self):
        win = tk.Toplevel(self.root)
        win.title("🔍 Analyze User")
        tk.Label(win, text="Select a user:").pack(pady=5)
        user_var = tk.StringVar()
        user_dropdown = ttk.Combobox(win, textvariable=user_var, values=people)
        user_dropdown.pack(pady=5)

        def show_info():
            user = user_var.get()
            if user not in G.nodes:
                messagebox.showerror("Error", "Invalid user.")
                return
            friends = list(G.neighbors(user))
            msg = f"{user} has {len(friends)} friends:\n" + ", ".join(friends)
            messagebox.showinfo("User Connections", msg)

        ttk.Button(win, text="Show Connections", command=show_info).pack(pady=5)

# --- Run App ---
root = tk.Tk()
root.geometry("400x300")
app = SocialNetworkApp(root)
root.mainloop()
