import requests
import fitz  # PyMuPDF
import os
import time
import hashlib
import threading
import signal
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from io import BytesIO

# Create a dedicated folder for PDF storage
PDF_STORAGE_DIR = "pdf_storage"
os.makedirs(PDF_STORAGE_DIR, exist_ok=True)

def is_pdf_url(url):
    """Check if a URL points to a PDF file."""
    return url.lower().endswith(".pdf") or "pdf" in url.lower()

def process_pdf_url(url, keep_file=False):
    """
    Process a PDF URL with better timeout handling to prevent page refreshes.
    Downloads the PDF into memory and extracts text without saving to disk.
    
    Args:
        url (str): The URL of the PDF to process
        keep_file (bool): Not used - we process in memory
        
    Returns:
        str: The extracted text or an error message
    """
    print(f"[INFO] Processing PDF from: {url}")
    
    try:
        # Use a short timeout for the initial connection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/pdf,*/*'
        }
        
        # Set a tight timeout to prevent hanging
        response = requests.get(url, headers=headers, stream=True, timeout=5)
        response.raise_for_status()
        
        # Check if it's actually a PDF
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' not in content_type and not url.lower().endswith('.pdf'):
            return f"[Not a PDF: {content_type}]"
        
        # Read the PDF into memory with size limit (10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        pdf_data = BytesIO()
        total_size = 0
        
        for chunk in response.iter_content(chunk_size=8192):
            total_size += len(chunk)
            if total_size > max_size:
                return "[PDF too large - extraction skipped]"
            pdf_data.write(chunk)
        
        pdf_data.seek(0)
        
        # Use a ThreadPoolExecutor with timeout to prevent hanging during extraction
        with ThreadPoolExecutor(max_workers=1) as executor:
            # Submit the extraction task
            future = executor.submit(extract_pdf_from_memory, pdf_data)
            
            try:
                # Wait for a maximum of 15 seconds
                result = future.result(timeout=15)
                
                # Truncate text if it's too long
                if len(result) > 50000:
                    return result[:50000] + "... [text truncated due to length]"
                    
                return result
            except TimeoutError:
                return "[PDF processing timeout - extraction aborted]"
            
    except requests.exceptions.Timeout:
        return "[Connection timeout while downloading PDF]"
    except requests.exceptions.RequestException as e:
        return f"[Network error: {str(e)}]"
    except Exception as e:
        return f"[PDF processing error: {str(e)}]"

def extract_pdf_from_memory(pdf_data):
    """Extract text from a PDF file in memory."""
    try:
        # Open the PDF from memory buffer
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        
        # Extract text with a reasonable limit
        text = ""
        max_pages = min(50, doc.page_count)  # Limit to 50 pages
        
        for i in range(max_pages):
            page = doc[i]
            text += page.get_text()
            
            # Add a note if we're limiting pages
            if i+1 == max_pages and max_pages < doc.page_count:
                text += f"\n\n[Note: Only showing first {max_pages} of {doc.page_count} pages]"
                
        doc.close()
        return text
    except Exception as e:
        return f"[PDF extraction error: {str(e)}]"

# The following functions are maintained for compatibility
def get_pdf_filename(url):
    """Generate a unique filename based on the URL (not used)"""
    return None

def download_pdf(url, max_size_mb=10):
    """Not used - processing happens in memory"""
    return None

def extract_pdf_text(pdf_path):
    """Not used - processing happens in memory"""
    return None

def get_stored_pdfs():
    """Get a list of all PDFs in the storage folder"""
    return []

def clean_old_pdfs(max_age_days=7):
    """Remove PDFs older than the specified number of days"""
    pass
