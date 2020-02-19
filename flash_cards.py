#import a bunch of stuff for sql
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from cockroachdb.sqlalchemy import run_transaction

#set these to some of the imports so they can be called
DBSession = sessionmaker()
Base = declarative_base()

#import random to create random numbers
import random

#describe the table data structure
class words(Base):
    __tablename__ = 'words'
    english = Column(String, primary_key=True)
    spanish = Column(String)
    french = Column(String)

secure_cluster = False           # Set to False for insecure clusters
connect_args = {}

#create an empty list to store the words in late
wordList = []

#set a global score variable
score = 0

#set the connect args. If local just disable ssl
if secure_cluster:
    connect_args = {
        'sslmode': 'require',
        'sslrootcert': 'certs/ca.crt',
        'sslkey': 'certs/client.maxroach.key',
        'sslcert': 'certs/client.maxroach.crt'
    }
else:
    connect_args = {'sslmode': 'disable'}

#set the db we are connecting to
engine = create_engine(
    'cockroachdb://root@localhost:26257/flash_cards',
    connect_args=connect_args,
    echo=True                   # Log SQL queries to stdout
)

conn = engine.connect()

#grab the data from db. Read each row into a dictionary then append each dictionary to a list. 
def queryTheDB(session):
	s = select([words])
	result = conn.execute(s)
	for row in result:
		oneRow = {'english':row['english'],'spanish':row['spanish'],'french':row['french']}
		wordList.append(oneRow)

#format the questions and check if the user's input matches the correct answer
def vocabularyTest(languageChoice):
	
	#choose a random dictionary from the list 
	localDictionary = wordList[random.randint(0,len(wordList)-1)]

	#ask the user what the English word is for the given Spanish or French word
	testQuestion = input("What is the English word for " + localDictionary[languageChoice] + "\n")

	#make the global score variable available locally
	global score

	#check if the user's answer is correct and increment the score if they got it. Give them the option to quit here
	if testQuestion == localDictionary['english']:
		score = score + 1
		print("Correct! Score:", score)
		vocabularyTest(languageChoice)
	elif testQuestion == "quit":
		exit()
	else:
		print("Incorrect. The correct answer was:",localDictionary['english'])
		vocabularyTest(languageChoice)

#ask the user what language they would like to test
def main():

	#load the words from the db
	run_transaction(sessionmaker(bind=engine), queryTheDB)

	languageChoice = input("Would you like to test your knowledge of French or Spanish vocabulary?")
	vocabularyTest(languageChoice)

#start the program
if __name__ == '__main__':
    main()

