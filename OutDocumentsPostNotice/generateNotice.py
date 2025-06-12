from pandas import Series
from readData import readExcelFiles
from PyPDF2 import PdfReader, PdfWriter
import readData

from blankFieldProps import BlankFieldProps

blank_path = "./blanks/243_form.pdf"

files = readExcelFiles()

sender = "ЧСИ - Неделчо Митев рег.№ 841 тел.: 0700 20 841"
sender_address = "1000 София БУЛ. Витоша N:17"
sender_city = "София"


def getFieldValues(row: Series):
    generalInfo = f"{row[readData.recieverProp]} \nУдостоверявам, че получих документ(и) с изх№: {row[readData.documentNumber]} ИД {row[readData.caseNumberProp]}"
    return {
        BlankFieldProps.RECEIVER_GENERAL_INFO: generalInfo,
        BlankFieldProps.ADDRESS: row[readData.adressProp],
        # BlankFieldProps.CITY: "София",
        BlankFieldProps.SENDER: sender,
        BlankFieldProps.SENDER_ADDRESS: sender_address,
        BlankFieldProps.SENDER_CITY: sender_city,
    }


for file_df in files:
    for index, row in file_df.iterrows():
        blank = PdfReader(blank_path)
        output_pdf = PdfWriter()

        page = blank.pages[0]
        output_pdf.add_page(blank.pages[0])
        output_pdf.update_page_form_field_values(
            output_pdf.pages[0], getFieldValues(row)
        )

        output_path = f"notices/output{index}.pdf"

        with open(output_path, "wb") as f:
            output_pdf.write(f)
