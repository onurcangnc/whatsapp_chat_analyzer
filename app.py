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
app.secret_key = "737571bcdb8a096e3562f662a183d1b9362c62cfc36d6f58"  # Replace with a secure key for session handling

# Updated WhatsApp parsing function
def parse_whatsapp_chat(file):
    message_pattern = r'\[(\d{2}\.\d{2}\.\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)'
    chat_data = []
    current_message = None

    # Read and decode the file
    for line in file:
        line = line.decode('utf-8').strip()
        if not line:
            continue

        match = re.match(message_pattern, line)
        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            sender = match.group(3)
            message = match.group(4)

            date_time_str = f'{date_str} {time_str}'
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

                # Summary of messages per sender
                message_summary = parsed_chat['Sender'].value_counts().reset_index()
                message_summary.columns = ['Sender', 'Total Messages']
                message_summary.to_excel(writer, sheet_name='Message Summary', index=False)

                # Average reply time sheet
                avg_reply_df = pd.DataFrame(list(avg_reply_times.items()), columns=['Sender', 'Average Reply Time (mins)'])
                avg_reply_df.to_excel(writer, sheet_name='Avg Reply Time', index=False)

                # Generate pie charts for data analysis
                plt.figure(figsize=(8, 6))
                plt.pie(message_summary['Total Messages'], labels=message_summary['Sender'], autopct='%1.1f%%')
                plt.title('Messages Sent by Each Sender')
                msg_pie_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
                plt.savefig(msg_pie_image_path)

                plt.figure(figsize=(8, 6))
                plt.pie(avg_reply_df['Average Reply Time (mins)'], labels=avg_reply_df['Sender'], autopct='%1.1f%%')
                plt.title('Average Reply Time by Each Sender')
                reply_pie_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
                plt.savefig(reply_pie_image_path)

                # Insert pie charts into the workbook
                workbook = writer.book
                worksheet_graphs = workbook.create_sheet('Pie Charts')
                img_msg_pie = ExcelImage(msg_pie_image_path)
                worksheet_graphs.add_image(img_msg_pie, 'A1')
                img_reply_pie = ExcelImage(reply_pie_image_path)
                worksheet_graphs.add_image(img_reply_pie, 'A20')

            # Store the file path for download
            session['output_file'] = output_path
            session['file_downloaded'] = False  # Track download status

            flash("File processed successfully.", "success")
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    output_file = session.get('output_file')
    if not output_file or not os.path.exists(output_file):
        flash("No file available to download.", "error")
        return redirect(url_for('index'))

    # Check if file has already been downloaded
    if session.get('file_downloaded'):
        flash("The file has already been downloaded.", "error")
        return redirect(url_for('index'))

    # Mark the file as downloaded
    session['file_downloaded'] = True

    # Delete the file after sending it to the user
    @after_this_request
    def remove_file(response):
        try:
            os.remove(output_file)
            session.pop('output_file', None)  # Clear the file from the session
        except Exception as e:
            print(f"Error deleting file: {e}")
        return response

    return send_file(output_file, as_attachment=True, download_name="parsed_chat_with_reply_times.xlsx")


if __name__ == '__main__':
    app.run(debug=True)
