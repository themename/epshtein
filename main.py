import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x500")

        # 1. Список предопределённых цитат
        self.quotes = [
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "theme": "Знания"},
            {"text": "Успех — это идти от ошибки к ошибке, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
        ]
        
        self.history = []
        self.file_path = os.path.join(os.path.expanduser("~"), "Desktop", "history.json")
        
        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        # Секция отображения цитаты
        self.quote_label = tk.Label(self.root, text="Нажмите кнопку, чтобы получить цитату", 
                                    wraplength=500, font=("Arial", 12, "italic"))
        self.quote_label.pack(pady=20)

        # 2. Кнопка генерации
        self.gen_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.gen_btn.pack(pady=5)

        # 4. Фильтрация
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр (Автор/Тема):").grid(row=0, column=0)
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.grid(row=0, column=1, padx=5)
        
        self.filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=2)

        # 3. История (Список)
        tk.Label(self.root, text="История цитат:").pack()
        self.history_listbox = tk.Listbox(self.root, width=80, height=10)
        self.history_listbox.pack(pady=5, padx=10)
        
        self.update_history_display()

    def generate_quote(self):
        # Выбор случайной цитаты
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
        
        # Добавление в историю
        self.history.append(quote)
        self.save_history()
        self.update_history_display()

    # 5. Работа с JSON
    def save_history(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def update_history_display(self, items=None):
        self.history_listbox.delete(0, tk.END)
        display_items = items if items is not None else self.history
        for q in reversed(display_items):
            self.history_listbox.insert(tk.END, f"[{q['theme']}] {q['author']}: {q['text']}")

    # 4. Логика фильтрации
    def apply_filter(self):
        query = self.filter_entry.get().lower().strip()
        if not query:
            self.update_history_display()
            return
        
        filtered = [q for q in self.history if query in q['author'].lower() or query in q['theme'].lower()]
        self.update_history_display(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
