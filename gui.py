import tkinter as tk
from tkinter import ttk, messagebox, Menu
import json
import os
from dataclasses import dataclass, field
from typing import Any

from user import user, UserListManager
from product import Product, ProductListManager
from k_top_calculator import calculator
from recommand_system import RecommendationSystem

# ------------ Configuration File ------------
USER_DATA_FILE = "users.json"
PRODUCT_DATA_FILE = "products.json"

# ------------ Data Persistence Logic ------------
def _add_default_products(manager: ProductListManager):
    categories = ["phone", "computer", "earphones", "ipad", "camera"]
    for i in range(1, 21):
        p = Product(f"electronic products{i:02d}")
        p.set_price(199 + (i * 150) % 5000)
        p.set_sales(0)
        p.set_score(0)
        p.set_category(categories[i % len(categories)])
        manager.add_product(p)


def load_users():
    if not os.path.exists(USER_DATA_FILE): return []
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except: return []
    users = []
    for u_dict in data:
        u = user(u_dict['username'], u_dict['password'])
        u.prefer_item = u_dict.get('prefer_item', [])
        u.score_item = u_dict.get('score_item', {})
        users.append(u)
    return users

def save_users(users):
    data = []
    for u in users:
        data.append({
            'username': u.get_username(),
            'password': u.get_password(),
            'prefer_item': u.prefer_item,
            'score_item': u.score_item
        })
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_products(manager: ProductListManager):
    if not os.path.exists(PRODUCT_DATA_FILE):
        _add_default_products(manager)
        save_products(manager)
        return

    try:
        with open(PRODUCT_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            _add_default_products(manager)
            save_products(manager)
            return
            
        for p_dict in data:
            p = Product(p_dict['name'])
            p.set_price(p_dict.get('price', 0))
            p.set_sales(p_dict.get('sales', 0))
            p.set_score(p_dict.get('score', 0))
            p.set_category(p_dict.get('category', ''))
            manager.add_product(p)
    except:
        _add_default_products(manager)
        save_products(manager)

def save_products(manager: ProductListManager):
    data = []
    for p in manager.get_product_list():
        data.append({
            'name': p.get_name(),
            'price': p.get_price(),
            'sales': p.get_sales(),
            'score': p.get_score(),
            'category': p.get_category()
        })
    with open(PRODUCT_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Recommendation Logic Helper ----------
def get_recommendations(current_user, user_manager, product_manager, threshold=0.3):
    if not current_user or not current_user.get_score_item():
        return []
    rec_sys = RecommendationSystem(user_manager, product_manager)
    return rec_sys.recommend_for_user(current_user, threshold)

# ---------- Main GUI Class ----------
class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Shopping Recommendation System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f5f5')
        self.root.withdraw()

        self.user_manager = UserListManager()
        self.product_manager = ProductListManager()

        self.users = load_users()
        for u in self.users:
            self.user_manager.add_user(u)
        load_products(self.product_manager)

        self.current_user = None
        self.rating_window = None
        self.selected_product = None

        self.show_login_register()

    def show_login_register(self):
        self.login_win = tk.Toplevel(self.root)
        self.login_win.title("Login / Register")
        self.login_win.geometry("350x300")
        self.login_win.resizable(False, False)
        self.login_win.grab_set()
        self.login_win.protocol("WM_DELETE_WINDOW", self.quit_app)

        main_frame = tk.Frame(self.login_win, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Welcome to Shopping System", font=('Microsoft YaHei', 14, 'bold'),
                 bg='#f0f0f0', fg='#ff6600').grid(row=0, column=0, columnspan=2, pady=(0,20))

        tk.Label(main_frame, text="Username:", font=('Microsoft YaHei', 10), bg='#f0f0f0').grid(row=1, column=0, sticky='e', pady=5)
        self.login_username = tk.Entry(main_frame, width=25, font=('Microsoft YaHei', 10))
        self.login_username.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(main_frame, text="Password:", font=('Microsoft YaHei', 10), bg='#f0f0f0').grid(row=2, column=0, sticky='e', pady=5)
        self.login_password = tk.Entry(main_frame, width=25, font=('Microsoft YaHei', 10), show="*")
        self.login_password.grid(row=2, column=1, pady=5, padx=(10,0))

        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Login", command=self.do_login, bg='#ff6600', fg='white', width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Register", command=self.show_register, bg='#3399ff', fg='white', width=10).pack(side=tk.LEFT, padx=10)

    def quit_app(self):
        self.root.quit()
        self.root.destroy()

    def do_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        u = self.user_manager.get_user_by_name(username)
        if u and u.get_password() == password:
            self.current_user = u
            self.login_win.destroy()
            self.root.deiconify()
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_register(self):
        reg_win = tk.Toplevel(self.login_win)
        reg_win.title("Register New User")
        reg_win.geometry("320x250")
        reg_win.grab_set()

        def do_register():
            name = reg_name.get().strip()
            pwd = reg_pwd.get().strip()
            if not name or not pwd:
                messagebox.showerror("Error", "Fields cannot be empty")
                return
            if self.user_manager.get_user_by_name(name):
                messagebox.showerror("Error", "User already exists")
                return
            new_user = user(name, pwd)
            self.user_manager.add_user(new_user)
            save_users(self.user_manager.get_all_users())
            messagebox.showinfo("Success", "Registration successful, please login")
            reg_win.destroy()

        main_frame = tk.Frame(reg_win, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(main_frame, text="Username:", bg='#f0f0f0').grid(row=0, column=0, pady=5)
        reg_name = tk.Entry(main_frame)
        reg_name.grid(row=0, column=1, pady=5)
        tk.Label(main_frame, text="Password:", bg='#f0f0f0').grid(row=1, column=0, pady=5)
        reg_pwd = tk.Entry(main_frame, show="*")
        reg_pwd.grid(row=1, column=1, pady=5)
        tk.Button(main_frame, text="Submit Registration", command=do_register, bg='#ff6600', fg='white').grid(row=2, column=0, columnspan=2, pady=10)

    def create_main_interface(self):
        top_frame = tk.Frame(self.root, bg='#ff6600', height=60)
        top_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Label(top_frame, text=f"Welcome, {self.current_user.get_username()}", font=('Microsoft YaHei', 12),
                 bg='#ff6600', fg='white').pack(side=tk.LEFT, padx=20)
        tk.Button(top_frame, text="Logout", command=self.logout, bg='white', fg='#ff6600').pack(side=tk.RIGHT, padx=20)

        main_pane = tk.Frame(self.root, bg='#f5f5f5')
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.LabelFrame(main_pane, text="📦 Product Library", font=('Microsoft YaHei', 12, 'bold'), bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        cols = ("Name", "Price", "Sales", "Rating", "Action")
        self.tree = ttk.Treeview(left_frame, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        right_frame = tk.Frame(main_pane, bg='#f5f5f5', width=1000)          
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        topk_f = tk.LabelFrame(right_frame, text="🔥 Hot Sellers", bg='white')
        topk_f.pack(fill=tk.X, pady=(0,10))
        self.topk_listbox = tk.Listbox(topk_f, height=15, font=('Microsoft YaHei', 9))  
        self.topk_listbox.pack(fill=tk.BOTH, padx=5, pady=5)

        rec_f = tk.LabelFrame(right_frame, text="🎁 Smart Recommendations", bg='white')
        rec_f.pack(fill=tk.BOTH, expand=True)
        self.rec_listbox = tk.Listbox(rec_f, height=12, font=('Microsoft YaHei', 9))
        self.rec_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Buy", command=self.buy_selected)
        self.context_menu.add_command(label="Rate", command=self.rate_selected)

        self.refresh_all()

    def logout(self):
        self.current_user = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.withdraw()
        self.show_login_register()

    def on_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            name = self.tree.item(item_id, "values")[0]
            self.selected_product = self.product_manager.get_product_by_name(name)
            self.context_menu.post(event.x_root, event.y_root)

    def buy_selected(self):
        if self.selected_product:
            p = self.selected_product
            p.set_sales(p.get_sales() + 1)
            save_products(self.product_manager)
            messagebox.showinfo("Success", f"Purchased {p.get_name()}")
            self.refresh_all()

    def rate_selected(self):
        if not self.selected_product: return
        self.rating_window = tk.Toplevel(self.root)
        self.rating_window.title("Rate")
        tk.Label(self.rating_window, text=f"Rate {self.selected_product.get_name()} (1-5):").pack(pady=10)
        
        # Remove the default perfect score of 5, forcing the user to input manually
        score_var = tk.StringVar(value="")
        tk.Entry(self.rating_window, textvariable=score_var).pack()
        
        def submit():
            try:
                s = int(score_var.get())
                if 1 <= s <= 5:
                    pname = self.selected_product.get_name()
                    self.current_user.set_prefer_item(pname, s)
                    self._update_avg_score(self.selected_product)
                    save_users(self.user_manager.get_all_users())
                    save_products(self.product_manager)
                    self.rating_window.destroy()
                    self.refresh_all()
                else: raise ValueError
            except: messagebox.showerror("Error", "Please enter an integer between 1 and 5")
        
        tk.Button(self.rating_window, text="Submit", command=submit).pack(pady=10)

    def _update_avg_score(self, product):
        all_u = self.user_manager.get_all_users()
        scores = [u.get_score_item()[product.get_name()] for u in all_u if product.get_name() in u.get_score_item()]
        if scores: product.set_score(round(sum(scores)/len(scores), 1))

    def refresh_all(self):
        # 1. Refresh main list
        for item in self.tree.get_children(): self.tree.delete(item)
        for p in self.product_manager.get_product_list():
            self.tree.insert("", "end", values=(p.get_name(), p.get_price(), p.get_sales(), p.get_score(), "⚡ Right-click"))
        
        # 2. Refresh hot sellers ranking
        self.topk_listbox.delete(0, "end")
        calc = calculator(5)
        @dataclass(order=True)
        class HeapItem:
            score: int
            item: Any = field(compare=False)
        for p in self.product_manager.get_product_list():
            if p.get_sales() > 0: calc.insert(HeapItem(p.get_sales(), p))
        for i, res in enumerate(calc.get_KTOP(), 1):
            self.topk_listbox.insert("end", f"{i}. {res.item.get_name()} ({res.score} sold)")

        # 3. Refresh recommendation list (introduce fallback strategy)
        self.rec_listbox.delete(0, "end")
        recs = get_recommendations(self.current_user, self.user_manager, self.product_manager)
        
        if recs:
            for p in recs[:5]: 
                self.rec_listbox.insert("end", f"✨ {p.get_name()} (Rating:{p.get_score()})")
        else:
            self.rec_listbox.insert("end", "⚠️ No similar friends yet")
            self.rec_listbox.insert("end", "💡 Recommending top-rated products for you:")
            
            # Fallback strategy: fetch the highest-rated unpurchased products from the entire platform
            top_rated = sorted(
                [p for p in self.product_manager.get_product_list() if p.get_score() > 0], 
                key=lambda x: x.get_score(), reverse=True
            )
            curr_rated = set(self.current_user.get_score_item().keys()) if self.current_user else set()
            fallback_recs = [p for p in top_rated if p.get_name() not in curr_rated][:5]
            
            if fallback_recs:
                for p in fallback_recs:
                    self.rec_listbox.insert("end", f"🌟 {p.get_name()} (Rating:{p.get_score()})")
            else:
                self.rec_listbox.insert("end", "Explore more in the product library~")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingApp(root)
    root.mainloop()