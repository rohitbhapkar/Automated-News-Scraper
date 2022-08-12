#------AUTOMATED NEWS SCRAPER AND MAIL RECEIVER------
#------Code By- Rohit Bhapkar----------


import requests #http requests
from bs4 import BeautifulSoup #web Scraping
import smtplib #send mail
#for email body-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


now =datetime.datetime.now() #to get day and date of the email we get

#email content placeholder
content = ''

#extracting Hacker News Headlines

def extract_news(url):
    print("Extracting Hacker News Stories")
    cnt=''
    cnt +=('<b>HN Top Stories: </b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign':''})):
        cnt+=((str(i+1) + ' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
        print(tag.prettify)
    return (cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ("<br>------<br>")
content +=('<br><br>End of Message')

#Sending the email
print("Composing Email")


#email details
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = 'rohitubhapkar@gmail.com'
TO = 'rohitubhapkar@gmail.com'
PASS = '' # Enter your password for authentication


msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()

