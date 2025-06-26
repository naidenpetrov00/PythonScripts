from pandas import Series
import readData


class BlankFields:
    RECEIVER_GENERAL_INFO = "reciever_genral_info"
    ADDRESS = "address"
    CITY = "city"
    SENDER = "sender"
    SENDER_ADDRESS = "sender_address"
    SENDER_CITY = "sender_city"
    DOCUMENT_NUMBER = "document_number"

    def __init__(self) -> None:
        self.sender = "ЧСИ - Неделчо Митев рег.№ 841 тел.: 0700 20 841"
        self.sender_address = "1000 София бул.Княз Александър Дондуков №:11"
        self.sender_city = "София"

    def getFieldValues(self, row: Series, prev_row_doc_number=None):
        current_doc = row[readData.documentNumber]
        out_date = row[readData.outDate].split("/")[-1]
        document_number = f"*{out_date}-{current_doc}*"

        if prev_row_doc_number is None:
            doc_info = f"{current_doc}"
        else:
            doc_info = f"{prev_row_doc_number}, {current_doc}"
        generalInfo = f"{row[readData.recieverProp]} \nУдостоверявам, че получих документ(и) с изх№: {doc_info} ИД {row[readData.caseNumberProp]}"

        return {
            self.RECEIVER_GENERAL_INFO: generalInfo,
            self.ADDRESS: row[readData.adressProp],
            self.SENDER: self.sender,
            self.SENDER_ADDRESS: self.sender_address,
            self.SENDER_CITY: self.sender_city,
            self.DOCUMENT_NUMBER: document_number,
        }
