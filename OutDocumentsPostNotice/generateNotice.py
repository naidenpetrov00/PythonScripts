import datetime as date
import os
from pandas import Series
import pandas as pd
from readData import readExcelFiles
from PyPDF2 import PdfReader, PdfWriter
import readData

from blankFieldProps import BlankFieldProps

blank_path = "./blanks/243_form.pdf"
output_folder = "./notices"
sender = "ЧСИ - Неделчо Митев рег.№ 841 тел.: 0700 20 841"
sender_address = "1000 София бул.Княз Александър Дондуков №:11"
sender_city = "София"
date_prop = "Дата"
today_date = date.datetime.today().strftime("%d.%m.%Y")


files = readExcelFiles()
results_df = pd.DataFrame(
    columns=[readData.recieverProp, readData.adressProp, readData.sender, date_prop]
)
results_df.loc[1, readData.sender] = sender
results_df.loc[1, date_prop] = today_date


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


table_path = "./blanks/table_blank.xlsx"

pd.set_option("display.max_colwidth", 50)


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


for file_df in files:
    for index, row in file_df.iterrows():
        blank = PdfReader(blank_path)
        output_pdf = PdfWriter()

        page = blank.pages[0]
        output_pdf.add_page(blank.pages[0])
        output_pdf.update_page_form_field_values(
            output_pdf.pages[0], getFieldValues(row)
        )

        updateTable(row)

        output_path = f"{output_folder}/{index}_{row[readData.caseNumberProp]}.pdf"

        with open(output_path, "wb") as f:
            output_pdf.write(f)

results_df.to_excel(f"{output_folder}/noticesTable{today_date}.xlsx", index=False)
