import argparse
import sys
from parser import Parser

TITLE_LAYOUT = "Title"
PART_LAYOUT = "Part"
STANDARD_LAYOUT = "Standard"

TEXT_LAYOUTS = {TITLE_LAYOUT, PART_LAYOUT, STANDARD_LAYOUT}

LAYOUT_TAGS = {
    TITLE_LAYOUT: 'h1 class="title"',
    PART_LAYOUT: 'h2 class="part"',
    STANDARD_LAYOUT: 'div class="standard"'
}

ENUMERATE_LAYOUT = "Enumerate"
ITEMIZE_LAYOUT = "Itemize"
ITEM_TAG = "li"
LIST_TAG = {
    ENUMERATE_LAYOUT: "ol",
    ITEMIZE_LAYOUT: "ul"
}

LIST_LAYOUTS = {ENUMERATE_LAYOUT, ITEMIZE_LAYOUT}

katex_elements_count = 0

styles = {"bar", "series"}


def main():
    arguments_parser = argparse.ArgumentParser(
        description="Convert .lyx file to .html files.")
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
    outfile = open(outfile_path, "w")
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
    while parser.current_command() != "\\end_body":
        if parser.current_command() == "\\begin_layout":
            parse_begin_layout(parser, outfile)
    assert parser.current() == "\\end_body\n"
    parser.advance()
    outfile.write('</div>\n')
    outfile.write("</body>\n")


def parse_begin_layout(parser, outfile):
    """parses a layout, from \\begin layout to \\end_layout."""
    assert parser.current_command() == "\\begin_layout"
    parameters = parser.current_parameters()
    assert len(parameters) == 1
    layout_type = parameters[0]
    if layout_type in TEXT_LAYOUTS:
        parse_text_layout(parser, outfile)


def parse_text_layout(parser, outfile):
    """parses a text layout, from \\begin layout to \\end_layout."""
    layout_type = parser.current_parameters()[0]
    outfile.write(f"<{LAYOUT_TAGS[layout_type]}>")
    parse_text(parser, outfile)
    assert parser.current_command() == "\\end_layout"
    outfile.write(f"</{LAYOUT_TAGS[layout_type].split()[0]}>\n")
    parser.advance()


def parse_list_layout(parser, outfile):
    """parses itemize and enumerate"""
    outfile.write(f"<{LIST_TAG}>")
    layout_type = parser.current_parameters()[0]
    # TODO


def parse_text(parser, outfile):
    """parses a text and its styles"""
    parser.advance()

    paragraph_styles = {
        "bar": "default",
        "series": "default"
    }

    outfile.write(f'<span style="{get_style(paragraph_styles)}">')
    style_changed = False
    while not parser.is_current_command() or \
            parser.current_command() != "\\end_layout":
        if not parser.is_current_command():
            if style_changed:
                outfile.write(
                    f'</span><span style="{get_style(paragraph_styles)}">')
                style_changed = False
            outfile.write(parser.current()[:-1])
            parser.advance()
        else:
            if parser.current_command() == "\\begin_inset":
                parse_inset(parser, outfile)
            elif parser.current_command()[1:] in styles:
                param = parser.current_parameters()[0]
                paragraph_styles[parser.current_command()[1:]] = param
                parser.advance()
                style_changed = True
            else:
                parser.advance()
    outfile.write('</span>')


def get_style(style_dict):
    out = ""
    if style_dict["bar"] == "under":
        out += 'text-decoration: underline; '
    elif style_dict["bar"] == "no":
        out += 'text-decoration: none;'

    if style_dict["series"] == "medium":
        out += 'font-weight: normal; '
    elif style_dict["series"] == "bold":
        out += 'font-weight: bold; '
    return out


def parse_inset(parser, outfile):
    """parses an inset"""
    assert parser.current_command() == "\\begin_inset"
    if parser.current_parameters()[0] == "Formula":
        if len(parser.current_parameters()) == 2:  # an inline formula
            latex_code = parser.current_parameters()[1]
            insert_formula(outfile, latex_code[1:-1])
            parser.advance()
        elif len(parser.current_parameters()) == 1:  # non inline formula
            latex_code = ""
            parser.advance()
            assert parser.current_command() == "\\["
            parser.advance()
            while parser.current_command() != "\\]":
                latex_code += parser.current()
                parser.advance()
            insert_big_formula(outfile, latex_code)
            parser.advance()
    assert parser.current_command() == "\\end_inset"
    parser.advance()
    return


def insert_formula(outfile, latex_code):
    global katex_elements_count
    ht = """
<div class="viewport" style="display: inline-block; overflow: auto; 
max-width: 80%; vertical-align: middle; margin-top: 0px;">
<p id="ktx_count_{ktx_count}" dir="ltr"
style="white-space: nowrap; overflow-x: auto; overflow-y: hidden; "/><script>
katex.render("{latex_code}", document.getElementById('ktx_count_{ktx_count}'),{
    throwOnError: false
});
</script></div>
    """
    ht = ht.replace("{ktx_count}", str(katex_elements_count))
    # TODO replace the following line with a better escaping mechanism
    ht = ht.replace("{latex_code}", latex_code.replace("\\", "\\\\"))
    outfile.write(ht)
    katex_elements_count += 1


def insert_big_formula(outfile, latex_code):
    outfile.write('<div style="text-align: center;">')
    insert_formula(outfile, latex_code[:-1])
    outfile.write('</div>')


if __name__ == "__main__":
    main()
