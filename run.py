import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Contact-book')

contactdetails = SHEET.worksheet('contactdetails')

def user_response(message, min_value, max_value):
    """
    Function used throughout the programme
    to validate users input from a list of choices.
    """
    input = pyip.inputInt(prompt=message, min=min_value, max=max_value)
    return input

def retrieve_records():
    """
    Function to retrieve all records found
    in the models list spreadhseet.
    """
    return contactdetails.get_all_records()


def retrieve_all_contact():
    """
    Function to retrieve full list of contact
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    for contact in all_contacts:
        print_record(contact)
    another_task()


def print_record(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")


def another_task():
    """
    Function to prompt users for another task.
    Returns True if the user wants to go back to the main menu,
    and False if the program should shut down.
    """
    print("\nWould you like to complete another task?\n")
    print("1. Yes, back to main menu\n2. No, end program")

    while True:
        user_input = user_response("\nPlease enter a number from the above options: ", 1, 2)

        if user_input == 1:
            print("\nNow taking you back to the main menu...\n")
            menu()
            return True
        else:
            print("Program shutting down...\n")
            raise SystemExit


def get_valid_input(prompt, validation_function):
    """
    Helper function to get valid input based on the provided validation function.
    """
    while True:
        user_input = pyip.inputStr(prompt)
        if validation_function(user_input):
            break
        else:
            print("Enter valid input.")

    return user_input

def add_new_contact():
    """
    Function to allow users to enter a new model's information.
    If the user tries to enter invalid characters, they will be alerted.
    """
    name = get_valid_input('*First Name: ', str.isalpha)

    print("Please enter your number")
    number = pyip.inputInt('*Mobile Number: ')

    email = get_valid_input('*Email: ', pyip.inputEmail)

    address = get_valid_input('*Address: ', lambda x: len(x) > 0)  
    
    age = pyip.inputInt('*Age: ')

    new_contact_info = [name, number, email, address, age]

    print(f'The data you have entered is: <{new_contact_info}>')

    print("\nWould you like to save?\n")
    save = pyip.inputMenu(['Yes', 'No'], numbered=True)

    if save == 'Yes':
        contactdetails.append_row(new_contact_info)
        print("\nWorksheet updated successfully")
    else:
        print("Worksheet not updated")

    return another_task()



def show_menu():
    """
    Function to display menu items to user.
    This function is called from the menu function.
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
    User selects which task they would like to do, uses their input and runs
    elif loop to trigger the next process.
    If an invalid choice is input then the programme
    will alert user and ask for another choice.
    """
    while True:
        show_menu()
        choice = input('Please enter a choice from the above numbers: ')
        if choice == '1':
            retrieve_all_contact()
        elif choice == '2':
            add_new_contact()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            edit_contact()
        else:
            print(f'Not a valid choice: <{choice}>,try again')


if __name__ == '__main__':
    menu()

