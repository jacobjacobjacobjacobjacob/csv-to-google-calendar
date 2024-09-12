# Automating Adding Events to Google Calendar

This Python script enables users to automate the process of adding events to their Google Calendar. It utilizes the Google Calendar API and offers functionalities such as adding manual events, importing events from a CSV file, and printing upcoming events.

## Prerequisites

Before using this script, ensure you have:

- Python installed on your system.
- Google API credentials set up. Instructions for obtaining credentials can be found [here](https://developers.google.com/workspace/guides/create-credentials).
- The easiest way is downloading the credentials as a .json file, copy/paste the contents of that json file into credentials.json. 
- Necessary Python modules installed, including `google-auth`, `google-auth-oauthlib`, and `google-api-python-client`. You can install these using pip:

```
pip install -r requirements.txt
```
# Usage
Clone the repository to your local machine:
```
git clone https://github.com/jacobjacobjacobjacobjacob/csv-to-google-calendar.git
```
Navigate to the directory containing the script:
```
cd csv-to-google-calendar
```
Run the script:
```
python3 main.py
```

Before running the script, you have to update 'credentials.json' as described above.

In 'config.py' you need to configure the calendar name, and the csv file name that you're working with.

Follow the on-screen prompts to add events manually, import events from a CSV file, or print upcoming events.



# To-do
- Export events to CSV: Add functionality to export calendar events to a CSV file.
