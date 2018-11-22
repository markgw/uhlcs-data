import re

from pimlico.core.modules.map import skip_invalid
from pimlico.core.modules.map.multiproc import multiprocessing_executor_factory


unpunctuated_pars_re = re.compile(ur"""(?P<par_end>[^!"#$'()*.:;?`\n])(?P<rest>\s*(^\s*$)+)""", re.MULTILINE)


@skip_invalid
def process_document(worker, archive_name, doc_name, doc):
    return unpunctuated_pars_re.sub(ur"\g<par_end>.\g<rest>", doc)


ModuleExecutor = multiprocessing_executor_factory(process_document)
