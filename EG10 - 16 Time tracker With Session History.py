# EG10 - 14 Time tracker With Session History

from BTCInput import *
import pickle
import time

class Session:
    __min_session_length = 0.5
    __max_session_length = 3.5
    
    @staticmethod
    def validate_session_length(session_length):
        if session_length < Session.__min_session_length:
            return False
        if session_length > Session.__max_session_length:
            return False
        return True
    
    def __init__(self, session_length):
        if not Session.validate_session_length(session_length):
            raise Exception('Invalid Exception.')
        self.__session_length = session_length
        self.__session_end_time = time.localtime()
        self.__version = 1
        
    @property
    def session_length(self):
        return self.__session_length
    
    @property
    def session_end_time(self):
        return self.__session_end_time
    
    def check_version(self):
        pass
    
    def __str__(self):
        template = 'Date: {0} Length: {1}'
        date_string = time.asctime(self.__session_end_time)
        return template.format(date_string, self.__session_length)
        
class Contact:
    __open_fee = 30
    __hourly_fee = 50
    
    __min_text_length = 4
    
    @staticmethod
    def validate_text(text):
        if len(text) < Contact.__min_text_length:
            return False
        else:
            return True
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if not Contact.validate_text(name):
            raise Exception('Invalid Name.')
        self.__name = name
        return
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address):
        if not Contact.validate_text(address):
            raise Exception('Invalid address.')
        self.__address = address
        return
    
    @property
    def telephone(self):
        return self.__telephone
    
    @telephone.setter
    def telephone(self, telephone):
        if not Contact.validate_text(telephone):
            raise Exception('Invalid Telephone.')
        self.__telephone = telephone
        return
    
    @property
    def hours_worked(self):
        return self.__hours_worked
    
    @property
    def billing_amount(self):
        return self.__billing_amount
    
    def __init__(self, name, address, telephone):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.__hours_worked = 0
        self.__billing_amount = 0
        self.__sessions = []
        self.__version = 1
        
    @property
    def session_report(self):
        #  Convert the list of sessions into a list of strings
        report_strings = map(str, self.__sessions)
        # Convert the list of strings into one string
        # separated by newline characters
        result = '\n'.join(report_strings)
        return result
        
    def __str__(self):
        template = '''Name: {0}
Address: {1}
Telephone: {2}
Hours on the case: {3}
Amount to bill: {4}
Sessions
{5}'''
        return template.format(self.name, self.address, self.telephone, self.hours_worked,
                               self.billing_amount, self.session_report)
        
    
    def check_version(self):
        if self.__version == 1:
            self.__billing_amount = 0
            slef.__version = 2
        
        if self.__version == 2:
            self.__sessions = []
            self.__version = 3
            
        for session in self.__sessions:
            session.check_version()
    
    def add_session(self,session_length):
        if not Session.validate_session_length(session_length):
            raise Exception('Invalid Session Length.')
        self.__hours_worked = self.__hours_worked + session_length
        amount_to_bill = Contact.__open_fee + (Contact.__hourly_fee * session_length)
        self.__billing_amount = self.__billing_amount + amount_to_bill
        session_record = Session(session_length)
        self.__sessions.append(session_record)
        
        
def new_contact():
    print('New contact')
    name = read_text('Enter the contact name: ')
    address = read_text('Enter the contact address: ')
    telephone = read_text('Enter the contact telephone: ')
    try:
        new_contact = Contact(name = name, address = address, telephone = telephone)
        contacts.append(new_contact)
    except Exception as e:
        print('Invalid Text:',e)
    
def find_contact(search_name):
    search_name = search_name.strip()
    search_name = search_name.lower()
    for contact in contacts:
        name = contact.name
        name = name.strip()
        name = name.lower()
        if name.startswith(search_name):
            return contact
    return None

def display_contact():
    print('Find contact')
    search_name = read_text('Enter the contact name: ')
    contact = find_contact(search_name)
    if contact != None:
        print(contact)
    else:
        print('This name was not found.')
        
def edit_contact():
    print('Edit contact')
    search_name = read_text('Enter the contact name: ')
    contact = find_contact(search_name)
    if contact != None:
        print('Name:',contact.name)
        new_name = read_text('Enter new name or . to leave unchanged: ')
        if new_name != '.':
            contact.name = new_name
        new_address = read_text('Enter new address or . to leave unchanged: ')
        if new_address != '.':
            contact.address = new_address
        new_telephone = read_text('Enter new telephone or . to leave unchanged: ')
        if new_telephone != '.':
            contact.telephone = new_telephone
    else:
        print('This name was not found')
        
def add_session_to_contact():
    print('Add Session')
    search_name = read_text('Enter the contact name: ')
    contact = find_contact(search_name)
    if contact != None:
        print('Name:',contact.name)
        print('Previous Hours Worked:',contact.hours_worked)
        session_length = read_float('Session Length: ')
        try:
            contact.add_session(session_length)
            print('Updated Hours Worked:',contact.hours_worked)
            print('Amount To Bill:',contact.billing_amount)
        except Exception as e:
            print('Add failed:',e)
    else:
        print('This name was not found.')
    
def save_contacts(file_name):
    print('Save contacts.')
    try:
        with open(file_name, 'wb') as output_file:
            pickle.dump(contacts ,output_file)
    except:
        print('Contacts not saved.')
        
def load_contacts(file_name):
    global contacts
    print('Load contacts.')
    with open(file_name,'rb') as input_file:
        contacts = pickle.load(input_file)
    for contact in contacts:
        contact.check_version()
        

menu = '''
1. New Contact
2. Find Contact
3. Edit Contact
4. Add Session
5 .Exit Program

    Enter a command: '''
filename = 'new_contacts.pickle'
try:
    load_contacts(filename)
except:
    print('Contacts file not found.')
    contacts = []
    
while True:
    command = read_int_ranged(prompt = menu, min_value = 1, max_value = 5)
    if command == 1:
        new_contact()
    elif command == 2:
        display_contact()
    elif command == 3:
        edit_contact()
    elif command == 4:
        add_session_to_contact()
    elif command == 5:
        save_contacts(filename)
        break