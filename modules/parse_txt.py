import os
from llama_index.core import SimpleDirectoryReader

class ParseTxt:
    """
    Parse text files using SimpleDirectoryReader and save the extracted text.
    """
    def __init__(self, loader_obj_dict='', txt_file_path=''):
        self.loader_obj_dict    = loader_obj_dict
        self.txt_file_path      = txt_file_path
    
    def ingestFormatConversion(self):
        if self.loader_obj_dict:
            data_dict = {}
            for document, loader_obj in self.loader_obj_dict.items():
                for doc in loader_obj:
                    page_number     = f"{document}_{doc.metadata.get("page_number")}" if doc.metadata.get("page_number") else f"{document}_1"
                    page_content    = doc.page_content
                    if page_number in data_dict.keys():
                        data_dict[page_number] = data_dict[page_number] + ' ' + page_content
                    else:
                        data_dict[page_number] = page_content
            return data_dict
    
    def ingestPlainTxt(self):
        if self.txt_file_path:
            document    = SimpleDirectoryReader(self.txt_file_path, filename_as_id=True).load_data()
            data_dict   = {}
            for doc in document:
                if doc.doc_id in data_dict.keys():
                    data_dict[doc.doc_id] = data_dict[doc.doc_id] + ' ' + doc.text
                else:
                    data_dict[doc.doc_id] = doc.text
            return data_dict