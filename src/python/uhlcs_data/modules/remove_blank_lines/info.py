"""
Filter out blank lines from text docs.

Blank lines are treated as paragraph breaks. Line breaks within pars are removed and we ensure that there's a
single space between the end of one line and the start of the next.

Any remaining blank lines are removed.

"""
from pimlico.core.modules.map import DocumentMapModuleInfo
from pimlico.datatypes.documents import RawTextDocumentType
from pimlico.datatypes.tar import TarredCorpusType, tarred_corpus_with_data_point_type, TarredCorpusWriter


class ModuleInfo(DocumentMapModuleInfo):
    module_type_name = "remove_blank_lines"
    module_readable_name = "Remove blank lines"
    module_inputs = [
        ("text", TarredCorpusType(RawTextDocumentType)),
    ]
    module_outputs = [
        ("text", tarred_corpus_with_data_point_type(RawTextDocumentType)),
    ]
    module_options = {}

    def get_writer(self, output_name, output_dir, append=False):
        return TarredCorpusWriter(self.get_absolute_output_dir("text"), encoding="utf8", append=append)

