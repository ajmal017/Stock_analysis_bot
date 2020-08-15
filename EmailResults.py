import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import config
import os
import Secrets
class EmailResults:
    
    
    def __init__(self, update=True):
        pass

                
    def SendResults(tic, d, RSI):

        if(RSI > 70):
            emoji=config.fire
        elif(RSI<30):
            emoji=config.ICE
        else:
            emoji=config.NEUTRAL_FACE
  
        body = "*******\n %s \n*******\n %s \n\nRSI: %s %s \n robinhood.com/stocks/%s  \n*******" % (tic, "howdy", str(round(RSI,2)), emoji, tic )

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = "Link"
        msg['From'] = Secrets.gmail_user
        msg['To'] = config.send_to

        img_data = open(config.GRAPH_FILE_NAME, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(config.GRAPH_FILE_NAME))
        part1 = MIMEText(body, 'plain')

        msg.attach(part1)
        msg.attach(image)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.set_debuglevel(True) # show communication with the server

            server.ehlo()
            server.login(Secrets.gmail_user, Secrets.gmail_password)
            server.sendmail(Secrets.gmail_user, config.send_to, msg.as_string(), "HTML")
            server.close()
            print("Sent")
        except Exception as e:
            print(e)
      

            
    def SendMessage(body, subject, send_to):
   
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Secrets.gmail_user
        msg['To'] = config.send_to
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.set_debuglevel(True) # show communication with the server

            server.ehlo()
            server.login(Secrets.gmail_user, Secrets.gmail_password)
            server.sendmail(Secrets.gmail_user, send_to, msg.as_string(), "HTML")
            server.close()
            print("Sent")
        except Exception as e:
            print(e)
         
