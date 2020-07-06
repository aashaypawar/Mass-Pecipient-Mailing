from __future__ import print_function
import time
import sys
import smtplib
import mimetypes
import email
import email.mime.application
import pdb

final_data = []

if len(sys.argv) == 1:
	print ("\nSYNTAX ERROR\nCorrect Syntax: python send_mail.py MAIL_PASSWORD_HERE\n")
	quit()
else:
	psswrd = sys.argv[1]


email_id = 'batman@justiceleague.org'
identification = 'Justice League Inc.'
SMTP_server = 'mail.justiceleague.org'
subject = "Resignition Citing Lack of Superpowers"
attachment_path_and_name = "./sample_attachment.jpg"



def get_data():

	with open(target_csv) as f:
		data = f.readlines()
	data = [i.split(',') for i in data]

	fi = []
	for row in data[1:]:
		fi.append({
						'email': row[2],
						'name': row[1].title(),
						'attachment': attachment_path_and_name
					})
	return fi


mail_details = {
		'email' : email_id,
		'identity': identification,
		'password' : psswrd,
		'SMTP-server' : SMTP_server
		}

def SEND_MAIL(name, to_EMAIL, attachment):
	print("SENDING to %s" %(to_EMAIL))
	TO_EMAIL = to_EMAIL


	msg = email.mime.Multipart.MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = mail_details['identity'] + " <" + mail_details['email'] + ">"
	msg['To'] = TO_EMAIL
	msg.preamble = 'This is a multi-part message in MIME format.'


	with open('salutation.txt', 'r') as f:
		salutation = "".join(f.readlines())
	with open('body.txt', 'r') as f:
		body = "".join(f.readlines())
	content = salutation.strip() + " " + name.strip() + body.strip()
	body = email.mime.Text.MIMEText(content, 'html')
	msg.attach(body)
	

	filename=attachment
	with open("./" + filename) as fp:
		att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
	att.add_header('Content-Disposition','attachment',filename=filename)
	msg.attach(att)
	

	s = smtplib.SMTP(mail_details['SMTP-server'])
	s.starttls()
	s.login(mail_details['email'], mail_details['password'])
	s.sendmail(mail_details['email'], TO_EMAIL, msg.as_string())
	s.quit()


def wait():
	time.sleep(60)
	return

if __name__=="__main__":
	final_data = get_data()
	for i, data in enumerate(final_data):
		print("%d/%d: "%(i+1, len(final_data)),end="")
		try:
			SEND_MAIL(data['name'], data['email'], data['attachment'])
		except (smtplib.SMTPRecipientsRefused), err:
			wait()
			continue
		if not i%100 and i!=0:
			wait()
		else:
			time.sleep(2)
	print("Completed")
