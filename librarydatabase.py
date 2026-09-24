import math

class Person:
    class Employee:
        def __init__(self, name, age, title, database):
            self.name = name
            self.age = age
            self.title = title
            self.database = database

    class Customer:
        def __init__(self, name, age, preference, time, database):
            self.name = name
            self.age = age
            self.preference = preference
            self.time = time
            self.database = database

        def simulate(self):
            pass

# ці 3 класи зверху ще не додані та не мають ніякого застосунку

class Book:
    def __init__(self, name, author, page_count, genre, status):
        self.name = name
        self.author = author
        self.page_count = page_count
        self.genre = genre
        self.status = status

class Simulation:
    def __init__(self, database, clients, employees, output):
        self.database = database
        self.clients = clients
        self.employees = employees
        self.output = output # показує симуляцію в консолі True/False

    def simulate(self):
        if self.database.status == True:
            pass

# клас simulation теж ще не має застосунку

class Database:
    def __init__(self, bpp, current_page, status):
        self.books : list[Book] = [Book("PLACEHOLDER_1", "AUTH_PLACEHOLDER_1", 255, "HORROR", "In stock"),
                                    Book("PLACEHOLDER_2", "AUTH_PLACEHOLDER_2", 255, "HORROR", "In stock"),
                                    Book("PLACEHOLDER_3", "AUTH_PLACEHOLDER_3", 255, "ADVENTURE", "In stock"),
                                    Book("PLACEHOLDER_4", "AUTH_PLACEHOLDER_4", 255, "ADVENTURE", "In stock"),
                                    Book("PLACEHOLDER_5", "AUTH_PLACEHOLDER_5", 255, "SCI-FI", "In stock"),
                                    Book("PLACEHOLDER_6", "AUTH_PLACEHOLDER_6", 255, "SCI-FI", "In stock"),
                                    Book("PLACEHOLDER_7", "AUTH_PLACEHOLDER_7", 255, "FANTASY", "In stock"),
                                    Book("PLACEHOLDER_8", "AUTH_PLACEHOLDER_8", 255, "FANTASY", "In stock"),
                                    Book("PLACEHOLDER_9", "AUTH_PLACEHOLDER_9", 255, "NOVEL", "In stock"),
                                    Book("PLACEHOLDER_10", "AUTH_PLACEHOLDER_10", 255, "NOVEL", "In stock")]
        self.bpp = bpp # (books per page) скільки книг буде показано на одній сторінці датабази
        self.current_page = current_page
        self.status = status # позначає чи відкрита бібліотека. включає симуляцію якщо True. True/False

    def add_book(self):
        print("")
        new_name = input("Enter new book's name: ")
        new_author = input("Enter new book's author: ")
        new_page = input("Enter new book's page count: ")
        new_genre = input("Select a book's genre: ")
        self.books.append(Book(new_name, new_author, new_page, new_genre, "In stock"))
        self.main_menu(4)

    def remove_book(self):
        print("")
        book_number = input("Please input book's index or type anything else to exit.")
        try:
            num = int(book_number)
            if len(self.books) != 0:
                if num >= 0 and num < len(self.books):
                    self.books.pop(num)
                    self.main_menu(0)
                else:
                    self.main_menu(2)
            else:
                self.main_menu(3)
        except ValueError:
            self.main_menu(2)

    def edit_book (self):
        print("")
        edited_book : Book = Book("","","","","")
        edited_book_ind = input("Input an index of book to edit, input anything else to exit: ")
        try:
            num = int(edited_book_ind)
            if num >= 0 and num < len(self.books):
                edited_book = self.books[num]
                if edited_book.status != "In stock":
                    self.main_menu(5)
            else:
                self.main_menu(2)
        except ValueError:
            self.main_menu(0)

        action1 = input("Edit book's name? (y/n): ")
        if action1 == "y":
            edited_book.name = input("Input book's new name: ")
        if action1 != "y" and action1 != "n": print("Invalid input. Defaulted to 'n'.")

        action2 = input("Edit book's author? (y/n): ")
        if action2 == "y":
            edited_book.author = input("Input book's new author: ")
        if action2 != "y" and action2 != "n": print("Invalid input. Defaulted to 'n'.")

        action3 = input("Edit book's genre? (y/n): ")
        if action3 == "y":
            edited_book.genre = input("Input book's new genre: ")
        if action3 != "y" and action3 != "n": print("Invalid input. Defaulted to 'n'.")

        action4 = input("Edit book's page count? (y/n): ")
        if action4 == "y":
            edited_book.page_count = input("Input book's page count: ")
        if action4 != "y" and action4 != "n": print("Invalid input. Defaulted to 'n'.")

        self.main_menu(6)

    def show_page(self, page, retry):
        print("")
        print("Input a number to select a page, input anything else to exit.")
        print("Pages: " + str(page) + "/" + str(math.ceil(len(self.books) / self.bpp)))
        print("")
        book_range_min = page * self.bpp - self.bpp
        i = 0
        while i < self.bpp:
            num = book_range_min + i
            if num < len(self.books):
                print(f"{num}. Name: ''{self.books[num].name}''; Author: {self.books[num].author}; Page count: |{self.books[num].page_count}|; Genre: [{self.books[num].genre}]; Status: [{self.books[num].status}]")
            else:
                print(f"{num}. -")
            i+=1

        if retry is True:
            print("Invalid number input. Please enter a valid page.")
        new_action = input()

        try:
            new_page = int(new_action)
            if new_page > 0 and new_page <= math.ceil(len(self.books) / self.bpp):
                self.show_page(int(new_action), False)
            else:
                self.show_page(page, True)

        except ValueError:
            self.main_menu(0)

    def simulate(self):
        pass

    def main_menu(self, message):
        print("Welcome to our library.")
        print("========================")
        print("Available actions:")
        print("[1] Browse database")
        print("[2] Add book")
        print("[3] Edit book")
        print("[4] Remove book")
        print("[Exit]")

        if message == 1:
            print("Invalid input. Please enter a valid action.")
        if message == 2:
            print("Invalid book index. Please enter a valid index next time.")
        if message == 3:
            print("Database is empty, unable to remove books. Please add a book first.")
        if message == 4:
            print("Your book has been added to the database.")
        if message == 5:
            print("Book that you want to edit is currently not in stock.")
        if message == 6:
            print("Selected book has been edited.")
        new_action = input("Enter your choice: ")
        if new_action == "1":
            self.show_page(self.current_page, False)
        elif new_action == "2":
            self.add_book()
        elif new_action == "3":
            self.edit_book()
        elif new_action == "4":
            self.remove_book()
        elif new_action.lower() == "exit":
            quit()
        else:
            self.main_menu(1)

if __name__ == "__main__":
    app = Database(10, 1, True)
    app.main_menu(0)