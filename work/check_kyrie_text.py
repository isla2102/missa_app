from pypdf import PdfReader
s=PdfReader('output/pdf/kyrie-reengraved.pdf').pages[0].extract_text();print(repr(s[:600]))
