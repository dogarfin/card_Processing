#! /usr/bin/env python
import os
import sys
from array import array

# Arraylist of Credit Card objects
creditCards = []
# Static list of commands
commands = ["add","charge","credit","summary"]

# Credit Card object that contains the the Charge and Credit functions. Object is used to be added to the 
# arraylists.
class CreditCard:  
  def __init__(self,name,cardNumber,limit,error):
    self.name = name
    self.cardNumber = cardNumber
    self.limit = int(limit[1:])
    self.error = error
    self.balance = 0
  # The charge function checks for an error and the current balance to make sure the added amount doesn't go
  # over the limit. If the balance passes, the charge is added to the balance.
  def Charge(self,amount):
    if not(self.error):
      if not((self.balance + amount) > self.limit):
        self.balance += amount
  # The credit function checks for an error. If the balance passes, the credit is removed from the balance.
  def Credit(self,amount):
    if not(self.error):
      self.balance -= amount

# The summary function completes the two functions of printing the sorted objects to stout and writing the 
# sorted objects to a new textfile.
def summary():
  s = 1 
  fil = 'summaryFiles/summaryFile'+str(s)+'.txt'
  while os.path.isfile(fil):
    s += 1
    fil = 'summaryFiles/summaryFile'+str(s)+'.txt'
  fi = open('summaryFiles/summaryFile'+str(s)+'.txt','w')
  creditCards.sort(key=lambda x:x.name)
  for a in creditCards:
    if a.error:
      print a.name + ': ' + 'error'
      fi.write(a.name + ': ' + 'error' + "\n")
    else:
      print a.name + ': $' + str(int(round(a.balance)))
      fi.write(a.name + ': $' + str(int(round(a.balance))) + "\n")
  fi.close()

 # The Add function is used to add a new Credit Card to the list of cards. It works by validating the card number against Luhn 10 and then
# checking the number length that must have a length no greater than 19. Depending on the validation, a card will be added with or without 
# an error.
def Add(newCard):
  if (is_luhn_valid(newCard.cardNumber)):
    if (len(newCard.cardNumber) < 20):
      creditCards.append(newCard)
    else:
      newCard.error = True
      creditCards.append(newCard)
  else:
    newCard.error = True
    creditCards.append(newCard)

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
    error = False 
    Add(CreditCard(name,number,limit,error))
  elif command == "charge":
    amount = input.split(' ',3)[2]
    for i in creditCards:
      if i.name == name:
        i.Charge(int(amount[1:]))
  elif command == "credit":
    amount = input.split(' ',3)[2]
    for i in creditCards:
      if i.name == name:
        i.Credit(int(amount[1:]))

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
# three of Add, Charge, or Credit. A textfile can also be processed here.
sys.argv.pop(0)
if len(sys.argv)+1 == 1:
  pass
elif len(sys.argv) > 1:
  parseCommand(sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3])
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
  elif (commandCheck(userInput)):
    summary()
  else:
    print 'Try to enter a file path, credit card info, or exit'
    continue

# Run the summary command at the end of the program.
summary()

