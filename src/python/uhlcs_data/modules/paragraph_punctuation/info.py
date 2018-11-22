"""
If the input contains paragraphs (separated by blank lines) that do not have any punctuation at the end of them,
add full stops. This is useful for making sure titles, or badly formatted paragraphs, don't get run together
with the next sentence when the sentence detector is run.

"""
from pimlico.core.modules.map import DocumentMapModuleInfo
from pimlico.datatypes.documents import RawTextDocumentType
from pimlico.datatypes.tar import TarredCorpusType, TarredCorpusWriter, tarred_corpus_with_data_point_type


class ModuleInfo(DocumentMapModuleInfo):
    module_type_name = "paragraph_punctuation"
    module_readable_name = "Fix unpunctuated pars"
    module_inputs = [
        ("text", TarredCorpusType(RawTextDocumentType)),
    ]
    module_outputs = [
        ("text", tarred_corpus_with_data_point_type(RawTextDocumentType)),
    ]
    module_options = {}

    def get_writer(self, output_name, output_dir, append=False):
        return TarredCorpusWriter(output_dir, append=append)
