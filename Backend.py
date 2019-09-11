import re
def checkfirstname(firstname):
	if re.match(r"^[A-Za-z]", firstname):
		pass
	else:
		return "First name is in wrong format."

def checklastname(lastname):
	if re.match(r"^[A-Za-z]", lastname):
		pass
	else:
		return "Last name is in wrong format."

def checkusername(username):
	if re.match(r"[a-zA-Z0-9_.]", username):
		pass
	if len(username) <= 15:
		pass
	else:
		return "Invalid username. Please enter username less than 15 characters long with alphanumeric characters, underscore, or period."
def checkpassword(password):
	if re.match(r"^[ A-Za-z0-9_@./#&+-]*$", password) and len(password) >= 8:
		pass
	else:
		return "Invalid password. Please enter a password longer than 8 characters."
def checkcapacity(capacity):
	if re.match(r"^[0-9]{1,4}$", capacity):
		pass
	else:
		return "Invalid capacity. Please enter an integer."

def checkeventcount(capacity):
	if re.match(r"^[0-9]{1,4}$", capacity):
		pass
	else:
		return "Invalid event count. Please enter an integer."

def checkstaffcount(capacity):
	if re.match(r"^[0-9]{1,4}$", capacity):
		pass
	else:
		return "Invalid staff count. Please enter an integer."

def checkeventname(eventname):
	if re.match(r"^[a-zA-Z0-9 ]*", eventname):
		pass
	else:
		return "Invalid Event Name. Please enter a valid Event Name."

def checkvisit(visit):
	if re.match(r"^[0-9]{1,3}$", visit):
		pass
	else:
		return "Invalid visit. Please enter an integer."

def checkrevenue(revenue):
	if re.match(r"^[0-9]{1,4}$", revenue):
		pass
	else:
		return "Invalid revenue. Please enter an integer."

def checkduration(duration):
	if re.match(r"^[0-9]{1,4}$", duration):
		pass
	else:
		return "Invalid duration. Please enter an integer."

def checkconfirm(password, confpassword):
	if confpassword == password:
		pass
	else:
		return "Password and confirm password do not match."

def checkroute(route):
	if re.match(r"[a-zA-Z0-9]", route):
		pass
	else:
		return "Invalid route. Please enter a valid route."

def checkphone(phone):
	if re.match(r"^[0-9]{10}$", phone):
		pass
	else:
		return "Invalid phone number. Please enter a 10 digit phone number."

def checkkeyword(keyword):
	if re.match(r"^[A-Za-z]", keyword):
		pass
	else:
		return "Invalid keyword. Please enter a valid word."

def checkaddress(address):
	if re.match(r"\d+\s[a-zA-Z0-9_ ]*", address):
		pass
	else:
		return "Invalid address. Please enter proper address format."

def checksiteaddress(address):
	print(address)
	if address == None or re.match(r"\d+\s[a-zA-Z0-9_ ]*", address):
		pass
	else:
		return "Invalid address. Please enter proper address format."
def checkcity(city):
	if re.match(r"^[A-Za-z]", city):
		pass
	else:
		return "Invalid city. Please enter a valid city."

def checkzip(zipcode):
	if re.match(r"^[0-9]{5}$", zipcode):
		pass
	else:
		return "Invalid zipcode. Please enter a 5 digit zipcode."

def checkemail(email):
	if re.match(r"[^@]+@[^@]+\.[^@]+", email):
		pass
	else:
		return "Invalid email. Please enter an email in the following format: EmailAdress@ServiceProivder.domain"

def checkpriceFilter(price):
	if re.match(r"^(\d{1,5}|\d{0,5}\.\d{1,2})$", price) or price == '':
		pass
	else:
		return "Invalid price. Please enter price in the following format: ####.##"

def checkpriceInsert(price):
	if re.match(r"^(\d{1,5}|\d{0,5}\.\d{1,2})$", price):
		pass
	else:
		return "Invalid price. Please enter price in the following format: ####.##"

def checkdateInsert(date):
	if re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", date):
		pass
	else:
		return "Invalid date. Please enter date in the following format: yyyy-mm-dd"

def checkdateFilter(date):
	if re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", date) or date == '':
		pass
	else:
		return "Invalid date. Please enter date in the following format: yyyy-mm-dd"
