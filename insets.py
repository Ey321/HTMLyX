import os.path
import floats
import main
import output_document
import shutil
import pathlib
import re
import subprocess
import layouts
import katex_renderer

image_count = 0
katex_macros = ""

EXISTING_MACROS = {"exp", "N", "S"}

BODY_TYPE_TO_CAPTION_COUNTER = {
    output_document.NORMAL_BODY: ("\\c@caption", "\\thecaption"),
    output_document.FLOATING_FIGURE_BODY: ("\\c@figure", "\\thefigure"),
    output_document.FLOATING_ALGORITHM_BODY: ("\\c@algorithm",
                                              "\\thealgorithm")
}

PIXELS_IN_CM = 37.8


def parse_inset(parser, outfile):
    """parses an inset"""
    assert parser.current_command() == "\\begin_inset"
    if parser.current_parameters()[0] == "Formula":
        if len(parser.current_parameters()) == 1:  # non inline formula
            latex_code = ""
            parser.advance()
            while parser.current() != "\\end_inset\n":
                latex_code += parser.current()
                parser.advance()
            # on non-inline formulas that are not align areas, the latex equation is surrounded by \[ \]
            if latex_code.startswith("\\[") and latex_code.endswith("\\]\n"):
                latex_code = latex_code[2:-3]
            insert_big_formula(outfile, latex_code)
        else:  # an inline formula
            latex_code = " ".join(parser.current_parameters()[1:])
            parser.advance()
            while parser.current() != "\\end_inset\n":
                latex_code += parser.current()
                parser.advance()
            insert_formula(outfile, latex_code.strip()[1:-1])
    elif parser.current_parameters()[0] == "Float":
        floats.parse_float(parser, outfile)
        return
    elif parser.current_parameters()[0] == "Separator":
        if parser.current_parameters() == ["Separator", "plain"]:
            outfile.write('<hr noshade class="plain">')
            parser.advance()
        else:
            raise Exception(f"Unsupported separator type: "
                            + str(parser.current_parameters()))
    elif parser.current_parameters()[0] == "Newline":
        if parser.current_parameters() == ["Newline", "newline"]:
            parser.advance()
            outfile.write("<br/>")
    elif parser.current_parameters()[0] == "Caption":
        if parser.current_parameters() == ["Caption", "Standard"]:
            outfile.write('<div class="caption" style="text-align: center;">')
            counter_name, caption_format = BODY_TYPE_TO_CAPTION_COUNTER[
                outfile.current_body]
            outfile.counter.increase_counter(counter_name)
            outfile.write(outfile.counter.evaluate(caption_format))
            parser.advance()  # \begin_inset Caption Standard
            parser.advance()  # \begin_layout Plain Layout
            layouts.parse_text(parser, outfile)
            parser.advance()  # \end_layout
            outfile.write("</div>")
    elif parser.current_parameters()[0] == "Graphics":
        parse_graphics(parser, outfile)
    elif parser.current_parameters()[0] == "FormulaMacro":
        parse_formula_macro(parser)
    elif parser.current_parameters()[0] == "Foot":
        # TODO actually handle foot, this is here just for the demo
        parser.advance()
        main.parse_multiple_text_layouts(parser, outfile)
    else:
        print(f"Unknown inset {parser.current().__repr__()}, skipping.")
        while parser.current() != "\\end_inset\n":
            parser.advance()

    assert parser.current_command() == "\\end_inset"
    parser.advance()
    return


def parse_formula_macro(parser):
    global katex_macros
    assert parser.current_command() == "\\begin_inset"
    assert parser.current_parameters() == ["FormulaMacro"]
    parser.advance()
    macro = parser.current()
    parser.advance()
    while parser.current() != "\\end_inset\n":
        # macro += parser.current()
        parser.advance()
    match = re.match(r"\\(re)?newcommand\{\\(?P<macroname>.*?)}", macro)
    assert match  # should match
    print(match.groupdict()["macroname"])
    if match.groupdict()["macroname"] in EXISTING_MACROS:
        katex_macros += "\\re" + macro[len("\\"):]
    else:
        katex_macros += macro


def parse_graphics(parser, outfile):
    assert parser.current_command() == "\\begin_inset"
    assert parser.current_parameters() == ["Graphics"]
    parser.advance()
    filename = None
    width = None
    height = None
    scale = None
    while parser.current() != "\\end_inset\n":
        line = parser.current().strip()
        if line.startswith("filename "):
            filename = line[9:]
        elif line.startswith("width "):
            width = line[6:]
        elif line.startswith("scale "):
            scale = int(line[6:])
        parser.advance()

    insert_image(parser, outfile, filename, width, height, scale)

    assert parser.current_command() == "\\end_inset"


def insert_image(parser, outfile, filename, width, height, scale):
    global image_count
    if os.path.isabs(filename):
        img_path = pathlib.Path(filename)
    else:
        img_path = pathlib.Path(parser.file_path)
        img_path = img_path.parent / filename

    dest_path = pathlib.Path(outfile.file_path).parent / "images" / f"img{image_count}"
    if not (dest_path.parent.exists()):
        os.mkdir(dest_path.parent)
    shutil.copy(img_path, dest_path)

    outfile.write(f'<img src="images/img{image_count}" ')
    if scale:
        outfile.write(f'onload="this.width*={scale / 100};this.onload=null;"')

    else:
        # TODO support all widths formats
        if width:
            # width is % of text width
            if match := re.match(r"(?P<width>\d+)text%$", width):
                outfile.write(f'width="{match["width"]}%"')
            # width is given in pt
            elif match := re.match(r"(?P<width>\d+)pt$", width):
                outfile.write(f'width="{match["width"]}pt"')
            # width is given in cm
            elif match := re.match(r"(?P<width>\d+)cm$", width):
                outfile.write(f'width="{int(match["width"]) * PIXELS_IN_CM}px"')

        if height:
            # TODO support height
            print("Height is not yet supported!")

    outfile.write("/>")
    image_count += 1


def insert_formula(outfile, latex_code, display_mode=False):
    if not display_mode:
        latex_code = "\\left. " + latex_code + "\\right."
    html_code = katex_renderer.render_equation(katex_macros + latex_code, display_mode)
    if display_mode:
        outfile.write(
            f'<span dir="ltr" style="overflow-x: hidden; overflow-y: hidden; \
            white-space: nowrap; vertical-align: baseline; width: max-content; display:inline-flex; justify-content: center;\
            ">{html_code}</span>')
    else:
        outfile.write(
            f'<span dir="ltr" style="overflow-x: auto; overflow-y: hidden; display: inline-flex; max-width: 100%; \
            white-space: nowrap; vertical-align: baseline;">{html_code}</span>')


def insert_big_formula(outfile, latex_code):
    outfile.write('''<div dir="ltr" style="text-align: center;display: inline-block; overflow-x: auto; overflow-y: hidden; 
    max-width: 100%; vertical-align: middle; margin-top: 0px; width: 100%;">''')
    insert_formula(outfile, latex_code[:-1], display_mode=True)
    outfile.write('</div>')
