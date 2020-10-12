import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysql',
    database='books'
)


#queries
createDB= "CREATE DATABASE books"
showDatabses = "SHOW DATABASES"
create_table = "CREATE TABLE book_details (book_name varchar(250), author_name varchar(250))"
show_tables = "SHOW TABLES"
insert_into_databas = "INSERT INTO book_details (book_name, author_name) VALUES (%s, %s)"
get_all_books = "SELECT * FROM book_details"
searchByBookName = "SELECT * FROM book_details where book_name='%s'"
searchByAuthorName = "SELECT * FROM book_details where author_name='%s'"
updateByBookName = "UPDATE book_details SET book_name ='bookName', author_name='authorName' WHERE book_name='bookName'"
updateByAuhorName = "UPDATE book_details SET book_name ='%s', author_name='%s' WHERE book_name='%s' and author_name='%s'"
delete_by_book_name = "DELETE FROM book_details WHERE book_name='%s'"
delete_by_book_author_name = "DELETE FROM book_details WHERE book_name='%s' and author_name='%s'"

cursor = mydb.cursor(buffered=True)

#creating cursor
cursor = mydb.cursor(buffered=True)

#cursor.executemany(insert_into_databas, book_to_add)
#mydb.commit()

def ShowAllBooks():
    # function 1
    cursor.execute(get_all_books)
    all_books = cursor.fetchall()
    for row in all_books:
        print(row)

# now implementing insertion query
def checkIfBookExistsWithSameAuthor(book_name, author_name):
    querry = "select * from book_details where book_name='%s' and author_name='%s'"
    cursor.execute(querry% (book_name, author_name), mydb)
    if cursor.rowcount > 0:
        return True
    else:
        return False

def checkIfBookDoesntExist(book_name):
    querry = "select * from book_details where book_name='%s'"
    cursor.execute(querry % book_name, mydb)
    if cursor.rowcount > 0:
        return True
    else:
        return False

def checkIfAuthorExist(author_name):
    querry = "select * from book_details where author_name='%s'"
    cursor.execute(querry % author_name, mydb)
    if cursor.rowcount > 0:
        return True
    else:
        return False


def insertBook():
    # function 2
    print("\n***************\tInsert Book Information\t***************")
    bookName = input("\tEnter Book Name!!!\t")
    authorName = input("\tEnter Author of Book!!!\t")
    if checkIfBookExistsWithSameAuthor(bookName, authorName):
        print(f"Book already Exists with author: {authorName} and book {bookName}")
    else:
        book_to_add = [
            (bookName, authorName),
        ]
        cursor.executemany(insert_into_databas, book_to_add)
        mydb.commit()

def searchBookbyBookName():
    # function 3
    print("\n***************\tSearch Book by Book name\t***************")
    bookName = input("\n\tEnter Book Name to find details!!!\t")
    if checkIfBookDoesntExist(bookName) == False:
        print("No record found!!")
    else:
        cursor.execute(searchByBookName % bookName, mydb)
        all_books = cursor.fetchall()
        for row in all_books:
            book_name , author_name = row
            print("\n\tBook name: ", book_name)
            print("\tAuthor name: ", author_name)

def allBooksOfAuthor():
    # function 4
    print("\n***************\tSearch Books by Author name\t***************")
    authorName = input("\n\tEnter Author's Name whos books u wanna find out!!!\t")
    if checkIfAuthorExist(authorName) == 0:
        print("Author Not Found")
    else:
        cursor.execute(searchByAuthorName % authorName, mydb)
        all_books = cursor.fetchall()
        for row in all_books:
            book_name , author_name = row
            print("\n\tBook name: ", book_name)


def updateBooksbyName():
    # function 5
    print("\n\t\tupdate")
    bookName = input("\tEnter Book Name whos author u wanna change!!!\t")
    if checkIfBookDoesntExist(bookName) == 0:
        print("No record found!!")
    else:
        authorName = input("Enter Author Name!!!\t")
        query = updateByBookName.replace ("bookName",str(bookName)).replace("authorName",str(authorName))
        cursor.execute(query,mydb)
        mydb.commit()
        print("Updated Records are as follows. ")

def updateBooksByAuthorName():
    # function 6
    authorName = input("Enter author name, whos book u want to update!\t")
    if checkIfAuthorExist(authorName) == False:
        print("\nAuthor Not FOund\n")
    else:
        bookName = input("Enter Book name to update\t")
        if checkIfBookExistsWithSameAuthor(bookName, authorName) == False:
            print(f"Book Doesn't Exist with author: {authorName} and book {bookName}")
        else:
            newBookname = input("\tENter name for book\t")
            newAuthorName = input("\tENter name for author\t")
            query = updateByAuhorName % (str(newBookname), str(newAuthorName), str(bookName), str(authorName))
            print(query)
            cursor.execute(query,mydb)
            print(cursor.rowcount)
            mydb.commit()
            print("Updated Records are as follows. ")


def deleteBookByBookName():
    # function 7
    bookName = input("ENter book name u want to delete!")
    if checkIfBookDoesntExist(bookName)== False:
        print(f"No record found by {bookName}")
    else:
        cursor.execute(delete_by_book_name%bookName, mydb)
        mydb.commit()

def deleteAuthorsBook():
    #function 8
    authorName = input("Enter author name, whos book u want to update!\t")
    if checkIfAuthorExist(authorName) == False:
        print("\nAuthor Not FOund\n")
    else:
        bookName = input("Enter Book name to Delete\t")
        if checkIfBookExistsWithSameAuthor(bookName, authorName) == False:
          print(f"Book Doesn't Exist with author: {authorName} and book {bookName}")
        else:
            cursor.execute(delete_by_book_author_name % (bookName, authorName), mydb)
            mydb.commit()

#          *************** Main function ****************
def Home():
    print("\n***************\tBooks----Store\t***************")
    while(True):
        choice = int(input('''
            \n\t1. Show All Books
            \n\t2. Insert Book
            \n\t3. Search Book by name
            \n\t4. Update Book by book name
            \n\t5. Delete Book by book name
            \n\t6. Search All Books of some Author
            \n\t7. Update Authors books
            \n\t8. Delete Authors Book
            \n\t0. Quit\n
        '''))
        if choice == 1:
            ShowAllBooks()
        elif choice == 2:
            insertBook()
            ShowAllBooks()
        elif choice == 3:
            searchBookbyBookName()
        elif choice == 4:
            ShowAllBooks()
            updateBooksbyName()
            ShowAllBooks()
        elif choice == 5:
            ShowAllBooks()
            deleteBookByBookName()
            ShowAllBooks()
        elif choice == 6:
            allBooksOfAuthor()
        elif choice == 7:
            ShowAllBooks()
            updateBooksByAuthorName()
            ShowAllBooks()
        elif choice == 8:
            ShowAllBooks()
            deleteAuthorsBook()
            ShowAllBooks()
        elif choice == 0:
            break
        else:
            print("Insert numeric value 0-8")
            Home()

Home()