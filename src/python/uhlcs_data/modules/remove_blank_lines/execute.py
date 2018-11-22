from pimlico.core.modules.map import skip_invalid
from pimlico.core.modules.map.multiproc import multiprocessing_executor_factory


@skip_invalid
def process_document(worker, archive_name, doc_name, doc):
    # Split the data on double blank lines, separating pars
    pars = doc.split(u"\n\n")
    # Strip linebreaks and remove empty pars, dealing with multiple blank lines
    pars = [par.strip(u"\n") for par in pars]
    pars = [par for par in pars if len(par)]
    # Remove all linebreaks from within pars, making sure there's one space where they were
    pars = [
        u" ".join(line.strip() for line in par.split(u"\n")) for par in pars
    ]
    # Join pars on a single linebreak
    return u"\n".join(pars)


ModuleExecutor = multiprocessing_executor_factory(process_document)
