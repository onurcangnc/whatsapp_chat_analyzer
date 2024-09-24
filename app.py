from flask import Flask, request, send_file, render_template, session, redirect, url_for, flash, after_this_request
import os
import pandas as pd
import re
from datetime import datetime
import tempfile
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from collections import defaultdict

app = Flask(__name__)
# Get the secret key from environment variable FLASK_SECRET_KEY or use a fallback key
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_key')

def parse_whatsapp_chat(file):
    message_pattern = r'\[(\d{1,2})\.(\d{1,2})\.(\d{4}),? (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)'
    chat_data = []
    current_message = None

    # Read and decode the file
    for line in file:
        line = line.decode('utf-8').strip()
        if not line:
            continue

        match = re.match(message_pattern, line)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            time_str = match.group(4)
            sender = match.group(5)
            message = match.group(6)

            date_time_str = f'{day}.{month}.{year} {time_str}'
            try:
                date_time_obj = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M:%S')
            except ValueError as ve:
                print(f"Date parsing error: {ve} for line: {line}")
                continue

            chat_data.append({
                'Date': date_time_obj.date(),
                'Time': date_time_obj.time(),
                'Datetime': date_time_obj,
                'Sender': sender,
                'Message': message
            })
            current_message = len(chat_data) - 1
        elif current_message is not None:
            # Handle multi-line messages
            chat_data[current_message]['Message'] += '\n' + line

    return pd.DataFrame(chat_data)

# Function to calculate average reply times
def calculate_average_reply_time(df):
    reply_times = defaultdict(list)
    previous_sender = None
    previous_time = None

    for i, row in df.iterrows():
        current_sender = row['Sender']
        current_time = row['Datetime']

        if previous_sender and previous_sender != current_sender:
            time_difference = (current_time - previous_time).total_seconds() / 60  # Convert to minutes
            reply_times[previous_sender].append(time_difference)

        previous_sender = current_sender
        previous_time = current_time

    average_reply_times = {sender: sum(times) / len(times) for sender, times in reply_times.items() if times}
    return average_reply_times

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('fileup')
        if file and file.filename.endswith('.txt'):
            # Parse the uploaded file
            parsed_chat = parse_whatsapp_chat(file)

            # Check if parsed_chat is empty
            if parsed_chat.empty:
                flash("Parsed chat is empty. Please check the chat format and try again.", 'error')
                return redirect(url_for('index'))

            # Calculate average reply times for each sender
            avg_reply_times = calculate_average_reply_time(parsed_chat)

            # Create a temporary Excel file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx').name
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                parsed_chat.to_excel(writer, sheet_name='Parsed Chat', index=False)

                # Access the workbook and sheet
                workbook = writer.book
                worksheet = writer.sheets['Parsed Chat']

                # Adjust column widths
                worksheet.column_dimensions['A'].width = 15  # Date column
                worksheet.column_dimensions['B'].width = 10  # Time column
                worksheet.column_dimensions['C'].width = 25  # Datetime column
                worksheet.column_dimensions['D'].width = 20  # Sender column
                worksheet.column_dimensions['E'].width = 50  # Message column

                # Summary of messages per sender
                message_summary = parsed_chat['Sender'].value_counts().reset_index()
                message_summary.columns = ['Sender', 'Total Messages']
                message_summary.to_excel(writer, sheet_name='Message Summary', index=False)

                # Adjust column
