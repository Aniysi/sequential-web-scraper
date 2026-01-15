from scraper import WebScraper
from epub_converter import EpubConverter
from email_sender import EmailSender

if __name__ == "__main__":
    start_url = input("Enter start URL: ").strip()
    end_url = input("Enter end URL: ").strip()
    
    if not start_url or not end_url:
        print("Start URL or end URL not provided.")
        exit(1)


    book_title = input("Enter book name: ")
    author = input("Enter author name: ")
    language = input("Enter book language: ")


    send_email = input("\nDo you want to send the EPUB via email? (y/n): ").strip().lower()

    scraper = WebScraper(start_url, end_url)
    print("Starting scraping...")
    path = scraper.scrape()


    converter = EpubConverter(folder_path=path, author=author, language=language, book_title=book_title)
    filename = converter.create_epub()

        
    if send_email == 'y':
        email_sender = EmailSender()
            
        sender_email, sender_password, recipient_email = email_sender.get_credentials()
            
        success = email_sender.send_epub(
            epub_file=filename,
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=recipient_email,
            subject=f"EPUB: {converter.get_title()}",
            body="Here is your scraped EPUB book."
        )
            
        if not success:
            print("\n⚠️  Email sending failed, but EPUB file is saved locally.")