
from PyPDF2 import PdfReader, PdfWriter


def create_single_page_pdf(input_path, output_path, page_index=0):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.add_page(reader.pages[page_index])
    with open(output_path, 'wb') as f:
        writer.write(f)

def write_to_pdf(writer, output_path):
    with open(output_path, 'wb') as f:
        writer.write(f)

