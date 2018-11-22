import re

from uhlcs_data.datatypes.text import ProcessedTextFiles, ProcessedTextFile
from uhlcs_data.utils.extractdocx import get_docx_text_from_content

only_numbers_re = re.compile(r"^[0-9]+$", re.MULTILINE)


class TextFromMSWordFile(ProcessedTextFile):
    def data_to_text(self, data):
        text = get_docx_text_from_content(data)
        return super(TextFromMSWordFile, self).data_to_text(text)


class MSWordFiles(ProcessedTextFiles):
    datatype_name = "text_from_msword"
    data_point_type = TextFromMSWordFile
