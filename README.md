# School Closings Email Alerts (Gmail)

Recieve School Closing Alerts based on Channel 5 Closures. Hosted on azure VM refreshing every 5min.

## Features

- Fetches school closing data from a website.
- Sends email alerts for specific schools.
- Prevents duplicate alerts.


## Prerequisites

- Python 3.x
- Required Python libraries (defined in `requirements.txt`)
- Azure Virtual Machine (optional, for scheduled execution)

## Setup

1. **Clone Repository**: Clone this repository to your local machine:

   ```bash
   git clone https://github.com/molin6/SchoolClosureAlerts.git
   cd SchoolClosingsText
Install Dependencies: Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
Gmail Credentials: Create a .env file in the project directory and add your Gmail credentials:

plaintext
Copy code
GMAIL_USERNAME=your_email@gmail.com
GMAIL_PASSWORD=your_email_password
RECIPIENT_EMAIL=recipient_email@example.com
Replace the placeholders with your actual Gmail email address and password, as well as the recipient's email address.

Usage
To run the script, use the following command:

bash
Copy code
python fetch_closings.py
You can schedule this script to run periodically (e.g., every 5 minutes) on a virtual machine to receive real-time email alerts for school closings.

Support
If you encounter any issues or have questions, feel free to create an issue in this repository.
