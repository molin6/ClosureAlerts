import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.gmail.com'  # Gmail SMTP server
smtp_port = 587  # Gmail SMTP port (TLS)
sender_email = ''  # Your Gmail email address
sender_password = ''  # Your Gmail password
receiver_email = ''  # Email address to receive alerts


# Function to fetch school closings
def fetch_school_closings(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    closing_items = soup.find_all('li', class_='closings__item')
    school_closings = []
    for item in closing_items:
        school_name = item.find('span', class_='closings__title').get_text(strip=True)
        closing_status = item.find('span', class_='closings__body').get_text(strip=True)
        school_closings.append({'name': school_name, 'status': closing_status})

    return school_closings

# Function to read previous data from a file
def read_previous_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to write data to a file
def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Function to process closures
def process_closures(current_data, previous_data):
    new_closures = [school for school in current_data if school not in previous_data]
    ongoing_closures = [school for school in previous_data if school in current_data]
    closed_closures = [school for school in previous_data if school not in current_data]

    return new_closures, ongoing_closures, closed_closures

# Function to check if a school is a target school
def is_target_school(school, target_schools):
    return school['name'] in target_schools

def send_email_alert(schools, smtp_server, smtp_port, sender_email, sender_password, receiver_email):
    subject = "School Closures Alert"

    # Create an HTML table for the list of closures with inline CSS styles
    body = "<html><body>"
    body += "<h2 style='color: #007acc;'>School Closures Alert</h2>"
    body += "<table style='border-collapse: collapse; width: 100%;' border='1' cellpadding='8'><tr>"
    body += "<th style='background-color: #007acc; color: white; text-align: left; padding: 8px;'>School Name</th>"
    body += "<th style='background-color: #007acc; color: white; text-align: left; padding: 8px;'>Closure Status</th></tr>"
    
    for school in schools:
        body += f"<tr><td style='padding: 8px;'>{school['name']}</td><td style='padding: 8px;'>{school['status']}</td></tr>"
    
    body += "</table></body></html>"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email alert sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")

def main():
    url = 'https://www.5newsonline.com/closings'
    current_data = fetch_school_closings(url)

    file_path = 'closures.txt'
    previous_data = read_previous_data(file_path)

    target_schools = ["Bentonville School District", "Fayetteville School District", "Rogers School District"]

    new_closures, ongoing_closures, closed_closures = process_closures(current_data, previous_data)

    new_target_closures = [school for school in new_closures if is_target_school(school, target_schools)]

    if new_target_closures:
        print(f"New target closures detected: {new_target_closures}. Sending email alerts...")
        send_email_alert(new_target_closures, smtp_server, smtp_port, sender_email, sender_password, receiver_email)
        # Update the file with current data (including new closures)
        write_data(file_path, current_data)

    if closed_closures:
        print("Some closures are no longer listed. Updating records...")
        # Remove closed closures from the list in the current data
        updated_current_data = [school for school in current_data if school not in closed_closures]
        write_data(file_path, updated_current_data)  # Update the file without closed closures

    if not new_target_closures and not closed_closures:
        print("No new changes detected for target schools.")

if __name__ == '__main__':
    main()
