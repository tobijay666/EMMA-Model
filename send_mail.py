import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email_with_pdf(userName, recipient_email):
    pdf_file_path = f'Reports/{userName}\'s_Sentimental_evaluation_report.pdf'
    # Set up the email message
    msg = MIMEMultipart()
    msg['Subject'] = 'PDF Report'
    msg['From'] = 'emmaai2023@gmail.com'
    msg['To'] = recipient_email

    # Attach the PDF file
    with open(pdf_file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file_path)

    msg.attach(attachment)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    # server = smtplib.SMTP('localhost')
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 467)
    server.starttls()
    server.login('emmaai2023@gmail.com', EMAIL_PASSWORD)
    server.sendmail('emmaai2023@gmail.com', recipient_email, msg.as_string())
    print("Email sent successfully")
    server.quit()




