import argparse
import sys
from parser import Parser
from output_document import OutputDocument
import layouts


def main():
    arguments_parser = argparse.ArgumentParser(
        description="Convert .lyx files to .html files.")
    arguments_parser.add_argument("input_file",
                                  type=str,
                                  help="path to a valid .lyx file")
    arguments_parser.add_argument(
        "output_file",
        type=str,
        help="where to store the resulting .html file")

    arguments = arguments_parser.parse_args(sys.argv[1:])
    parse_file(arguments.input_file, arguments.output_file)


def parse_file(infile_path, outfile_path):
    outfile = OutputDocument(outfile_path)
    outfile.write("<!DOCTYPE html>")
    outfile.write("<html>\n")
    write_head(outfile)
    parser = Parser(infile_path)
    while parser.next() != "\\begin_body\n":
        parser.advance()
    parser.advance()
    parse_body(parser, outfile)
    outfile.write("</html>")
    outfile.close()


def write_head(outfile):
    outfile.write("<head>\n")
    outfile.write('<meta http-equiv="Content-type" '
                  'content="text/html;charset=UTF-8"/>\n')
    outfile.write(
        """
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="katex.min.css">
<!-- The loading of KaTeX is deferred to speed up page rendering -->
<script type='text/javascript' src="katex.min.js"></script>
"""
    )
    outfile.write("""
<style type="text/css">

h1.title {
    text-align: center;
}

div.lyx-code {
  font-family: Menlo, Monaco, "Courier New", monospace;
  background-color: #eaeaea;
  padding: 20px;
  border-radius: 15px;
}

hr.plain {
  border: 1px dotted #AFAFAF;
}


</style>
""")
    outfile.write('</head\n>')


def parse_body(parser, outfile):
    """
    parses the body of the document, from \\begin_body to \\end_body
    :param parser:
    :param outfile:
    :return:
    """
    assert parser.current() == "\\begin_body\n"
    outfile.write('<body dir="auto">\n')
    outfile.write(
        '<div dir="auto" style="min-width: 200px; max-width: 960px;'
        'margin: 0 auto;">\n')
    parser.advance()
    parse_multiple_text_layouts(parser, outfile)
    assert parser.current() == "\\end_body\n"
    parser.advance()
    outfile.write('</div>\n')
    outfile.write("</body>\n")


def parse_multiple_text_layouts(parser, outfile):
    while parser.current_command() == "\\begin_layout":
        layouts.parse_begin_layout(parser, outfile)


if __name__ == "__main__":
    main()
