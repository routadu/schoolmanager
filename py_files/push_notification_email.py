import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime as dt



def send_mail_single(sender_address,sender_password,receiver_address,subject,message,school_name):

    try:

        time=dt.now().strftime("%H:%M")
        date=dt.now().strftime("%d-%m-%Y")

        message=message+"\n\n\n\n\n\n\n\n\n\nThis message was sent on {} at {}\n\nFrom: {} Mail System".format(date,time,school_name)

        s=smtplib.SMTP(host='smtp.gmail.com',port='587')
        s.starttls()
        s.login(sender_address,sender_password)

        msg=MIMEMultipart()

        msg['From']=sender_address
        msg['To']=receiver_address
        msg['Subject']=subject

        msg.attach(MIMEText(message,'plain'))


        s.send_message(msg)
        del msg

        s.quit()

        return 'Sent Successfully'
    
    except:

        return 'Something Went Wrong'

def send_email_multiple(sender_address,sender_password,receiver_address_lst,subject,message,school_name):

    try:

        time=dt.now().strftime("%H:%M")
        date=dt.now().strftime("%d-%m-%Y")
        
        s=smtplib.SMTP(host='smtp.gmail.com',port='587')
        s.starttls()
        s.login(sender_address,sender_password)

        message=+"\n\n\n\n\n\n\n\n\n\nThis message was sent on {} at {}\n\nFrom: {} School Mail System".format(date,time,school_name)
        
        for child_receiver in receiver_address:
            
            msg=MIMEMultipart()

            msg['From']=sender_address
            msg['To']=child_receiver
            msg['Subject']=subject

            msg.attach(MIMEText(message,'plain'))


            s.send_message(msg)
            del msg

        s.quit()

        return 'Sent Successfully'
    
    except:

        return 'Something Went Wrong'
        
def MailServiceCheckUp(mail_username,mail_password):

    try:
        
        s=smtplib.SMTP(host='smtp.gmail.com',port='587')
        s.starttls()
        s.ehlo()
        s.login(mail_username,mail_password)

        return 'Successful'

    except smtplib.SMTPHeloError:

        return 'Domain Error'
    
    except smtplib.SMTPAuthenticationError:

        return 'Authentication Error'

    except smtplib.SMTPException:

        return 'Some Error Occured'
   
        
