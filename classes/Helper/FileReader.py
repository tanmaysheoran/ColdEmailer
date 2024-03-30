import fitz
import re


class FileReader:
    def __init__(self, file: bytes):
        self.file = file

    def convert_pdf_to_text(self):
        self.doc = "".join(
            [page.get_text() for page in fitz.open("pdf", self.file)])

    def process_pdf(self):
        text = self.doc
        # Regular expressions to match email addresses and phone numbers
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'

        # Find all email addresses and phone numbers in the text
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        # Remove email addresses and phone numbers from the text
        text_no_contacts = re.sub(email_pattern, '', text)
        text_no_contacts = re.sub(phone_pattern, '', text_no_contacts)

        # Create a dictionary to store email addresses, phone numbers, and cleaned text
        self.extracted_data = {
            "emails": emails,
            "phones": phones,
            "cleaned_text": text_no_contacts
        }

    def convert_and_extract(self):
        self.convert_pdf_to_text()
        self.process_pdf()
        return self.extracted_data
