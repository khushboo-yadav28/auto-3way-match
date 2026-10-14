import re
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
import PyPDF2


def extract_text_from_pdf(pdf_path):
  """Reads raw text from the downloaded PDF and normalizes/translates it into

  English to support multilingual vendor invoices with rate-limit resilience.
  """
  text = ''
  try:
    with open(pdf_path, 'rb') as file:
      reader = PyPDF2.PdfReader(file)
      for page in reader.pages:
        text += page.extract_text() + '\n'

    # Multilingual Normalization
    try:
      translated_text = GoogleTranslator(
          source='auto', target='english'
      ).translate(text)
      if translated_text and translated_text.strip():
        print(
            '[INFO] Multilingual Engine: Invoice text successfully normalized'
            ' to English.'
        )
        text = translated_text
    except TooManyRequests:
      print(
          '[WARNING] Translation rate limit hit. Falling back to native'
          ' bilingual regex extraction.'
      )
    except Exception as trans_err:
      print(f'[WARNING] Translation skipped: {trans_err}. Using native regex.')

    return text
  except Exception as e:
    print(f'Error reading PDF: {e}')
    return ''


def extract_invoice_data(text):
  """Extracts structured data using regex patterns that flexibly handle

  mixed-language parenthetical labels (e.g., 'चालान संख्या (Invoice ID):').
  """
  data = {
      'invoice_id': None,
      'vendor_name': None,
      'item_quantities': None,
      'unit_pricing': None,
      'total_amount': None,
  }

  # Matches Vendor / From / विक्रेता / વેન્ડર (allowing optional parentheses before colon)
  vendor_match = re.search(
      r'(?:Vendor|From|विक्रेता|वेન્ડર)(?:\s*\(.*?\))?\s*:\s*(.+)',
      text,
      re.IGNORECASE,
  )
  if vendor_match:
    data['vendor_name'] = vendor_match.group(1).strip()

  # Matches Invoice ID / चालान संख्या
  id_match = re.search(
      r'(?:Invoice\s*(?:ID|#|Number)?|चालान\s*संख्या|ઇનવોઇસ\s*નંਬਰ)(?:\s*\(.*?\))?\s*:\s*([\w-]+)',
      text,
      re.IGNORECASE,
  )
  if id_match:
    data['invoice_id'] = id_match.group(1).strip()

  # Matches Qty / मात्रा
  qty_match = re.search(
      r'(?:Qty|Quantity|Quantities|मात्रा|જથ્થो)(?:\s*\(.*?\))?\s*:\s*(\d+)|(\d+)\s*x',
      text,
      re.IGNORECASE,
  )
  if qty_match:
    data['item_quantities'] = int(qty_match.group(1) or qty_match.group(2))

  # Matches Unit Price / यूनिट कीमत
  price_match = re.search(
      r'(?:at|Price|Unit Price|Unit Pricing|यूनिट\s*कीमत|એકમ\s*કિંમત)(?:\s*\(.*?\))?\s*:?\s*\$?\s*([\d,\.]+)',
      text,
      re.IGNORECASE,
  )
  if price_match:
    data['unit_pricing'] = float(price_match.group(1).replace(',', ''))

  # Matches Total Amount / कुल राशि
  total_match = re.search(
      r'(?:Total(?: Amount)?|Amount Due|कुल\s*राशि|કુલ\s*રકમ)(?:\s*\(.*?\))?\s*:?\s*\$?\s*([\d,\.]+)',
      text,
      re.IGNORECASE,
  )
  if total_match:
    data['total_amount'] = float(total_match.group(1).replace(',', ''))

  return data