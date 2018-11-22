# coding=utf-8
import os
import re
from subprocess import Popen, PIPE

from pimlico.core.modules.options import str_to_bool, comma_separated_strings
from pimlico.datatypes.documents import RawTextDocumentType
from pimlico.datatypes.files import UnnamedFileCollection

initial_numbers_re = re.compile(r"^([0-9\.]+ )+", re.MULTILINE)

verse_footnote_intro = re.compile(r"^\s*\*\s+[0-9]+:[0-9]+\s+", re.MULTILINE)
verse_no_space_line_start_re = re.compile(r"^[0-9\-]+\s*(?!:)", re.MULTILINE)
verse_no_space_after_space_re = re.compile(r"\s[0-9\-]+[^:]\s*", re.MULTILINE)

final_numbers_re = re.compile(r"[0-9]+$", re.MULTILINE)

only_numbers_re = re.compile(ur"^[0-9–\-]+$", re.MULTILINE)

colon_footnotes_re = re.compile(r"^:[0-9,\-]+\s.*$", re.MULTILINE)
bracket_footnotes_re = re.compile(r"^[0-9,\-]+\)\s.*$", re.MULTILINE)
star_footnotes_re = re.compile(r"^\*+\s+.*?\n\n", re.MULTILINE + re.DOTALL)

verse_only_lines_re = re.compile(ur"^[0-9–\-:\s]+$", re.MULTILINE)

multiple_blank_lines_re = re.compile(ur"(^\s*$){2,}", re.MULTILINE)

double_newlines_re = re.compile(ur"\n\n", re.MULTILINE)


class ProcessedTextFile(RawTextDocumentType):
    def data_to_text(self, data):
        """
        Takes raw data and produces unicode text.

        """
        utf8_conv_script = self.options.get("utf8_conv_script", None)
        if utf8_conv_script is not None:
            # -CO causes Perl to assume the output is utf8-encoded
            proc = Popen(["perl", "-CO", utf8_conv_script], stdin=PIPE, stdout=PIPE)
            # Pass in the data to run the conversion
            stdout, stderr = proc.communicate(data)
            return stdout.decode("utf8")
        elif self.options["encoding"] is not None:
            return data.decode(self.options["encoding"])
        else:
            return data

    def postprocess(self, data):
        """
        Applies all postprocessing, according to parameters specified in the options.

        """
        if self.options["strip_whitespace"]:
            data = u"\n".join(line.strip() for line in data.split(u"\n"))
        to_remove = [char.decode("unicode-escape") for char in self.options["remove"]]
        if to_remove:
            for char in to_remove:
                data = data.replace(char, u"")
        if self.options["double_newlines"]:
            # Replace all double newlines with singles. Important that this is applied before anything else that
            # involves line breaks
            data = double_newlines_re.sub(u"\n", data)
        if self.options["strip_initial_numbers"]:
            data = initial_numbers_re.sub(u"", data)
        if self.options["verse_footnotes"]:
            data = verse_footnote_intro.sub(u"\n", data)
        if self.options["colon_footnotes"]:
            data = colon_footnotes_re.sub(u"", data)
        if self.options["bracket_footnotes"]:
            data = bracket_footnotes_re.sub(u"", data)
        if self.options["star_footnotes"]:
            data = star_footnotes_re.sub(u"\n", data)
        if self.options["strip_final_numbers"]:
            data = final_numbers_re.sub(u"", data)
        if self.options["strip_only_numbers"]:
            data = only_numbers_re.sub(u"", data)
        if self.options["skip_bracketed_lines"]:
            data = u"\n".join(line for line in data.split(u"\n")
                              if not (len(line) > 2 and line[0] == u"(" and line[-1] == u")"))
        if self.options["verse_no_space"]:
            data = verse_no_space_line_start_re.sub(u"", data)
            data = verse_no_space_after_space_re.sub(u" ", data)
        if self.options["skip_verse_lines"]:
            data = verse_only_lines_re.sub(u"", data)
        if self.options["blank_lines_to_pars"]:
            # Split the data on double blank lines, separating pars
            pars = data.split(u"\n\n")
            # Strip linebreaks and remove empty pars, dealing with multiple blank lines
            pars = [par.strip(u"\n") for par in pars]
            pars = [par for par in pars if len(par)]
            # Remove all linebreaks from within pars, making sure there's one space where they were
            pars = [
                u" ".join(line.strip() for line in par.split(u"\n")) for par in pars
            ]
            # Join pars on a single linebreak
            data = u"\n".join(pars)
        elif self.options["skip_multiple_blank_lines"]:
            data = multiple_blank_lines_re.sub(u"", data)
        # If we're stripping whitespace, do so again at the end, after applying all other filters
        if self.options["strip_whitespace"]:
            data = u"\n".join(line.strip() for line in data.split(u"\n"))
        # Remove initial or final newlines, leaving just one at the end
        data = u"{}\n".format(data.strip(u"\n"))
        return data

    def process_document(self, doc):
        return self.postprocess(self.data_to_text(doc))


class ProcessedTextFiles(UnnamedFileCollection):
    data_point_type = ProcessedTextFile
    input_module_options = dict(UnnamedFileCollection.input_module_options, **{
        "utf8_conv_script": {
            "help": "Path to a Perl script to convert the raw bytes of the input files into utf-8 encoded "
                    "unicode. Each file will be passed through the script"
        },
        "encoding": {
            "help": "Encoding to assume for input files. This is ignored if utf8_conv_script is given. If neither "
                    "is given, the input is assumed to be plain ASCII text, or processed by some other postprocessing "
                    "function",
        },
        "strip_whitespace": {
            "help": "Remove whitespace from start and end of lines. (Default: True)",
            "default": True,
            "type": str_to_bool,
        },
        "strip_initial_numbers": {
            "help": "Remove any words at the start of a line that consist only of numeric digits and periods. "
                    "This is designed to get rid of verse numbers. (Default: False)",
            "default": False,
            "type": str_to_bool,
        },
        "strip_final_numbers": {
            "help": "Remove any numeric digits at the end of lines. This is designed to get rid of page numbers that "
                    "have got tacked onto the end of the last line. (Default: False)",
            "default": False,
            "type": str_to_bool,
        },
        "strip_only_numbers": {
            "help": "Remove any lines consisting only of numeric digits. This is designed to get rid of page numbers "
                    "on a line of their own. (Default: False)",
            "default": False,
            "type": str_to_bool,
        },
        "remove": {
            "help": "Comma-separated list of characters to strip out of the data. "
                    "May include Python unicode escape sequences ('\uXXXX')",
            "default": [],
            "type": comma_separated_strings,
        },
        "verse_footnotes": {
            "help": "A special notation that appears in some of these files introduces footnotes with a line starting "
                    "with a '*', a verse number, then the text. If verse_footnotes=T, the '*' and verse number "
                    "will be removed, a new paragraph started before the line (blank line inserted) and the rest of "
                    "the footnote text left",
            "type": str_to_bool,
        },
        "verse_no_space": {
            "help": "An annoying, but common, way to include bible verse numbers in the text is to just put them at "
                    "the start of the sentence. Particularly annoying is when there's no space after them. This "
                    "filter strips away any numeric digits occurring either at the start of a line or after a space",
            "type": str_to_bool,
        },
        "colon_footnotes": {
            "help": "One way to denote footnotes: ':X footnote', where X is a number. Remove the whole footnote "
                    "line",
            "type": str_to_bool,
        },
        "bracket_footnotes": {
            "help": "Another way to denote footnotes: 'X)  footnote', where X is a number. Remove the whole footnote "
                    "line",
            "type": str_to_bool,
        },
        "skip_bracketed_lines": {
            "help": "If a whole line is enclosed in parentheses, skip it. Some texts have references in parentheses, "
                    "which it's good to skip",
            "type": str_to_bool,
        },
        "star_footnotes": {
            "help": "Another way to denote footnotes: '* footnote'. Remove the whole footnote, up to the next blank "
                    "line. This assumes a blank_lines_to_pars style of par break and that the footnote occupies "
                    "the whole par. This is the case where this type of footnote has arisen",
            "type": str_to_bool,
        },
        "skip_verse_lines": {
            "help": "For some reason, even after all other filters, we end up with some lines that are just a "
                    "chapter-verse number, or range. Skip any lines that consist only of numbers, colons, hyphens "
                    "and whitespace",
            "type": str_to_bool,
        },
        "double_newlines": {
            "help": "Assume the file has all its newlines doubled and replace all double linebreaks with singles. "
                    "This is applied before all other blank line processing, so things like blank_lines_to_pars "
                    "can still be applied after removing the doubling",
            "type": str_to_bool,
        },
        "blank_lines_to_pars": {
            "help": "Take blank lines to indicate par breaks, remove linebreaks within pars and remove all blank lines",
            "type": str_to_bool,
        },
        "skip_multiple_blank_lines": {
            "help": "Allow only single blank lines. If there are more in a row, reduce to one. Note that there's no "
                    "need to use this together with blank_lines_to_pars, since it does this anyway",
            "type": str_to_bool,
        },
    })

    def path_name_to_doc_name(self, path):
        # Remove extension and replace with ".txt"
        basename = os.path.splitext(os.path.basename(path))[0]
        return u"%s%stxt" % (basename, os.path.extsep)
