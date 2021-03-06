import requests
from bs4 import BeautifulSoup

import string
import random

## characters to generate password from



def gen_random_password():
	characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
	length = 8

	## shuffling the characters
	random.shuffle(characters)

	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return "".join(password)


def gen_email(first_name, last_name):
	if last_name == "NULL":
		email = first_name.lower() + '@shiremail.com'

	else:
		first_name = first_name.split()
		# first_name[0]

		if len(first_name[0]) > 5:
			first_name_short = first_name[0][:5]
		else:
			first_name_short = first_name[0]

		email = first_name_short.lower() + '.' + last_name.lower() + '@shiremail.com'

	return email

def scrape_character(character):
	dick_char = {}

	url = "https://lotr.fandom.com/wiki/" + character
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")

	# %%
	name = soup.find("h1")
	name = name.text
	name = name.replace('\n', '')
	name = name.replace('\t', '')

	name_split = name.split()
	if len(name_split) > 1:
		last_name = name_split[-1]
		name_split = name_split[:-1]
		first_name = ' '.join(name_split)
	else:
		first_name = name
		last_name = 'NULL'

	dick_char["first_name"] = first_name
	dick_char["last_name"] = last_name

	print('name ', first_name, last_name)
	# %%
	img = soup.find(class_="pi-image-thumbnail")
	img_src = img["src"]
	print(img_src)
	dick_char["img_src"] = img_src

	# %%
	# dob = soup.find(data-source="birth")
	dob = soup.select('div[data-source="birth"]')
	if dob == []:
		dick_char["dob"] = 'NULL'
	else:
		# print(dob)
		print(dob[0].div.text)
		dick_char["dob"] = dob[0].div.text

	race = soup.select('div[data-source="race"]')
	if race == []:
		dick_char["race"] = 'NULL'
	else:
		race[0].div.text
		dick_char["race"] = race[0].div.text

	email = gen_email(first_name, last_name)
	dick_char['email'] = email

	dick_char['pass'] = gen_random_password()
	dick_char['user'] = first_name.lower().split()[0];

	return dick_char


def gen_parenthesis(entry):
	if entry != 'NULL':
		entry = "\'" + entry + "\'"

	return entry


def convert_dict(profile_dict):
	dict_parenthesis = {}
	for key, value in profile_dict.items():
		dict_parenthesis[key] = gen_parenthesis(value)

	return dict_parenthesis


def gen_sql(profile_dict):
	sql_string = "insert into user_profile (user, email, pass, name, last_name, race, dob) value (" + profile_dict["user"] \
	             + ", " + profile_dict["email"] + ", " + profile_dict["pass"] + ", " + profile_dict["first_name"] + ", " \
	             + profile_dict["last_name"] + ", " + profile_dict["race"] + ", " + profile_dict["dob"] + ");\n"
	return sql_string


def character_to_query(character):
	scraped_dict = scrape_character(character)
	scraped_dict_p = convert_dict(scraped_dict)

	sql_query = gen_sql(scraped_dict_p)

	return sql_query


def queries_to_file(character_list):
	f = open('2_insert_characters.sql', 'w')

	for ch in character_list:
		query = character_to_query(ch)
		f.write(query)

	f.close()


# characters = ["Gollum", "Aragorn_II_Elessar", "Sauron", "Gandalf", "Bilbo_Baggins", "Frodo_Baggins"]
#
# queries_to_file(characters)

def read_characters_file(filename):
	f = open(filename, 'r')

	lines = f.readlines()
	print("Length: ", len(lines))

	list_characters = []
	for l in lines:
	    list_characters.append(l[:-1])

	return list_characters

#
# d = scrape_character("Gollum")
# print(d)
#
# d = scrape_character("Aragorn_II_Elessar")
# print(d)
