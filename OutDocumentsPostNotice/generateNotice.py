from readData import readExcelFiles
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, BooleanObject
from typing import Any, List


from blankFieldProps import BlankFieldProps

blank_path = "./blanks/243_formC.pdf"

files = readExcelFiles()

field_values = {
    BlankFieldProps.RECEIVER_GENERAL_INFO: "Основна информация",
    BlankFieldProps.ADDRESS: "ул. Иван Вазов 10",
    BlankFieldProps.CITY: "София",
    BlankFieldProps.SENDER: "Кантора ЧСИ",
    BlankFieldProps.SENDER_ADDRESS: "бул. България 50",
    BlankFieldProps.SENDER_CITY: "Пловдив",
    "Test Required": "Test"
}

for file_df in files:
    # for index, row in file_df.iterrows():
    blank = PdfReader(blank_path)
    output_pdf = PdfWriter()

    page = blank.pages[0]
    output_pdf.add_page(blank.pages[0])
    output_pdf.update_page_form_field_values(output_pdf.pages[0], field_values)

    fields = blank.get_form_text_fields()
    print(fields)

    with open(f"notices/output{0}.pdf", "wb") as f:
        output_pdf.write(f)
