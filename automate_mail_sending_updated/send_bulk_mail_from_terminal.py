import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

# status indicators
blueinfo = "\033[0;34m[i]\033[0m"
greenplus = "\033[1;32m[+]\033[0m"
yellowminus = "\033[1;33m[-]\033[0m"
redminus = "\033[1;31m[-]\033[0m"
redexclaim = "\033[1;31m[!]\033[0m"
redexclaimblink="\033[1;31m[\033[5;31m!\033[0m\033[1;31m]\033[0m"

def read_candidates_from_file(file_path):
    candidates = []
    with open(file_path, "r") as file:
        for line in file:
            email, name = line.strip().split("\t")
            candidates.append((email, name))
    return candidates

def send_email(sender_email, recipient_email, subject, body, app_password):
    try:
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create a MIMEText object to represent the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Replace [candidate_name] with candidate's first name in the email body
        first_name = recipient_name.split()[0]
        personalized_body = body.replace("[candidate_name]", first_name)

        # Attach the body of the personalized email
        msg.attach(MIMEText(personalized_body, "plain"))

        # Create an SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, app_password)  # Login to your Gmail account using the App password

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"{blueinfo} Email sent successfully to {recipient_name} <{recipient_email}>")
        return 1
    except Exception as e:
        print(f"{redminus} Error occurred while sending email to {recipient_name} <{recipient_email}>: {str(e)}")
        return 0

if __name__ == "__main__":
    sender_email = input(f"\n{greenplus} Enter your Gmail address: ")
    app_password = getpass.getpass(f"{greenplus} Enter your Gmail App password: ")
    print("")

    file_path = "candidate_name_email.txt"

    with open("email_body.txt", "r") as email_body_file:
        body = email_body_file.read()

    with open("email_subject.txt", "r") as email_subject_file:
        subject = email_subject_file.read()

    candidates = read_candidates_from_file(file_path)

    total_emails_sent = 0
    for email, name in candidates:
        recipient_email = email.strip()
        recipient_name = name.strip()
        # Replace [candidate_name] with the candidate's first name in the email body
        # Use the full name (first name and last name) in the subject (if [candidate_name] exists in the subject)
        personalized_subject = subject.replace("[candidate_name]", recipient_name)
        total_emails_sent += send_email(sender_email, recipient_email, personalized_subject, body, app_password)

    print("\n---------------------------------------------------------------------------")
    print(f"\n{blueinfo} Total Emails Sent: {total_emails_sent}")
    print(f"\n{redexclaimblink} DELETE THE APP PASSWORD FROM YOUR ACCOUNT IF YOU ARE DONE! {redexclaimblink}\n")
