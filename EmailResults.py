import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import config
import os

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

        sent_from = config.gmail_user
        to = [config.send_to]
        subject = 'f'
        body = "*******\n %s \n*******\n %s \n\nRSI: %s %s \n robinhood.com/stocks/%s  \n*******" % (tic, d.to_string(index=False), str(round(RSI,2)), emoji, tic )

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)


        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart()
        msg['Subject'] = "Link"
        msg['From'] = config.gmail_user
        msg['To'] = config.send_to

        # Create the body of the message (a plain-text and an HTML version).
       # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        
        
        
        img_data = open(config.GRAPH_FILE_NAME, 'rb').read()

        image = MIMEImage(img_data, name=os.path.basename(config.GRAPH_FILE_NAME))


        # Add attachment to message and convert message to string
        
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(body, 'plain')
        #part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(image)
        # msg.attach(part2)







        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.set_debuglevel(True) # show communication with the server

            server.ehlo()
            server.login(config.gmail_user, config.gmail_password)
            server.sendmail(sent_from, to, msg.as_string(), "HTML")
            server.close()
            print("Sent")




        except:
            print('Something went wrong...')



    
            
    def SendMessage(body):

        print(config.gmail_user)
    
        
        sent_from = config.gmail_user
        to = [config.send_to]
        subject = 'f'
        #body = "\n*******\n %s \n robinhood.com/stocks/%s \n*******" % (d, tic )

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)


        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Bot Log"
        msg['From'] = config.gmail_user
        msg['To'] = config.send_to

        # Create the body of the message (a plain-text and an HTML version).
    
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(body, 'plain')
        #part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        # msg.attach(part2)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.set_debuglevel(True) # show communication with the server

            server.ehlo()
            server.login(config.gmail_user, config.gmail_password)
            server.sendmail(sent_from, to, msg.as_string(), "HTML")
            server.close()
            print("Sent")




        except Exception as e:
            print(e)
            
            
            
    def SendEmailMessage(body):


        
            sent_from = config.gmail_user
            to = [config.send_to]
            subject = 'f'
            #body = "\n*******\n %s \n robinhood.com/stocks/%s \n*******" % (d, tic )

            email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)


            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Bot Log"
            msg['From'] = config.gmail_user
            msg['To'] = config.send_to

 
    
            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(body, 'plain')
            #part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            # msg.attach(part2)

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.set_debuglevel(True) # show communication with the server

                server.ehlo()
                server.login(config.gmail_user, config.gmail_password)
                server.sendmail(sent_from, to, msg.as_string(), "HTML")
                server.close()
                print("Sent")




            except Exception as e:
                print(e)
