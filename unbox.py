#!/usr/bin/env python3
"""
unbox - extract readable conversation from mbox/email files
Reads from stdin, writes to stdout
"""
import sys
import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import re
from io import BytesIO
from mailbox import mbox
import tempfile
import os

from bs4 import BeautifulSoup


def html_to_text(html_content):
    """Convert HTML to readable plain text"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text and clean up whitespace
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def get_email_body(msg):
    """Extract the best available body content from email"""
    body = ""
    attachments = []
    
    if msg.is_multipart():
        # Walk through all parts
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            # Track attachments
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    attachments.append(filename)
                continue
            
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    # Continue to collect attachments but prefer plain text
                    if not attachments:
                        for p in msg.walk():
                            if "attachment" in str(p.get("Content-Disposition", "")):
                                fn = p.get_filename()
                                if fn:
                                    attachments.append(fn)
                        break
                except:
                    pass
            
            elif content_type == "text/html" and not body:
                try:
                    html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    body = html_to_text(html_content)
                except:
                    pass
    else:
        # Not multipart
        content_type = msg.get_content_type()
        try:
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_type == "text/html":
                html_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                body = html_to_text(html_content)
        except:
            body = str(msg.get_payload())
    
    return body.strip(), attachments


def clean_email_address(addr):
    """Clean up email address formatting"""
    if not addr:
        return ""
    # Remove extra whitespace and clean up formatting
    return ' '.join(addr.split())


def format_date(date_str):
    """Format date string with timezone preserved"""
    if not date_str:
        return ""
    try:
        dt = parsedate_to_datetime(date_str)
        # Format with timezone
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z').strip()
    except:
        # If parsing fails, return original
        return date_str


def process_email(msg):
    """Process a single email message and return formatted output"""
    # Extract headers
    from_addr = clean_email_address(msg.get('From', ''))
    to_addr = clean_email_address(msg.get('To', ''))
    cc_addr = clean_email_address(msg.get('Cc', ''))
    bcc_addr = clean_email_address(msg.get('Bcc', ''))
    subject = msg.get('Subject', '(No Subject)')
    date = msg.get('Date', '')
    
    # Get body and attachments
    body, attachments = get_email_body(msg)
    
    # Format output
    output = []
    output.append(f"From: {from_addr}")
    output.append(f"To: {to_addr}")
    if cc_addr:
        output.append(f"CC: {cc_addr}")
    if bcc_addr:
        output.append(f"BCC: {bcc_addr}")
    output.append(f"Subject: {subject}")
    if date:
        formatted_date = format_date(date)
        output.append(f"Date: {formatted_date}")
    if attachments:
        output.append(f"Attachments: {', '.join(attachments)}")
    output.append("")  # Blank line before body
    output.append(body)
    
    return '\n'.join(output)


def process_mbox_from_stdin():
    """Process mbox data from stdin"""
    # mbox requires a file-like object, so we need to use a temp file
    # Read all stdin into a temporary file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(sys.stdin.buffer.read())
    
    try:
        box = mbox(tmp_path)
        emails = []
        
        for message in box:
            emails.append(process_email(message))
        
        print(f"Processed {len(emails)} email(s)", file=sys.stderr)
        
        # Join with separator
        separator = '\n\n' + '='*60 + '\n\n'
        return separator.join(emails)
    except Exception as e:
        print(f"Error processing mbox data: {e}", file=sys.stderr)
        return None
    finally:
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass


def process_single_email_from_stdin():
    """Process a single email message from stdin"""
    try:
        msg = BytesParser(policy=policy.default).parse(sys.stdin.buffer)
        return process_email(msg)
    except Exception as e:
        print(f"Error processing email data: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("unbox - Extract readable conversation from mbox/email files")
        print("\nUsage:")
        print("  cat emails.mbox | unbox > output.txt")
        print("  cat single_email.eml | unbox > output.txt")
        print("\nDescription:")
        print("  Reads email data from stdin and writes cleaned, human-readable output to stdout.")
        print("  Supports both mbox format (multiple emails) and single email files (.eml).")
        print("\nFeatures:")
        print("  • Converts HTML emails to plain text")
        print("  • Preserves timezone information in dates")
        print("  • Lists attachments (without extracting them)")
        print("  • Extracts From, To, CC, BCC, Subject, and Date headers")
        print("  • Status messages and errors go to stderr")
        print("\nExamples:")
        print("  # Process an mbox file")
        print("  cat archive.mbox | unbox > readable.txt")
        print()
        print("  # Process a single email")
        print("  cat message.eml | unbox > message.txt")
        print()
        print("  # Pipe from other tools")
        print("  fetchmail | unbox > today.txt")
        print("\nRequirements:")
        print("  • Python 3.6+")
        print("  • beautifulsoup4 (install: pip install beautifulsoup4)")
        sys.exit(0)
    
    # Read first line to detect format
    first_line = sys.stdin.buffer.peek(512)[:512]
    
    # Reset to beginning by reading into buffer
    stdin_data = sys.stdin.buffer.read()
    
    # Determine if mbox or single email
    if stdin_data.startswith(b'From '):
        # Write data back for mbox processing
        sys.stdin = open('/dev/stdin', 'rb')
        # Use temp file approach
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(stdin_data)
        
        try:
            box = mbox(tmp_path)
            emails = []
            
            for message in box:
                emails.append(process_email(message))
            
            print(f"Processed {len(emails)} email(s)", file=sys.stderr)
            
            # Join with separator and output
            separator = '\n\n' + '='*60 + '\n\n'
            result = separator.join(emails)
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass
    else:
        # Single email
        msg = BytesParser(policy=policy.default).parsebytes(stdin_data)
        result = process_email(msg)
    
    if result:
        print(result)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
