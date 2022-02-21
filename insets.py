import os.path
import floats
import layouts
import output_document
import shutil
import pathlib
import re
import subprocess

image_count = 0

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
        if len(parser.current_parameters()) == 2:  # an inline formula
            latex_code = parser.current_parameters()[1]
            insert_formula(outfile, latex_code[1:-1])
            parser.advance()
        elif len(parser.current_parameters()) == 1:  # non inline formula
            latex_code = ""
            parser.advance()
            while parser.current() != "\\end_inset\n":
                latex_code += parser.current()
                parser.advance()
            # on non-inline formulas that are not align areas, the latex equation is surrounded by \[ \]
            if latex_code.startswith("\\[") and latex_code.endswith("\\]\n"):
                latex_code = latex_code[2:-3]
            insert_big_formula(outfile, latex_code)
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

    assert parser.current_command() == "\\end_inset"
    parser.advance()
    return


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
    html_code = subprocess.Popen(["node", "renderer/renderer.js", latex_code, str(display_mode)],
                                 stdout=subprocess.PIPE).stdout.read().decode()
    outfile.write(f"""
    <div class="viewport" style="display: inline-block; overflow: auto; 
    max-width: 80%; vertical-align: middle; margin-top: 0px;">
    <p dir="ltr"
    style="white-space: nowrap; overflow-x: auto; overflow-y: hidden; ">{html_code}</p>""")


def insert_big_formula(outfile, latex_code):
    outfile.write('<div style="text-align: center;">')
    insert_formula(outfile, latex_code[:-1], display_mode=True)
    outfile.write('</div>')
