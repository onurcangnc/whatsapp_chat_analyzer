# WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is a Flask-based web application that processes exported WhatsApp chat files, analyzes them, and generates insightful metrics. It supports conversion of chat files into structured formats (CSV, Excel) and provides data visualizations such as pie charts for message distribution and average reply times.

## Features

- **WhatsApp Chat Parsing**: Automatically parses WhatsApp chat exports, detecting messages, senders, and timestamps.
- **Data Export**: Outputs processed chat data as CSV and Excel files.
- **Analytics**:
  - Message count per sender
  - Average reply time per sender
- **Data Visualization**: Generates pie charts to visualize:
  - Distribution of total messages per sender
  - Average reply times per sender

  ## Technologies Used

- ![Flask](https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png) **Flask**: Backend web framework
- ![Pandas](https://github.com/marwin1991/profile-technology-icons/assets/76012086/24b02d77-2f28-43c7-b5d6-e15e3395851b) **Pandas**: Data processing and analysis
- ![Matplotlib](https://matplotlib.org/_static/logo_light.svg) **Matplotlib**: Data visualization for generating charts
- ![OpenPyXL](https://openpyxl.readthedocs.io/en/stable/_static/logo.png) **OpenPyXL**: To create Excel files with charts embedded
- ![Heroku](https://logowik.com/content/uploads/images/heroku8748.jpg) **Heroku**: Deployment platform for the application

