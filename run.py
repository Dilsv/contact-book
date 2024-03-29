import gspread
from google.oauth2.service_account import Credentials
import re

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Contact-book')
contacts = SHEET.worksheet('contacts')


def user_response(message, min_value, max_value):
    """
    A function employed across the program to
    authenticate user input from a predefined
    list of options.
    """
    while True:
        try:
            user_input = int(input(message))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print("Invalid input. Enter a valid number.")
        except ValueError:
            print("Invalid input. Enter a valid number.")


def retrieve_records():
    """
    Function designed to gather all contacts from
    the spreadsheet containing contact details.
    """
    return contacts.get_all_records()


def retrieve_all_contacts():
    """
    Function to retrieve the full list of contacts.
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    for contact in all_contacts:
        print_record(contact)
    another_task()


def print_record(record):
    """
    A function that iterates through all records
    provided as a parameter, printing their
    details in a key-value list format.
    """
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")


def another_task():
    """
    A function designed to ask users for another task,
    returning True if the user wishes to return to the
    main menu, and False if the program should be shut down.
    """
    print("\nWould you like to complete another task?\n")
    print("1. Yes, back to the main menu\n2. No, end program")

    user_input = user_response("\nPlease enter a number from the above options: ", 1, 2)

    if user_input == 1:
        print("\nNow taking you back to the main menu...\n")
        menu()
    else:
        print("Program shutting down...\n")
        os.exit()


def add_new_contact():
    """
    Function enabling users to input new contact information,
    with the provision to alert them if invalid characters 
    are attempted.
    """
    print("Please enter the following information for the new contact:")
    first_name = input('*First Name: ')
    number = user_response('*Mobile Number: ', 11, float('inf'))
    country = input('*Country: ')
    age = user_response('*Age: ', 0, float('inf'))

    new_contact_info = [first_name, number, country, age]

    print(f'The data you have entered is: {new_contact_info}')

    print("\nWould you like to save?\n")
    save = user_response("1. Yes\n2. No\n", 1, 2)

    if save == 1:
        contacts.append_row(new_contact_info)
        print("\nWorksheet updated successfully")
    else:
        print("Worksheet not updated")

    another_task()


def search_display(choice, search_by):
    """
    Function that exhibits search results, invoked within
    the search function and utilized in the edit_search
    function.
    """
    header = contacts.row_values(1)
    index = header.index(choice) + 1

    column = contacts.col_values(index)
    rows_ids = []
    rows_data = []

    for i in range(len(column)):
        if column[i] == search_by:
            row_number = i + 1
            rows_ids.append(row_number)

    if len(rows_ids) > 0:
        print("Number of Contacts found: ", len(rows_ids))
        for row_number in rows_ids:
            row = contacts.row_values(row_number)
            rows_data.append(row)
            print(row_number, row)
    else:
        print("\nNo Contacts found")
        another_task()

    return rows_ids


def search(choice):
    """
    Function to show search choices to user.
    """
    search_by = input(f'\nEnter {choice}: ').capitalize()
    print("\nLoading Contacts...\n")
    rows_ids = search_display(choice, search_by)
    return rows_ids


def search_contacts():
    """
    Permits users to search for specific contacts based
    on criteria such as first name, mobile number, country,
    or age. The search function is subsequently invoked to
    present the results to the user.
    """
    print("\nHow would you like to search?\n\
    \n1. By First Name\n\
    2. By Mobile Number\n\
    3. By Country\n\
    4. By Age\n")

    user_input = user_response(
        "\nPlease enter a number from the above options: ", 1, 4
    )

    if user_input == 1:
        search('First Name')
    elif user_input == 2:
        search('Mobile Number')
    elif user_input == 3:
        search('Country')
    elif user_input == 4:
        search('Age')

    another_task()


def get_updated_value(user_input):
    """
    Helper function to get the updated value based on user input.
    """
    if user_input == 1:
        return input('\n*New First Name: ')
    elif user_input == 2:
        return user_response('\n*New Mobile Number: ', 11, float('inf'))
    elif user_input == 3:
        return input('\n*New Country: ')
    elif user_input == 4:
        return user_response('\n*New Age: ', 0, float('inf'))
    else:
        return None  # Handle other cases if necessary


def edit_search():
    """
    Function to allow the user to search contacts by First Name.
    """
    print("\nHow would you like to search?\n\
    \n1. By First Name\n")

    user_input = user_response("\nPlease enter a number from the above options: ", 1, 1)

    if user_input == 1:
        name_to_search = input("\nEnter the First Name to search: ")
        rows_ids = search_by_name(name_to_search)

    while True:
        contact_row = user_response('\nPlease enter the number that is \
            next to the contact you would like to select: ', 0, float('inf'))

        if contact_row in rows_ids:
            break

    print("\
        \n1. First Name\n\
    2. Mobile Number\n\
    3. Country\n\
    4. Age\n")

    user_input = user_response("\nWhich value would you like to change: ", 1, 4)
    updated_value = get_updated_value(user_input)

    updated_contact_info = contacts.row_values(contact_row)
    index = user_input - 1
    updated_contact_info[index] = updated_value

    print(f'The updated contact will be: {updated_contact_info}')
    print("\nWould you like to save?\n")
    save = user_response("1. Yes\n2. No\n", 1, 2)

    if save == 1:
        update_contact(contact_row, user_input, updated_value)
        print("\nWorksheet updated successfully")
    else:
        print("\nWorksheet not updated")

    another_task()


def search_by_name(first_name):
    """
    Helper function to search for contacts by First Name.
    """
    header = contacts.row_values(1)
    index = header.index("First Name") + 1

    column = contacts.col_values(index)
    rows_ids = []

    for i in range(len(column)):
        if column[i] == first_name:
            row_number = i + 1
            rows_ids.append(row_number)

    if len(rows_ids) > 0:
        print("Number of Contacts found: ", len(rows_ids))
        for row_number in rows_ids:
            row = contacts.row_values(row_number)
            print(row_number, row)
    else:
        print("\nNo Contacts found")
        another_task()

    return rows_ids


def update_contact(contact_row, contact_column, updated_value):
    """
    Function responsible for updating the Google Spreadsheet
    when a user modifies individual contact information.
    """
    contacts.update_cell(contact_row, contact_column, updated_value)


def show_menu():
    """
    Function designed to present menu items to the user,
    and it is invoked from the menu function.
    """
    print("\nWelcome to your Contact Book!\n")
    print("Main menu")
    print("-----------------")
    print("1) See all Contacts")
    print("2) Add new Contact")
    print("3) Search Contact")
    print("4) Edit Contact\n")


def menu():
    """
    The user chooses a task, and their input is utilised to
    initiate the next process through an "elif" loop.
    If an invalid choice is entered, the program will notify 
    the user and prompt them for an alternative selection.
    """
    while True:
        show_menu()
        choice = input('Please enter a choice from the above numbers: ')
        if choice == '1':
            retrieve_all_contacts()
        elif choice == '2':
            add_new_contact()
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            edit_search()
        else:
            print(f'Not a valid choice: {choice}, try again')


if __name__ == '__main__':
    menu()