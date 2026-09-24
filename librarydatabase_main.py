import math
from collections import deque

# ==========================================================
#  ПРОЄКТ: База даних бібліотеки (ООП)
#  Дисципліна: Алгоритмізація та програмування
#
#  6 класів, у кожного 2-5 методів і 2-7 властивостей.
#  4 структури даних:
#     list  — упорядкований каталог книг (Library.books, Reader.borrowed)
#     dict  — пошук книги за кодом            (Library.catalog)
#     set   — коди виданих книг (унікальність) (Library.borrowed)
#     deque — черга запитів FIFO              (Library.requests)
# ==========================================================

class Book:
    """Книга. Стан змінюється лише через методи borrow / return_book."""

    def __init__(self, code, title, author, genre, status="В наявності"):
        self.code = code
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.holder = None  # хто зараз тримає книгу (об'єкт Reader або None)

    def borrow(self, reader):
        # видати можна лише наявну книгу
        if self.status == "В наявності":
            self.status = "Видано"
            self.holder = reader
            return True
        return False

    def return_book(self):
        # повернути можна лише видану книгу
        if self.status == "Видано":
            self.status = "В наявності"
            self.holder = None
            return True
        return False

    def info(self):
        line = f"[{self.code}] «{self.title}» — {self.author}; {self.genre}; {self.status}"
        if self.holder is not None:
            line += f" (у читача {self.holder.name})"
        return line


class Reader:
    """Читач. Тримає список книг, які має на руках (структура list)."""

    def __init__(self, name, card):
        self.name = name
        self.card = card
        self.borrowed = []  # list

    def take(self, book):
        self.borrowed.append(book)

    def give_back(self, book):
        if book in self.borrowed:
            self.borrowed.remove(book)


class Librarian:
    """Бібліотекар. Працює з бібліотекою (композиція: делегує їй роботу)."""

    def __init__(self, name, position):
        self.name = name
        self.position = position

    def add_book(self, library, title, author, genre):
        return library.add_book(title, author, genre)

    def serve(self, library):
        # обслуговує один запит із черги
        return library.process_request()


class Library:
    """Ядро проєкту. Містить усі 4 структури даних і правила їх зміни."""

    def __init__(self):
        self.books = [  # list — упорядкований каталог
            Book("BK-001", "Кобзар", "Тарас Шевченко", "Поезія"),
            Book("BK-002", "Тіні забутих предків", "Михайло Коцюбинський", "Повість"),
            Book("BK-003", "Місто", "Валер'ян Підмогильний", "Роман"),
            Book("BK-004", "Лісова пісня", "Леся Українка", "Драма"),
            Book("BK-005", "Захар Беркут", "Іван Франко", "Історичний роман"),
            Book("BK-006", "Тигролови", "Іван Багряний", "Пригодницький роман"),
        ]
        self.catalog = {book.code: book for book in self.books}  # dict — код -> книга
        self.borrowed = set()      # set — коди виданих книг
        self.requests = deque()    # deque — черга запитів (FIFO)
        self.next_id = len(self.books) + 1

    def add_book(self, title, author, genre):
        code = f"BK-{self.next_id:03d}"
        self.next_id += 1
        book = Book(code, title, author, genre)
        self.books.append(book)
        self.catalog[code] = book
        return book

    def remove_book(self, code):
        book = self.catalog.pop(code, None)
        if book is not None:
            self.books.remove(book)
            self.borrowed.discard(code)
        return book

    def find_book(self, code):
        return self.catalog.get(code)  # швидкий пошук за ключем O(1)

    def add_request(self, reader, code, action):
        # action: "borrow" або "return"
        self.requests.append((reader, code, action))

    def process_request(self):
        # бере один запит з початку черги й повертає повідомлення про результат
        if not self.requests:
            return "Черга порожня"
        reader, code, action = self.requests.popleft()
        book = self.find_book(code)
        if book is None:
            return f"{reader.name}: книгу {code} не знайдено"
        if action == "borrow":
            if book.borrow(reader):
                self.borrowed.add(code)
                reader.take(book)
                return f"{reader.name} бере «{book.title}» [{code}]"
            return f"{reader.name}: «{book.title}» вже видано читачу {book.holder.name}"
        else:  # return
            if book.return_book():
                self.borrowed.discard(code)
                reader.give_back(book)
                return f"{reader.name} повертає «{book.title}» [{code}]"
            return f"{reader.name}: «{book.title}» не була видана"


class Simulation:
    """Сценарна симуляція процесу: задані дані -> запуск -> передбачуваний вивід."""

    def __init__(self, library, output=True):
        self.library = library
        self.output = output  # True — друкувати кроки в консоль

    def run(self):
        if self.output:
            print("=== СИМУЛЯЦІЯ РОБОТИ БІБЛІОТЕКИ ===")
        librarian = Librarian("Марія", "бібліотекар")
        anna = Reader("Анна", "R-01")
        ihor = Reader("Ігор", "R-02")

        # ставимо запити в чергу (обробляться в порядку надходження)
        self.library.add_request(anna, "BK-001", "borrow")
        self.library.add_request(ihor, "BK-001", "borrow")   # спроба видати вже видану книгу -> відмова
        self.library.add_request(ihor, "BK-003", "return")   # спроба повернути ще не видану книгу -> відмова
        self.library.add_request(ihor, "BK-003", "borrow")
        self.library.add_request(anna, "BK-001", "return")
        self.library.add_request(ihor, "BK-001", "borrow")   # тепер знову доступна

        while self.library.requests:
            message = librarian.serve(self.library)
            if self.output:
                print(message)

        self.report()

    def report(self):
        print("--- Підсумок ---")
        print(f"Зараз видано книг: {len(self.library.borrowed)}")
        print(f"Усього в каталозі: {len(self.library.books)}")


class Menu:
    """Інтерактивне консольне меню (окремий клас: відповідає лише за інтерфейс)."""

    def __init__(self, library, bpp=5):
        self.library = library
        self.bpp = bpp  # книг на сторінці
        self.current_page = 1

    def main_menu(self):
        while True:
            print("\n=== БІБЛІОТЕКА ===")
            print("[1] Переглянути каталог")
            print("[2] Додати книгу")
            print("[3] Редагувати книгу")
            print("[4] Видалити книгу")
            print("[exit] Вихід")
            choice = input("Ваш вибір: ").strip().lower()
            if choice == "1":
                self.show_page()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.edit_book()
            elif choice == "4":
                self.remove_book()
            elif choice == "exit":
                break
            else:
                print("Некоректний ввід. Спробуйте ще раз.")

    def show_page(self):
        books = self.library.books
        if not books:
            print("Каталог порожній.")
            return
        total_pages = math.ceil(len(books) / self.bpp)
        if self.current_page > total_pages:
            self.current_page = 1
        while True:
            print(f"\nСторінка {self.current_page}/{total_pages}")
            start = (self.current_page - 1) * self.bpp
            for i in range(start, min(start + self.bpp, len(books))):
                print(books[i].info())
            action = input("Номер сторінки або будь-що інше для виходу: ").strip()
            try:
                new_page = int(action)
                if 1 <= new_page <= total_pages:
                    self.current_page = new_page
                else:
                    print("Такої сторінки немає.")
            except ValueError:
                return

    def add_book(self):
        title = input("Назва: ").strip()
        author = input("Автор: ").strip()
        genre = input("Жанр: ").strip()
        book = self.library.add_book(title, author, genre)
        print(f"Додано: {book.info()}")

    def edit_book(self):
        if not self.library.books:
            print("Каталог порожній.")
            return
        code = input("Код книги для редагування (напр. BK-003), Enter — вихід: ").strip().upper()
        if not code:
            return
        if code.isdigit():
            code = f"BK-{int(code):03d}"
        book = self.library.find_book(code)
        if book is None:
            print("Книгу з таким кодом не знайдено.")
            return
        new_title = input(f"Нова назва (Enter — лишити «{book.title}»): ").strip()
        if new_title:
            book.title = new_title
        new_author = input(f"Новий автор (Enter — лишити «{book.author}»): ").strip()
        if new_author:
            book.author = new_author
        new_genre = input(f"Новий жанр (Enter — лишити «{book.genre}»): ").strip()
        if new_genre:
            book.genre = new_genre
        print(f"Оновлено: {book.info()}")

    def remove_book(self):
        if not self.library.books:
            print("Каталог порожній.")
            return
        code = input("Код книги для видалення (напр. BK-003 чи 3), Enter — вихід: ").strip().upper()
        if not code:
            return
        if code.isdigit():
            code = f"BK-{int(code):03d}"
        book = self.library.find_book(code)
        if book is None:
            print("Книгу з таким кодом не знайдено.")
            return
        self.library.remove_book(book.code)
        print(f"Видалено: [{book.code}] «{book.title}»")


if __name__ == "__main__":
    print("=== ПРОЄКТ «БІБЛІОТЕКА» ===")
    print("[1] Запустити симуляцію процесу")
    print("[2] Відкрити інтерактивну бібліотеку")
    print("[exit] Вихід")
    while True:
        start_choice = input("Ваш вибір: ").strip().lower()
        if start_choice == "1":
            Simulation(Library()).run()
        elif start_choice == "2":
            Menu(Library()).main_menu()
        elif start_choice == "exit":
            break
        else:
            print("Некоректний ввід. Спробуйте ще раз.")
