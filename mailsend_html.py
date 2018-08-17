def send_email(user, pwd, recipient, subject, body,message):
    import smtplib
    from email.utils import formatdate
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
 
    #TO = recipient
    #TO = recipient if isinstance(recipient, list) else [recipient]
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['message'] = message
    MESSAGE['To'] = ", ".join(recipient)
    MESSAGE['From'] = user
    #MESSAGE.preamble = """
    #Your mail reader does not support the report format.
    #Please visit us <a href="http://www.mysite.com">online</a>!"""
    #body="Hi All, Below is the list of services along with their versions"
    HTML_BODY = MIMEText(body, 'html')
    MESSAGE.attach(HTML_BODY)


    # Prepare actual message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # Print debugging output when testing
        if __name__ == "__main__":
              server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, recipient, MESSAGE.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print('failed to send mail')
        if __name__ == "__main__":
             """Executes if the script is run as main script (for testing purposes)"""
#emailnotifyaddress=['devops@oronetworks.com']
#emailnotifyaddress=['engineering@oronetworks.com']
emailnotifyaddress=['jayant.rai@oronetworks.com','abhishek.ranjan@oronetworks.com']
#emailnotifyaddress=['jiten.sharma@oronetworks.com','venkat.swamy@oronetworks.com','jayant.rai@oronetworks.com','abhishek.ranjan@oronetworks.com','ajay.malik@oronetworks.com']
#emailnotifyaddress=['venkat.swamy@oronetworks.com']
subject='ENG-PROD Comparison'
message= 'The following table lists all the services with unique version number'
f= open('report.html', 'r')
content = f.read()
f.close()
f= open('/home/scripts/file-diff/diff.html', 'r')
content += f.read()
f.close()

send_email('no-reply@oronetworks.com', '5S2ZDjL74c', emailnotifyaddress, subject,content,message)
f.close()

