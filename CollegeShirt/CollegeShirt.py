# Created by Robert Brodin, 2020. Simple email script!

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
import time

# Used for ease of changing the email that is being sent to the colleges. Reads a text file (txtFile) and returns a list of strings from the desired email to be sent text file.
def getEmailToSend(txtFile, name):
    lineList = ""
    fileToRead = open(txtFile, "r")
    filedata = fileToRead.read()
    fileToRead.close()

    filedata = filedata.replace("Dear NAME,", "Dear" + " " + name + ",")

    f = open(txtFile, 'w')
    f.write(filedata)
    f.close()

    fileToRead = open(txtFile, "r")
    for line in fileToRead:
        lineList = lineList + line

    fileToRead.close()
    filedata = filedata.replace("Dear" + " " + name + ",", "Dear NAME,")
    f = open(txtFile, 'w')
    f.write(filedata)
    f.close()

    return lineList

# Used to get a list of the college email addresses. Reads a text file (txtFile) and returns a list of strings of email addresses.
def getEmailAddresses(txtFile):
    emailList = []
    fileToRead = open(txtFile, "r")
    for email in fileToRead:
        # Creating a new variable to hold the email address, up until the dash. As well as the name!
        # When hitDash is set to true, stop appending to that variable and switch to a different variable.
        # I could have done this more efficiently but alas, it works and for this script that is what matters.
        emailAddress = ""
        name = ""
        hitDash = False
        for char in email:
            if(char == "-"):
                hitDash = True
            elif not hitDash:
                emailAddress+=char
            else:
                name+=char
        emailList.append(emailAddress)
        emailList.append(name)
    fileToRead.close()
    return emailList

# Used to send an email. Takes argument toAddr (email address to send email to), body (the content of the email). Function is void.
def sendEmail(fromAddr, password, toAddr, body, name, title):
    msg = MIMEMultipart()
    msg['From'] = name + " <" + fromAddr + ">"
    msg['To'] = toAddr
    msg['Subject'] = title # can make more specific, just testing for now.

    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddr, password)
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()

# TODO: getEmailToSendWorks (reading from emailToSend.txt)
testList1 = getEmailToSend("emailToSend.txt", "Rob Brodin")
print testList1
testList = getEmailAddresses("collegeEmailAddresses.txt")
print testList

count = 0
email = []
name = []
while count < len(testList):
    if(count % 2 == 0):
        email.append(testList[count])
    else:
        name.append(testList[count].replace("\n", ""))
    count+=1
print email
print name

# TODO: Code works up until here! As of 11:37 AM
messages = []
for n in name:
    messages.append(getEmailToSend("emailToSend.txt", n))

def getAccountInfo(txtFile):
    # Keys in the hashmap are name, email, password, and title
    userInfo = {}
    fileToRead = open(txtFile, "r")
    for line in fileToRead:
        key = ""
        value = ""
        hitDash = False
        for word in line:
            if (word == "-"):
                hitDash = True
            elif not hitDash:
                key += word
            else:
                value += word
        userInfo[key.strip().lower()] = (value.replace("\n", "")).lstrip()
    return userInfo

print messages
userInfo = getAccountInfo("accountInfo.txt")
print userInfo

counter = 0
for message in messages:
    sendEmail(userInfo["email"], userInfo["password"], email[counter], message, userInfo["name"],
              userInfo["title"])
    counter+=1
