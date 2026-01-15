# Sequential Web Scraper

A comprehensive Python application for scraping sequential web content, converting it to EPUB format, and distributing it via email.

## Overview

This project automates the process of extracting chapters or sequential content from websites, organizing them into a structured eBook, and optionally sending the eBook to a specified email address (such as Amazon Kindle).

## Important Disclaimer

**This tool is provided for educational and personal use only.** Users are solely responsible for ensuring their use complies with applicable laws and website terms of service. Many websites prohibit automated scraping in their terms of service and robots.txt files. 

The developer assumes no liability for misuse of this software. Before scraping any website, you must:

1. Review the target website's Terms of Service and robots.txt file
2. Obtain explicit permission from the website owner if required
3. Ensure your use complies with applicable laws (CFAA, GDPR, etc.)
4. Understand that ignoring crawling policies may result in legal action

**Use this tool responsibly and only on websites you own or have explicit permission to scrape.**

## Features

- **Web Scraping**: Extracts sequential content from websites using Playwright browser automation
- **EPUB Generation**: Converts scraped text content into eBook format with metadata
- **Email Distribution**: Sends generated eBooks via SMTP (compatible with Amazon Kindle email addresses)
- **Configuration Management**: Stores email credentials for reuse
- **User-Friendly Interface**: Interactive command-line interface

## What This Tool Does

The application consists of three main components:

1. **Scraper** - Extracts text content from a series of web pages
2. **EPUB Converter** - Packages the extracted text into an eBook file
3. **Email Sender** - Delivers the eBook to an email address

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone or download the project to your desired location.

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browser files:
   ```bash
   playwright install
   ```

## Configuration

### Email Configuration

The application stores email credentials in `email_config.json` for convenient reuse. The file structure is as follows:

```json
{
  "sender_email": "your.email@gmail.com",
  "sender_password": "your_app_password",
  "recipient_email": "your.kindle@kindle.com",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

**Note**: For Gmail accounts, you must generate an application-specific password rather than using your main account password.

## Usage

### Running the Application

Execute the main program:

```bash
python main.py
```

### Interactive Workflow

The application will prompt you for the following information:

1. **Start URL**: The URL of the first chapter or page to scrape
2. **End URL**: The URL of the final chapter or page to scrape
3. **Book Name**: The title for the generated eBook
4. **Author Name**: The author name to include in eBook metadata
5. **Book Language**: The language code (e.g., 'en' for English, 'it' for Italian)
6. **Email Distribution**: Confirmation to send the EPUB via email (optional)

### Example Usage

```
Enter start URL: https://example.com/chapter-1
Enter end URL: https://example.com/chapter-50
Enter book name: My Novel
Enter author name: John Doe
Enter book language: en
Do you want to send the EPUB via email? (y/n): y
```

## Dependencies

Required packages are listed in `requirements.txt` and can be installed with:

```bash
pip install -r requirements.txt
```

## Output

### Generated Files

- **EPUB Files**: Saved in the `epubs/` directory with metadata embedded
- **Temporary Text Files**: Stored in the `temp/` directory during processing
- **Configuration File**: `email_config.json` stores email settings for future use

## Security & Legal Considerations

- Email credentials are stored in `email_config.json` - ensure this file is not shared or committed to version control
- For Gmail accounts, use application-specific passwords instead of your main password
- **You are responsible for ensuring your use of this tool complies with all applicable laws and website policies**
- Do not use this tool to bypass security measures or access protected content without permission
- Unauthorized scraping may violate the Computer Fraud and Abuse Act (CFAA) or similar legislation in your jurisdiction

## Troubleshooting

### Common Issues

**Issue**: Playwright browser fails to launch
- **Solution**: Run `playwright install` to download required browser binaries

**Issue**: Email sending fails with authentication error
- **Solution**: Verify Gmail credentials and confirm application-specific password is used

**Issue**: No email is received and the epub is not uploaded on Amazon Kindle
- **Solution**: Make sure the sender email is listed among allowed adresses for your Amazon account

## License & Liability

This project is provided as-is for educational purposes only. The author assumes no responsibility for any misuse, legal issues, or damages resulting from the use of this software. Users are solely liable for their actions and must ensure compliance with all applicable laws and website terms of service.
