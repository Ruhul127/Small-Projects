import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Load Mixed Data (text and numbers) from a CSV or Excel file
def load_data(file_path):
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

#Process and manipulate the mixed data (example)
def process_data(data):
    # Perform data validation, transformations, or cleaning here
    # Example: fill missing numerical data with a default value and strip text columns
    data['numeric_column'] = data['numeric_column'].fillna(0)
    data['text_column'] = data['text_column'].str.strip()

    return data

#Save the updated data back to a file
def save_data(data, output_file):
    try:
        data.to_excel(output_file, index=False)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving data: {e}")

#Automate the task and send notification via email (optional)
def send_email_notification(receiver_email, subject, body):
    try:
        sender_email = "your_email@example.com"
        password = "your_password"

        # Set up the server
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()

        # Login to the email account
        server.login(sender_email, password)

        # Craft the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(msg)
        server.quit()

        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main automation workflow
if __name__ == "__main__":
    input_file = "data.xlsx"  # Replace with the actual path to the data file
    output_file = "processed_data.xlsx"

    # Load the data
    data = load_data(input_file)
    
    if data is not None:
        # Process the data
        processed_data = process_data(data)

        # Save the updated data
        save_data(processed_data, output_file)

        # Optionally, send an email notification
        send_email_notification("recipient@example.com", "Task Completed", "Data entry task is complete.")
