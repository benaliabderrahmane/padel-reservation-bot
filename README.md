# Padel Court Reservation Bot

This Python script automates the process of logging in and reserving a padel court on the TMO Padel website.

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Setup

1. Install the required Python packages:

```bash
pip install selenium
```


2. Download ChromeDriver and place it in the specified path in the script.

3. Update the following variables in the script:
- `executable_path`: Path to your ChromeDriver
- `options.binary_location`: Path to your Chrome executable

4. (Optional) Modify the login credentials, desired date, and time as needed.

## Usage

Run the script using Python:

```bash
python main.py
```

## Disclaimer

This script interacts with a third-party website. Use it responsibly and in accordance with the website's terms of service.
