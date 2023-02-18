# ******************************TASK 39 CAPSTONE*******************************
"""
Writen in Python (3.10.0) within Visual Studio Code (VSC).

VSC extension SQLite used in developing this programme but noot nessailry a 
requirement. The extension retrives and will display databases and tables
in the SQLITE Explorer output window.

The current programme is configured for a Database named "ebookstore_db.db".
and includes a table called "books".

If the database does not exist, the program will create it and save it in the 
same directory as the program file. A confirmation message will be displayed 
indicating the successful creation of the database.

Requirements
- Sqlite3 module
- Pandas module 
"""
# *************************BOOKSTORE DATABASE MANAGER**************************

# Import Modules
import sqlite3
import os
import pandas as pd

# Create Bookstore Database

db_file = "eBookstore_db.db"

    # Check Database exists.
if not os.path.isfile(db_file):
    print("Database created!")
    db = sqlite3.connect(db_file)
    db.commit()
else:
    db = sqlite3.connect(db_file)

    # Create cursor object to execute any SQL commends required.
cursor = db.cursor()

# Create Database Table, set classes.
table_name = "books"

cursor.execute(f"SELECT name FROM sqlite_master WHERE type" + 
               f" ='table' AND name = ?", (table_name,))
result = cursor.fetchone()
if not result:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, 
                                         title TEXT, 
                                         author TEXT, 
                                         qty INTEGER)""")
    print(f"Table {table_name} created")
    db.commit()

# *************************DEFINE PROGRAMME FUNCTIONS**************************

def line_divider():
    """
    Function to print solid line (unicode character) in terminal.
    """
    print("")
    print('\u2501' * 79)


def user_return():
    """
    Function to pause user returning to main menu
    This is so they can spend longer looking at search returns.
    """
    while True:
        user_return = input("Enter 'Y' to return to main menu : ").lower()

        if user_return == 'y':
            return
        else: 
            continue


def call_table_ids(cursor, table_name):

    cursor.execute(f"SELECT id FROM {table_name}")
    existing_id_values = [row[0] for row in cursor.fetchall()]
    #print(f"The following IDs are assigned : \n{existing_id_values}\n")

    return existing_id_values


def add_record(cursor, table_name):
    """
    Add book record to books table.
    """
    # Call call_table_ids function
    existing_id_values = call_table_ids(cursor,table_name)

    # Check id primary key is unique.
    while True:
        try:
            i_d = input(("\nPlease enter the new ID of" + 
                         " the book or 'r' to return : "))

            #Allow use to escape.
            if i_d == 'r':
                line_divider()
                return

            # Cast to interger and catch ValueErrors
            try:
                i_d = int(i_d)
            except ValueError:
                print("ERROR - Not a valid interger, try again.")
                continue     

            # Check new ID not duplicate of existing.
            if i_d not in existing_id_values:
                break
            else:
                raise ValueError

        except ValueError as exception :
            print("ERROR - Duplicate ID number" + 
                  ", enter a unique ID number.")

    # User to input remaining feature value entries.
    title  = str(input("\nEnter the title of this book entry : ")).lower()
    author = str(input("\nEnter the author of this book entry : ")).lower()


        # Input qty, cast to interger and catch ValueErrors
    while True:
        try:
            qty = input("\nEnter the numerical value of the books in stock : ")
            qty = int(qty)
            break
        except ValueError:
            print("ERROR - Not a valid interger, try again.")
            continue 

    # Insert new book entry record into given table. 
    cursor.execute(f"INSERT INTO {table_name}(id, title, author, qty)" 
                   f" VALUES(?,?,?,?)",
                   (i_d, title, author, qty))

    # Confirmatory check
    print("\nNew entry added!")
    line_divider()
    db.commit()


def view_table(table_name):
    """
    Function to search through named table books.
    """
    print("\n\x1B[4mSearch Options\x1B[0m\n")
    # Unicode to underline menu headings.
    print("\x1B[4mCodes\x1B[0m\t \x1B[4mOptions\x1B[0m")
    # Unicode and formatting to display menu keys and descriptions.
    print("""             
    0 \t\b\b\b\u2502\t View all,
    1 \t\b\b\b\u2502\t Search by Book ID,
    2 \t\b\b\b\u2502\t Search by Book Title,
    3 \t\b\b\b\u2502\t Search by Book Author,
    4 \t\b\b\b\u2502\t Search by Book Quanties (equal to or below),
    5 \t\b\b\b\u2502\t Search by Book Quanties (equal to or above),
    r \t\b\b\b\u2502\t Return to Main Menu""")
    
    # Enact Search
    while True:

        # Take user search option
        user_option = input("\nPlease Enter Menu Option Code : ").lower()
        line_divider()      

        # Code to handle menu codes only.
        if user_option in ["0","1","2","3","4","5","r"]:

            if user_option == "0":
                # No search criterion,
                break
            elif user_option == "1":
                # Search by ID,
                search_element =  int(input(("\nPlease enter ID of the" + 
                                             " book you'd like to search : ")))
                search_option = "id"
                symbol = "="
                break
            elif user_option == "2":
                # Search by Title,
                search_element= str(input(("\nPlease enter Title of book" + 
                                           " you'd like to search : "))).lower()
                search_option = "title"
                symbol = "="
                break
            elif user_option == "3":
                # Search by Author,
                search_element = str(input(("\nPlease enter Author of book" + 
                                            " you'd like to search : "))).lower()
                search_option = "author"
                symbol = "="
                break
            elif user_option == "4":
                # Search by qty equal to or below,
                search_element = int(input(("\nPlease enter Book Qty equal or"+
                                            " below you'd like to search : ")))
                search_option = "qty"
                symbol = "<="
                break
            elif user_option == "5":
                # Search by qty equal to or above,
                search_element = int(input(("\nPlease enter Book Qty equal or"+ 
                                            " above you'd like to search : ")))
                search_option = "qty"
                symbol = ">="
                break
            else: 
                # No search criterion,
                user_option == "r"
                break
        else:
            # Handle non-valid menu codes.
            print("Invalid option, enter code from menu else 'r' to return.")
            continue

    # Formulate SQL Queries.
    # All Table records.
    if user_option == "0":
        cursor.execute(f" SELECT * FROM {table_name}")
    # Select Table records matching search criterion.
    elif user_option in ["1","2","3","4","5"]:
        cursor.execute(f" SELECT * FROM {table_name}" +
                       f" WHERE {search_option} {symbol} ? ", (search_element,))
    # Break function.
    elif user_option == "r":
        return

    # Based on SQL Query, fetch records.
    records = cursor.fetchall()

    # Create empty SQL Query data list.
    search_return_data = []

    # For each row in SQL Query return.
    for row in records:
        # Append to data list
        search_return_data.append(row)

    # Check list contains elements to proceed
    if len(search_return_data) != 0:

        # Turn data list into dataframe.
        search_return_df = pd.DataFrame(search_return_data, columns = ["ID",
                                                                    "Title",
                                                                    "Author", 
                                                                    "Qty"])
        search_return_df.set_index("ID", inplace = True)

        # Print dataframe.
        print("\n\x1B[4mSearch Returns\x1B[0m\n")
        print(f"{search_return_df}\n")
        user_return()
        line_divider()

    else:
        print("\nNo Records found matching your search criteria.\n")
        user_return()
        line_divider()


def update_record(cursor, table_name):
    """
    Function to update book records in table_name.
    """
    # try to select record to update by entering ID.
    while True:
        try:
            id_select = input(("\nPlease select the ID of the book you" + 
                               " would like to edit or 'r' to return: "))

            # 'r' to allow user to escape.
            if id_select == "r":
                line_divider()
                return

            # Now cast to interger.
            id_select = int(id_select)

            # Call call_table_ids function
            existing_id_values = call_table_ids(cursor,table_name)
            if id_select in existing_id_values:
                break
            else:
                print("Book Record ID entered does not exist")
                continue
        # Raise Value Error for non valid inputs.
        except ValueError:
            print("ERROR - You have entered an invalid input, try again.")
            continue

    # For valid Record ID,enter feature label to update.
    edit_choice = input(("\nWhat aspect would you like edit" +
                         " (id. title. author, qty) : ")).lower()

    # Update book ID else return.
    if edit_choice == "id" : 

        # While loop to handle ValueErrors
        while True:
            try:
                new_value = input(("\nPlease enter the new ID of" + 
                                    " the book or 'r' to return : "))
                #Allow use to escape.
                if new_value == 'r':
                    line_divider()
                    return

                # Cast to interger and catch ValueErrors
                try:
                    new_value = int(new_value)
                except ValueError:
                    print("ERROR - Not a valid interger, try again.")
                    continue                    

                # Check new ID not duplicate of existing.
                if new_value not in existing_id_values:
                    break
                else:
                    raise ValueError

            except ValueError as exception :
                print("ERROR - Duplicate ID number" + 
                      ", enter a unique ID number.")

        search_option = "id"

    # Update book Title    
    elif edit_choice == "title" : 
        new_value = str(input(("\nPlease enter the new title of the" +
                               " book or 'r' to escape : "))).lower()
        search_option = "title"

    # Update book author
    elif edit_choice == "author" :
        new_value = str(input(("\nPlease enter the new author of the" +
                               " book or 'r' to escape : "))).lower()
        search_option = "author"

    # Update book qty
    elif edit_choice == "qty" :

        while True:        
            new_value = input(("\nPlease enter the new qty of the" +
                               " book or 'r' to escape : "))
            
            # Cast to interger and catch ValueErrors
            #Allow use to escape.
            if new_value == 'r':
                line_divider()
                break

            # Cast to interger and catch ValueErrors
            try:
                new_value = int(new_value)
                break
            except ValueError:
                print("ERROR - Not a valid interger, try again.")
                continue 

        search_option = "qty"

    #Allow use to escape.
    if new_value == 'r':
        line_divider()
        return

    # SQL Query update record
    cursor.execute(f"UPDATE {table_name} SET {search_option} = '{new_value}'" +
                   f" WHERE id = {id_select}")

    # Confirmatory check
    print("\nEntry Updated!")
    line_divider()
    db.commit()


def delete_record(cursor, table_name):
    """
    Function to delete book records from table_name
    """  
    while True:
        try:
            id_select = input(("\nPlease select ID of the book you would" + 
                            " like to delete or 'r' to return : "))

            #Allow use to escape.
            if id_select == 'r':
                line_divider()
                return

            # Cast to interger and catch ValueErrors
            try:
                id_select = int(id_select)
            except ValueError:
                print("ERROR - Not a valid interger, try again.")
                continue                    
                        
            # Check ID exists.
            existing_id_values = call_table_ids(cursor,table_name)
            if id_select in existing_id_values:
                break

            else:
                raise ValueError

        except ValueError as exception :
            print("ERROR - ID record does not exist, try again")    

    # SQL Query delete record
    cursor.execute(f"DELETE FROM {table_name} WHERE id = {id_select}")

    # Confirmatory check
    print("\nEntry Removed!")
    line_divider()
    db.commit()


def db_manager_menu():
    """
    Function to call database manager menu.
    """
    # Database Management Menu Options
    print("\x1B[\n4meBookstore Database Manager Menu\x1B[0m \n")
        # Unicode to underline menu headings.
    print("\x1B[4mCodes\x1B[0m\t \x1B[4mOptions\x1B[0m")
        # Unicode and formatting to display menu keys and descriptions.
    print("""             
    0 \t\b\b\b\u2502\t Enter New Book Record,
    1 \t\b\b\b\u2502\t View or Search Book Records,
    2 \t\b\b\b\u2502\t Update Book Record,
    3 \t\b\b\b\u2502\t Delete Book Record,
    e \t\b\b\b\u2502\t Exit Programme.""")


# ********************************DRIVER CODE**********************************

# Initiate Programme
line_divider()
print("\nWelcome to eBookstore Database Manager. ")
print("Version 1.00 (01/01/2023)")
line_divider()

# Describe Database
print(f"\nCurrent Database File Name \t: {db_file}")
print(f"Current Database Table Name \t: {table_name}")
line_divider()

# Run Menu Options
menu_switch = 1

while True : 
    
    # Database Management Menu Options
    if menu_switch == 1 :
        db_manager_menu()
        menu_switch = 1
    
    # Take user search option
    menu_option = input("\nPlease Enter Menu Option Code : ").lower()
    

    # Code to handle menu codes only.
    if menu_option in ["0","1","2","3","e",]:
        
        # Run Add_Record Function.
        if menu_option == "0":
            line_divider()
            add_record(cursor, table_name)
            menu_switch = 1
            continue
            
        # Run View_Table Function.
        elif menu_option == "1":
            line_divider()
            view_table(table_name)
            menu_switch = 1
            continue
        
        # Run Update_Table Function.
        elif menu_option == "2":
            line_divider()
            update_record(cursor, table_name)
            menu_switch = 1
            continue
        
        # Run Delete_Record Function.
        elif menu_option == "3":
            line_divider()
            delete_record(cursor, table_name)
            menu_switch = 1
            continue
        
        # Exit Programme.
        elif menu_option == "e":
            line_divider()
            print("\nClosing eBookstore Database Manager - Goodbye!")
            menu_switch = 1
            line_divider()
            break
        
    else:
        # Handle non-valid menu codes.
        menu_switch = 0
        print("\nInvalid menu option, please try again")
        line_divider()
        continue    
    
# ************************************END**************************************