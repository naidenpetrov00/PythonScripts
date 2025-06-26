import datetime as date
from pandas import Series
import pandas as pd
from blankField import BlankFields
from readData import readExcelFiles
from PyPDF2 import PdfReader, PdfWriter
import readData
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--mode",
    choices=["single", "pair"],
    help="Notise per row or notice per pair by case number",
)
args = parser.parse_args()

blank_path = "./blanks/243_form.pdf"
output_folder = "./notices"

today_date = date.datetime.today().strftime("%d.%m.%Y")


blank_fields = BlankFields()

files = readExcelFiles()

number = "Товарителница"
date_prop = "Дата"
results_df = pd.DataFrame(
    columns=[
        readData.recieverProp,
        readData.adressProp,
        number,
        readData.sender,
        date_prop,
        readData.outDate,
    ]
)
results_df.loc[1, readData.sender] = blank_fields.sender
results_df.loc[1, date_prop] = today_date


def updateTable(row: Series):
    global results_df
    results_df = pd.concat(
        [
            results_df,
            pd.DataFrame(
                [
                    {
                        readData.recieverProp: row[readData.recieverProp],
                        readData.adressProp: row[readData.adressProp].split(";")[0],
                    }
                ]
            ),
        ],
        ignore_index=True,
    )


prev_row_doc_number = None

for file_df in files:
    for i, (index, row) in enumerate(file_df.iterrows()):
        blank = PdfReader(blank_path)
        output_pdf = PdfWriter()
        page = blank.pages[0]
        output_pdf.add_page(blank.pages[0])
        output_path = f"{output_folder}/{index}_{row[readData.caseNumberProp]}.pdf"

        if args.mode == "pair":
            if i % 2 == 0:
                prev_row_doc_number = row[readData.documentNumber]
            else:
                output_pdf.update_page_form_field_values(
                    output_pdf.pages[0],
                    blank_fields.getFieldValues(row, prev_row_doc_number),
                )
                updateTable(row)

                with open(output_path, "wb") as f:
                    output_pdf.write(f)

        elif args.mode == "single":
            output_pdf.update_page_form_field_values(
                output_pdf.pages[0], blank_fields.getFieldValues(row)
            )
            updateTable(row)

            with open(output_path, "wb") as f:
                output_pdf.write(f)


results_df.to_excel(f"{output_folder}/noticesTable{today_date}.xlsx", index=False)
