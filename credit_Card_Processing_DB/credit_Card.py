#! /usr/bin/env python
import os
import sys
sys.path.append("Metakit/")
import metakit


# Static list of possible commands
commands = ["add","charge","credit"]

# Database and Database view
db = metakit.storage("CreditCardsDB.mk",1)
vw = db.getas("CreditCard[name:S,cardNumber:S,limit:I,balance:S]")

# Credit Card object that contains the Cardholder's name, Credit Card number, and the limit on the card.
class CreditCard:  
  def __init__(self,name,cardNumber,limit):
    self.name = name
    self.cardNumber = cardNumber
    self.limit = int(limit[1:])
    self.balance = "$0"

# The Add function is used to add a new Credit Card to the list of cards. It works by validating the card number against Luhn 10 and then
# checking the number length that must have a length no greater than 19. Depending on the validation, a card will be added with or without 
# an error.
def Add(newCard):
  if (is_luhn_valid(newCard.cardNumber)):
    if (len(newCard.cardNumber) < 20):
      vw.append(name=newCard.name,cardNumber=newCard.cardNumber,limit=newCard.limit,balance=newCard.balance)
    else:
      newCard.balance = "error"
      vw.append(name=newCard.name,cardNumber=newCard.cardNumber,limit=newCard.limit,balance=newCard.balance)
  else:
    newCard.balance = "error"
    vw.append(name=newCard.name,cardNumber=newCard.cardNumber,limit=newCard.limit,balance=newCard.balance)

# The summary function completes three tasks. The first task is the sorting of the list of values in the Database. The second
# task is the print out the values stored in the Database. The third task is to write these values to a new text file that is 
# created and named incrementally to avoid overwriting previous files.
def summary():
  s = 1 
  fil = 'summaryFiles/summaryFile'+str(s)+'.txt'
  while os.path.isfile(fil):
    s += 1
    fil = 'summaryFiles/summaryFile'+str(s)+'.txt'
  fi = open('summaryFiles/summaryFile'+str(s)+'.txt','w')
  for a in vw.sort(vw.name):
    print a.name + ': ' + str(a.balance)
    fi.write(a.name + ': ' + str(a.balance) + "\n")
  fi.close()

# The Parse Command function takes a string containing Credit Card Processing and passes the information to the 
# Add, Charge, and Credit functions. It contains a lot of different string processing information used for running the 
# functions and creating Credit Card objects.
def parseCommand(input):
  input = input.lower()
  command = input.split(' ',1)[0]
  name = input.split(' ',2)[1]
  if command == "add":
    number = input.split(' ',3)[2]
    limit = input.split(' ',4)[3]
    Add(CreditCard(name,number,limit))
    db.commit()
  elif command == "charge":
    amount = int(input.split(' ',3)[2][1:])
    for i in vw:
      if i.name == name:
        if not(i.balance == "error"):
          x = int(i.balance[1:])
          if not((x + amount) > i.limit):
            x += amount
            i.balance = "$"+str(x)
        db.commit()
  elif command == "credit":
    amount = int(input.split(' ',3)[2][1:])
    for i in vw:
      if i.name == name:
        if not(i.balance == "error"):
          x = int(i.balance[1:])
          x -= amount
          i.balance = "$"+str(x)
        db.commit()

# Luhn 10 (Code taken from Wikipedia for algotithm)
def luhn_checksum(cardNumber):
  def digits_of(n):
    return[int(d) for d in str(n)]
  digits = digits_of(cardNumber)
  odd_digits = digits[-1::-2]
  even_digits = digits[-2::-2]
  checksum = 0
  checksum += sum(odd_digits)
  for d in even_digits:
    checksum += sum(digits_of(d*2))
  return checksum %10

# Luhn 10 validation that returns a boolean value (Code taken from Wikipedia for algotithm)
def is_luhn_valid(cardNumber):
  return luhn_checksum(cardNumber) == 0

# The Command Check function takes in a command from the command line and compares it against the static list of
# commands. This returns a boolean depending on whether the command line value is a valid command.
def commandCheck(input):
  for i in commands:
    if i in input:
      return True
  return False

# This is the location where we enter the program. This parses the command line arguments that can be one of the
# three of add, charge, or debit. A textfile can also be processed here.
sys.argv.pop(0)
if len(sys.argv)+1 == 1:
  pass
elif len(sys.argv) > 1:
  print sys.argv
  print sys.argv[2]
  if sys.argv[0] == 'add':
    parseCommand(sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3])
  elif sys.argv[0] == 'charge':
    parseCommand(sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2])
  elif sys.argv[0] == 'credit':
    parseCommand(sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2])
elif ('.' in str(sys.argv[0])):
  textFile = str(sys.argv[0])
  with open(os.path.expanduser(textFile)) as infile:
    for i in infile:
      parseCommand(i)
      
# This is the second location where we then prompt on the command line for input. This is a while loop that continues
# until the user inputs an exit.
while True:
  userInput = raw_input('Please enter a file with path, credit card information seperated by spaces, or enter exit: ')
  if (' ' in userInput) and (commandCheck(userInput)):
    parseCommand(userInput) 
  elif ('.' in userInput):
    with open(os.path.expanduser(userInput)) as infile:
      for i in infile:
        parseCommand(i)
  elif (userInput == 'exit'):
    break
  elif ('summary' in userInput):
    summary()
  else:
    print 'Try to enter a file path, credit card info, or exit'
    continue

# Run the summary command at the end of the program.
summary()


