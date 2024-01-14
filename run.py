import gspread
from google.oauth2.service_account import Credentials

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


def retrieve_records():
    """
    Function to retrieve all records found
    in the models list spreadhseet.
    """
    return contactdetails.get_all_records()


def retrieve_all_contact():
    """
    Function to retrieve full list of models
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    for contact in all_contacts:
        print_record(contact)


def print_record(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")

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