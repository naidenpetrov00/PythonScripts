from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from readData import readExcelFiles, caseNumberProp

blank_path = "./blanks/243.pdf"

files = readExcelFiles()

for file_df in files:
    for index, row in file_df.iterrows():
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.drawString(100, 100, str(row[caseNumberProp]))

        c.save()
        packet.seek(0)

        blank = PdfReader(blank_path)
        overlay_pdf = PdfReader(packet)
        output_pdf = PdfWriter()

        page = blank.pages[0]
        page.merge_page(overlay_pdf.pages[0])
        output_pdf.add_page(page)

        with open(f"notices/output{index}.pdf", "wb") as f:
            output_pdf.write(f)
