# Automating Adding Events to Google Calendar

This Python script enables users to automate the process of adding events to their Google Calendar. It utilizes the Google Calendar API and offers functionalities such as adding manual events, importing events from a CSV file, and printing upcoming events.

## Prerequisites

Before using this script, ensure you have:

- Python installed on your system.
- Google API credentials set up. Instructions for obtaining credentials can be found [here](https://developers.google.com/workspace/guides/create-credentials).
- Necessary Python modules installed, including `google-auth`, `google-auth-oauthlib`, and `google-api-python-client`. You can install these using pip:

```
pip install google-auth google-auth-oauthlib google-api-python-client
```
# Usage
Clone the repository to your local machine:
```
git clone https://github.com/your-username/your-repository.git
```
Navigate to the directory containing the script:
```
cd your-repository
```
Run the script:
```
python main.py
```
Follow the on-screen prompts to add events manually, import events from a CSV file, or print upcoming events.

Update the `.env` file with the required configurations. Make sure to provide necessary details such as API keys, calendar names, and other environment variables needed for the script to run smoothly.
