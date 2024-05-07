from typing import Optional, Union
from langchain.text_splitter import TextSplitter
from langchain_community.document_loaders import (
    UnstructuredURLLoader,
    PyPDFLoader,
    UnstructuredExcelLoader,
)
from core.files import save_url_to_local_file, delete_files
from core.constants import ResourceSources


class DocumentProcessor:
    def __init__(self, doc_type: str, splitter: Optional[TextSplitter] = None):
        self._doc_type = doc_type
        self._text_spliter = splitter

    def url_loader(self, urls):
        loader = UnstructuredURLLoader(urls=urls)
        return loader

    def pdf_loader(self, pdf_url):
        loader = PyPDFLoader(file_path=pdf_url)
        return loader

    def excel_loader(self, file_url):
        file_type, local_path = save_url_to_local_file(file_url)
        loader = UnstructuredExcelLoader(local_path, mode="elements")
        delete_files([local_path])  # Delete the downloaded file after use
        return loader

    def run_loader(self, url: Union[str, list]):
        if self._doc_type == ResourceSources.PDF.value:
            loader = self.pdf_loader(url)
        elif self._doc_type == ResourceSources.EXCEL.value:
            loader = self.excel_loader(url)
        elif self._doc_type == ResourceSources.URL.value:
            loader = self.url_loader(url)
        else:
            raise ValueError("Invalid document type.")

        if self._text_spliter is not None:
            data = loader.load_and_split(self._text_spliter)
        else:
            data = loader.load()

        return data
