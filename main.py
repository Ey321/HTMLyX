import argparse
import sys
from parser import Parser
from output_document import OutputDocument
import layouts
import insets


def main():
    arguments_parser = argparse.ArgumentParser(
        description="Convert .lyx files to .html files.")
    arguments_parser.add_argument("input_file",
                                  type=str,
                                  help="path to a valid .lyx file")
    arguments_parser.add_argument("-s", "--split", action="store_true",
                                  help="split document every part to avoid large files which are difficult to "
                                  "render.")
    arguments_parser.add_argument(
        "output_file",
        type=str,
        help="where to store the resulting .html file")

    arguments = arguments_parser.parse_args(sys.argv[1:])
    parse_file(arguments.input_file, arguments.output_file, arguments.split)
    insets.katex_macros = ""
    parse_file(arguments.input_file, arguments.output_file, arguments.split)


def parse_file(infile_path, outfile_path, split):
    outfile = OutputDocument(outfile_path)
    parser = Parser(infile_path)
    parser.advance()
    while parser.next() != "\\begin_body\n":
        if parser.current_command() == "\\language":
            parser.default_language = parser.current_parameters()[0]
        parser.advance()
    parser.advance()
    parse_body(parser, outfile, split)
    outfile.close()


def write_body_begin(outfile):
    outfile.write('<body dir="auto">\n')
    outfile.write(
        '<div dir="auto" style="min-width: 200px; max-width: 960px;'
        'margin: 0 auto;">\n')


def write_body_end(outfile):
    outfile.write('</div>\n')
    outfile.write("</body>\n")


def parse_body(parser, outfile, split: bool):
    """
    parses the body of the document, from \\begin_body to \\end_body
    :param parser:
    :param outfile:
    :param split:
    :return:
    """
    assert parser.current() == "\\begin_body\n"
    write_body_begin(outfile)
    parser.advance()
    parse_multiple_text_layouts(parser, outfile, split)
    assert parser.current() == "\\end_body\n"
    parser.advance()
    write_body_end(outfile)


def parse_multiple_text_layouts(parser, outfile, split: bool = False):
    while parser.current_command() == "\\begin_layout":
        if parser.current_parameters()[0] == layouts.PART_LAYOUT and split:
            write_body_end(outfile)
            outfile.new_file()
            write_body_begin(outfile)
        layouts.parse_begin_layout(parser, outfile)


if __name__ == "__main__":
    main()
