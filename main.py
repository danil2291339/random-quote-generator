import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime


# ==================== МОДЕЛЬ ДАННЫХ ====================
class QuoteModel:
    def __init__(self):
        self.quotes = self.load_quotes()
        self.history = self.load_history()

    def load_quotes(self):
        """Загрузка цитат из JSON"""
        default_quotes = [
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди",
             "theme": "Мотивация"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон",
             "theme": "Жизнь"},
            {"text": "Не суди о каждом дне по собранному урожаю, а по посеянным семенам.",
             "author": "Роберт Льюис Стивенсон", "theme": "Мудрость"},
            {"text": "Тот, кто двигает горы, начинает с маленьких камней.", "author": "Конфуций", "theme": "Мотивация"},
            {"text": "Сложнее всего начать действовать, остальное зависит от упорства.", "author": "Амелия Эрхарт",
             "theme": "Успех"},
            {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "theme": "Наука"},
            {"text": "Только тот, кто рискует идти далеко, может узнать, как далеко можно зайти.",
             "author": "Т.С. Элиот", "theme": "Смелость"},
            {
                "text": "Счастье не в том, чтобы делать всегда, что хочешь, а в том, чтобы всегда хотеть того, что делаешь.",
                "author": "Лев Толстой", "theme": "Счастье"},
        ]

        if os.path.exists("quotes.json"):
            try:
                with open("quotes.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return default_quotes
        else:
            self.save_quotes(default_quotes)
            return default_quotes

    def save_quotes(self, quotes=None):
        """Сохранение цитат в JSON"""
        if quotes is None:
            quotes = self.quotes
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []  # ВАЖНО: всегда возвращаем список, даже если файла нет

    def save_history(self):
        """Сохранение истории в JSON"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_random_quote(self):
        """Получение случайной цитаты"""
        return random.choice(self.quotes)

    def add_to_history(self, quote):
        """Добавление цитаты в историю"""
        entry = {
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(entry)
        self.save_history()

    def add_quote(self, text, author, theme):
        """Добавление новой цитаты"""
        if not text.strip() or not author.strip() or not theme.strip():
            return False, "Все поля должны быть заполнены!"

        new_quote = {
            "text": text.strip(),
            "author": author.strip(),
            "theme": theme.strip()
        }
        self.quotes.append(new_quote)
        self.save_quotes()
        return True, "Цитата успешно добавлена!"

    def get_authors(self):
        """Получить список уникальных авторов"""
        return sorted(list(set(q["author"] for q in self.quotes)))

    def get_themes(self):
        """Получить список уникальных тем"""
        return sorted(list(set(q["theme"] for q in self.quotes)))


# ==================== ПРЕДСТАВЛЕНИЕ (VIEW) ====================
class QuoteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Стили
        style = ttk.Style()
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ===== Фрейм отображения цитаты =====
        quote_frame = ttk.LabelFrame(main_frame, text="🎲 Случайная цитата", padding="10")
        quote_frame.pack(fill=tk.X, pady=(0, 10))

        self.quote_text_var = tk.StringVar(value="Нажмите кнопку, чтобы получить цитату")
        self.quote_label = ttk.Label(quote_frame, textvariable=self.quote_text_var,
                                     wraplength=700, font=("Arial", 12, "italic"), justify="center")
        self.quote_label.pack(fill=tk.X, pady=5)

        self.author_var = tk.StringVar()
        self.author_label = ttk.Label(quote_frame, textvariable=self.author_var,
                                      font=("Arial", 10), foreground="gray")
        self.author_label.pack(fill=tk.X, pady=2)

        self.theme_var = tk.StringVar()
        self.theme_label = ttk.Label(quote_frame, textvariable=self.theme_var,
                                     font=("Arial", 9), foreground="blue")
        self.theme_label.pack(fill=tk.X)

        # Кнопка генерации
        self.generate_btn = ttk.Button(quote_frame, text="✨ Сгенерировать цитату",
                                       command=self.controller.generate_quote)
        self.generate_btn.pack(pady=10)

        # ===== Фрейм фильтрации =====
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 Фильтрация истории", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        filter_row = ttk.Frame(filter_frame)
        filter_row.pack(fill=tk.X)

        ttk.Label(filter_row, text="Фильтр по автору:").pack(side=tk.LEFT, padx=(0, 5))
        self.author_filter_var = tk.StringVar()
        self.author_combo = ttk.Combobox(filter_row, textvariable=self.author_filter_var, width=20)
        self.author_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.author_combo.bind("<<ComboboxSelected>>", lambda e: self.controller.apply_filters())

        ttk.Label(filter_row, text="Фильтр по теме:").pack(side=tk.LEFT, padx=(0, 5))
        self.theme_filter_var = tk.StringVar()
        self.theme_combo = ttk.Combobox(filter_row, textvariable=self.theme_filter_var, width=20)
        self.theme_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.theme_combo.bind("<<ComboboxSelected>>", lambda e: self.controller.apply_filters())

        self.clear_filters_btn = ttk.Button(filter_row, text="Сбросить фильтры",
                                            command=self.controller.clear_filters)
        self.clear_filters_btn.pack(side=tk.LEFT)

        # ===== Фрейм истории =====
        history_frame = ttk.LabelFrame(main_frame, text="📜 История цитат", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)

        # Создание Treeview для истории
        columns = ("timestamp", "text", "author", "theme")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        self.history_tree.heading("timestamp", text="Дата/время")
        self.history_tree.heading("text", text="Цитата")
        self.history_tree.heading("author", text="Автор")
        self.history_tree.heading("theme", text="Тема")

        self.history_tree.column("timestamp", width=140)
        self.history_tree.column("text", width=400)
        self.history_tree.column("author", width=120)
        self.history_tree.column("theme", width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ===== Фрейм добавления цитаты =====
        add_frame = ttk.LabelFrame(main_frame, text="➕ Добавить новую цитату", padding="10")
        add_frame.pack(fill=tk.X, pady=(10, 0))

        add_row1 = ttk.Frame(add_frame)
        add_row1.pack(fill=tk.X, pady=2)
        ttk.Label(add_row1, text="Текст:").pack(side=tk.LEFT, padx=(0, 5))
        self.new_text_entry = ttk.Entry(add_row1, width=60)
        self.new_text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        add_row2 = ttk.Frame(add_frame)
        add_row2.pack(fill=tk.X, pady=2)
        ttk.Label(add_row2, text="Автор:").pack(side=tk.LEFT, padx=(0, 5))
        self.new_author_entry = ttk.Entry(add_row2, width=30)
        self.new_author_entry.pack(side=tk.LEFT, padx=(0, 15))
        ttk.Label(add_row2, text="Тема:").pack(side=tk.LEFT, padx=(0, 5))
        self.new_theme_entry = ttk.Entry(add_row2, width=20)
        self.new_theme_entry.pack(side=tk.LEFT)

        self.add_quote_btn = ttk.Button(add_frame, text="💾 Сохранить цитату",
                                        command=self.controller.add_quote)
        self.add_quote_btn.pack(pady=5)

    def display_quote(self, quote):
        """Отображение текущей цитаты"""
        self.quote_text_var.set(f"❝ {quote['text']} ❞")
        self.author_var.set(f"— {quote['author']}")
        self.theme_var.set(f"📌 Тема: {quote['theme']}")

    def update_history_display(self, history_items):
        """Обновление отображения истории"""
        # Очистка Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Добавление записей
        for entry in history_items:
            self.history_tree.insert("", tk.END, values=(
                entry.get("timestamp", ""),
                entry.get("text", ""),
                entry.get("author", ""),
                entry.get("theme", "")
            ))

    def update_filters(self, authors, themes):
        """Обновление списков фильтров"""
        self.author_combo['values'] = ["Все"] + authors
        self.theme_combo['values'] = ["Все"] + themes

    def get_filter_values(self):
        """Получение значений фильтров"""
        author = self.author_filter_var.get()
        theme = self.theme_filter_var.get()
        return author, theme

    def clear_filter_entries(self):
        """Очистка полей фильтров"""
        self.author_filter_var.set("")
        self.theme_filter_var.set("")

    def clear_add_entries(self):
        """Очистка полей добавления"""
        self.new_text_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_theme_entry.delete(0, tk.END)

    def show_message(self, title, message, is_error=False):
        """Показать сообщение пользователю"""
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


# ==================== КОНТРОЛЛЕР ====================
class QuoteController:
    def __init__(self, root):
        self.model = QuoteModel()
        self.view = QuoteView(root, self)

        # Текущая отображаемая цитата
        self.current_quote = None

        # Обновление фильтров
        self.update_filters()

        # Отображение истории
        self.apply_filters()

    def update_filters(self):
        """Обновление списков фильтров в представлении"""
        authors = self.model.get_authors()
        themes = self.model.get_themes()
        self.view.update_filters(authors, themes)

    def generate_quote(self):
        """Генерация случайной цитаты"""
        quote = self.model.get_random_quote()
        self.current_quote = quote
        self.view.display_quote(quote)
        self.model.add_to_history(quote)
        self.apply_filters()

    def add_quote(self):
        """Добавление новой цитаты"""
        text = self.view.new_text_entry.get()
        author = self.view.new_author_entry.get()
        theme = self.view.new_theme_entry.get()

        success, message = self.model.add_quote(text, author, theme)

        if success:
            self.view.show_message("Успех", message)
            self.view.clear_add_entries()
            self.update_filters()
            self.apply_filters()
        else:
            self.view.show_message("Ошибка", message, is_error=True)

    def apply_filters(self):
        """Применение фильтров к истории"""
        author_filter, theme_filter = self.view.get_filter_values()

        filtered_history = []

        # Проверка, что history существует и является списком
        if self.model.history and isinstance(self.model.history, list):
            for entry in self.model.history:
                # Применение фильтров
                if author_filter and author_filter != "Все":
                    if entry.get("author") != author_filter:
                        continue
                if theme_filter and theme_filter != "Все":
                    if entry.get("theme") != theme_filter:
                        continue
                filtered_history.append(entry)

        self.view.update_history_display(filtered_history)

    def clear_filters(self):
        """Сброс фильтров"""
        self.view.clear_filter_entries()
        self.apply_filters()


# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteController(root)
    root.mainloop()