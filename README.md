# WhatsApp Chat Analyzer

## Overview

The **WhatsApp Chat Analyzer** is a web-based application that allows users to upload WhatsApp chat logs in `.txt` format and analyze them. The application processes the chat data and generates insights such as average reply times, message counts, and more. Additionally, users can upload CSV or Excel files to further analyze the data and download a psychological report on the chat participants.

## Features

- Upload WhatsApp chat logs in `.txt` format for analysis.
- Upload CSV/Excel files for advanced analysis.
- Download processed chat data in CSV format.
- Generate psychological reports from CSV/Excel data.
- Responsive design and clean user interface using Bootstrap.
- Includes validation for file types before uploading.
  
## Tech Stack

- **Backend**: Flask (Python) ![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- **Frontend**: HTML, CSS, JavaScript, jQuery, Bootstrap ![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black) ![jQuery](https://img.shields.io/badge/jQuery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
- **Processing**: Pandas for CSV/Excel data manipulation ![Pandas](https://img.shields.io/badge/Pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
- **Deployment**: Gunicorn, Heroku ![Gunicorn](https://img.shields.io/badge/Gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Heroku](https://img.shields.io/badge/Heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white) 
- **AI Integration**: OpenAI GPT-4 API for human psychology report generation ![OpenAI](https://img.shields.io/badge/OpenAI-%231A1A1A.svg?style=for-the-badge&logo=openai&logoColor=white) 

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
```

2. **Install dependencies:**

- You can find all dependencies in ```requirements.txt```. Install them using pip:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

- Create a ```.env``` file in the project root and define the following variables:

```bash
FLASK_SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

4. **Run the app locally:**

```bash
flask run
The app will be available at http://127.0.0.1:5000/.
```

5. **Deploy on Heroku:**

- Use the ```Procfile``` provided for deployment on Heroku.

```bash
heroku create
git push heroku master
```

## Usage

1. Uploading a WhatsApp chat log:

2. Browse and select a ```.txt``` file containing a WhatsApp chat export.
Once uploaded, the chat log will be processed and analyzed.
Download CSV:

3. After processing the chat log, you can download the analyzed data as a CSV file.

4. Generating Psychological Report:

- You can also upload CSV/Excel files to generate psychological reports about the chat participants.

## File Structure

- ```app.py```: Contains the Flask server logic and routes.

- ```requirements.txt```: Lists the Python dependencies required for the project.

- ```Procfile```: Configuration for deploying on Heroku.

- ```static/```: Contains static files such as custom CSS (style.css) and 
JavaScript (script.js).

- ```templates/```: Contains HTML templates such as index.html.
Contributing


## Contributing

- Feel free to fork the project, open issues, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.


Author: Onurcan Genç 

[Portfolio](https://onurcangenc.com.tr)



```bash
This `README.md` covers the project overview, installation, usage, and deployment steps while including relevant details from the files you uploaded. Let me know if you'd like any changes!
```




