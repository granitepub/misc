#!/bin/python3

import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient import errors, discovery
import mimetypes
from email.mime.base import MIMEBase
from email import encoders

MAC = "MacMini"
MAC_DIRECTORY = "/Users/MacMini/Dropbox/PressReports"
LAPTOP = os.environ['HOME']
#LAPTOP_DIRECTORY = "/home/deadpool/Dropbox/PressReports"
#LAPTOP_DIRECTORY = "/home/logan/Dropbox/PressReports/pdf_files"
LAPTOP_DIRECTORY = os.environ['HOME'] + "/Dropbox/PressReports/pdf_files"

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service

def create_message(sender, to, subject, message_text, message_html):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart('alternative')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  message.attach(MIMEText(message_text, 'plain'))
  message.attach(MIMEText(message_html, 'html'))
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  body = {'raw': raw}
  return body


def create_message_with_attachment(sender, to, subject, message_text, message_html, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  # message.attach(MIMEText(message_text, 'plain'))
  message.attach(MIMEText(message_html, 'html'))

  message = addAttachments(file, message)

  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  body = {'raw': raw}
  return body

def addAttachments(list, message):
  if list is not None:
    for each_file_path in list:
      try:
        file_name = each_file_path.split("/")[-1]
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(each_file_path, "rb").read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=' + file_name)
        message.attach(part)
      except:
        print("could not attache file")
    return message

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def createPlainMessageBody(file):
  msgPlain = "Here is the list of files attached: \n"
  for f in file:
    msgPlain += '\t' + f.split("/")[-1] + '\n'

  msgPlain += '\n\n\n\n\n'
  return msgPlain

def createHTMLMessageBody(file):
  msgHtml = "Here is the list of files attached:"
  for f in file:
    msgHtml += "<br/>" + f.split("/")[-1]
  msgHtml += "<br/>" + "<br/>" + "<br/>" + "<br/>"
  return msgHtml

def startEmail(file):
  #to = "dcpressroom1@gmail.com, dixiepub@gmail.com"
  #to = "jglisson@dailycorinthian.com"
  #to = "rterry@dailycorinthian.com"
  to = "rterry@dailycorinthian.com, mwynn@jonesborosun.com"

  sender = "dcpressroom1@gmail.com"
  subject = "Press Reports"
  msgHtml = createHTMLMessageBody(file)
  msgPlain = createPlainMessageBody(file)
  user_id = "me"
  service = get_credentials()
  
  # message = create_message(sender, to, subject, msgPlain, msgHtml)
  # send_message(service, user_id, message)
  
  message1 = create_message_with_attachment(sender, to, subject, msgPlain, msgHtml, file)
  send_message(service, user_id, message1)

def getFiles(files):
  filenames = [os.path.join(files, f) for f in os.listdir(files)]
  # use below to send xlsx files --
  #fileList = [f for f in filenames if ".xlsx" in f]
  fileList = [f for f in filenames if ".pdf" in f]
  
  return fileList

def main():
  if os.environ['LOGNAME'] == MAC:
    attachment_directory = MAC_DIRECTORY
  else:
    attachment_directory = LAPTOP_DIRECTORY
  files = getFiles(attachment_directory)
  startEmail(files)


if __name__ == '__main__':
  main()
