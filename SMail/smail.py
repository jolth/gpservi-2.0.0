# -*- coding: UTF-8 -*-
"""
 Módulo para el envio de e-mail
"""
import smtplib
import sys
import email.utils
from email.mime.text import MIMEText

#sender = 'rastree@devmicrosystem.com'
#sender = 'www-data@rastree.com'

#def sendMail(receivers, subject='Simple test message', text='This is body of the message.', sender='www-data@rastree.com', hostname='localhost'):
#def sendMail(receivers, subject='Simple test message', text='This is body of the message.', sender='mailer-daemon@rastree.com', hostname='localhost'):
def sendMail(receivers, subject='Simple test message', text='This is body of the message.', sender='rastree@rastree.com', hostname='localhost'):
    """
        Usage:
            >>> import smail
            >>> 
            >>> sender = 'rastree@devmicrosystem.com'
            >>> receivers = {'Soporte':'soporte@devmicrosystem.com', 'Jorge Toro':'jorge.toro@devmicrosystem.com'}
            >>> subject='Simple test message'
            >>> text="Este es un mensaje de prueba"
            >>> smail.sendMail(receivers, subject, text, sender)
            >>> 
    """
    ## Create the message
    msg = MIMEText(text)
    r = [(k, v) for k, v in receivers.iteritems()]
    for k in r:
        # Header Receivers 
        msg['To']=email.utils.formataddr(k)
    msg['From'] = email.utils.formataddr(('App Rastree', sender))
    msg['Subject'] = subject
    # Receivers
    r = [v for v in receivers.values()]
    # Server
    server = smtplib.SMTP(hostname)
    server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(sender, r, msg.as_string())
        print >> sys.stderr, "**********\nSuccessfully sent email\n**********"
    except:
        print >> sys.stderr, "**********\nError: Unable to send email\n**********"
        print >> sys.stderr, sys.exc_info()
    finally:
        server.quit()
