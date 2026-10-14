from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
from rpa_backend.extraction_engine import extract_invoice_data

# Sample invoice text in Hindi simulating a raw PDF extraction
sample_foreign_text = """
चालान संख्या (Invoice ID): INV-2026-HI99
विक्रेता (Vendor): Tech Solutions Corp
मात्रा (Quantity): 5
यूनिट कीमत (Unit Price): $150.00
कुल राशि (Total Amount): $750.00
"""

print('--- 1. Original Foreign Text ---')
print(sample_foreign_text)

# Translate to English with rate-limit safety check in the test script
try:
  translated = GoogleTranslator(source='auto', target='english').translate(
      sample_foreign_text
  )
  print('\n--- 2. Translated Normalized Text ---')
  print(translated)
except TooManyRequests:
  print(
      '\n[WARNING] Translation rate limit hit in test script. Using original'
      ' text as fallback.'
  )
  translated = sample_foreign_text

# Run through regex extraction
extracted_data = extract_invoice_data(translated)
print('\n--- 3. Final Extracted Structured Data ---')
print(extracted_data)