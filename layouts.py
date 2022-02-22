import insets

BEGIN_DEEPER = "\\begin_deeper"
TITLE_LAYOUT = "Title"
PART_LAYOUT = "Part"
SECTION_LAYOUT = "Section"
SUBSECTION_LAYOUT = "Subsection"
SUBSUBSECTION_LAYOUT = "Subsubsection"
PARAGRAPH_LAYOUT = "Paragraph"
SUBPARAGRAPH_LAYOUT = "Subparagraph"
STANDARD_LAYOUT = "Standard"
AUTHOR_LAYOUT = "Author"
UNNUMBERED_TITLE_LAYOUT = "Title*"
UNNUMBERED_PART_LAYOUT = "Part*"
UNNUMBERED_SECTION_LAYOUT = "Section*"
UNNUMBERED_SUBSECTION_LAYOUT = "Subsection*"
UNNUMBERED_SUBSUBSECTION_LAYOUT = "Subsubsection*"
UNNUMBERED_PARAGRAPH_LAYOUT = "Paragraph*"
UNNUMBERED_SUBPARAGRAPH_LAYOUT = "Subparagraph*"
DATE_LAYOUT = "Date"
LYX_CODE_LAYOUT = "LyX-Code"
PLAIN_LAYOUT = "Plain Layout"

TEXT_LAYOUTS = {TITLE_LAYOUT, AUTHOR_LAYOUT, DATE_LAYOUT, PART_LAYOUT,
                SECTION_LAYOUT, SUBSECTION_LAYOUT,
                SUBSUBSECTION_LAYOUT, PARAGRAPH_LAYOUT, SUBPARAGRAPH_LAYOUT,
                UNNUMBERED_TITLE_LAYOUT, UNNUMBERED_PART_LAYOUT,
                UNNUMBERED_SECTION_LAYOUT, UNNUMBERED_SUBSECTION_LAYOUT,
                UNNUMBERED_SUBSUBSECTION_LAYOUT, UNNUMBERED_PARAGRAPH_LAYOUT,
                UNNUMBERED_SUBPARAGRAPH_LAYOUT,
                STANDARD_LAYOUT,
                PLAIN_LAYOUT
                }

LAYOUT_TAGS = {
    TITLE_LAYOUT: 'h1 class="title"',
    AUTHOR_LAYOUT: 'h1 class="author"',
    PART_LAYOUT: 'h2 class="part"',
    UNNUMBERED_PART_LAYOUT: 'h2 class="part"',
    SECTION_LAYOUT: 'h3 class="section"',
    UNNUMBERED_SECTION_LAYOUT: 'h3 class="section"',
    SUBSECTION_LAYOUT: 'h4 class="subsection"',
    UNNUMBERED_SUBSECTION_LAYOUT: 'h4 class="subsection"',
    SUBSUBSECTION_LAYOUT: 'h5 class="subsubsection"',
    UNNUMBERED_SUBSUBSECTION_LAYOUT: 'h5 class="subsubsection"',
    PARAGRAPH_LAYOUT: 'h6 class="paragraph"',
    UNNUMBERED_PARAGRAPH_LAYOUT: 'h6 class="paragraph"',
    SUBPARAGRAPH_LAYOUT: 'h6 class="subparagraph"',
    UNNUMBERED_SUBPARAGRAPH_LAYOUT: 'h6 class="subparagraph"',
    STANDARD_LAYOUT: 'div class="standard"',
    PLAIN_LAYOUT: 'div class="plain"'
}
BEGIN_TAGS = {

}
LAYOUT_NUMBERING = {
    PART_LAYOUT: r'<span style="display: block">\partname  \thepart</span>',
    SECTION_LAYOUT: r'<span>\thesection  </span>',
    SUBSECTION_LAYOUT: r'<span>\thesubsection  </span>',
    SUBSUBSECTION_LAYOUT: r'<span>\thesubsubsection  </span>',
    PARAGRAPH_LAYOUT: "",
    SUBPARAGRAPH_LAYOUT: "",
}

ENUMERATE_LAYOUT = "Enumerate"
ITEMIZE_LAYOUT = "Itemize"
ITEM_TAG = "li"
LIST_TAG = {
    ENUMERATE_LAYOUT: "ol",
    ITEMIZE_LAYOUT: "ul"
}
ENUMERATE_TYPES = "1aiAI"

LIST_LAYOUTS = {ENUMERATE_LAYOUT, ITEMIZE_LAYOUT}

styles = {"bar", "uuline", "uwave",
          "series",
          "color",
          "strikeout"}
VALID_COLORS = {
    "inherit",
    "default",
    "black",
    "blue",
    "brown",
    "cyan",
    "darkgray",
    "gray",
    "green",
    "lightgray",
    "lime",
    "magenta",
    "olive",
    "orange",
    "pink",
    "purple",
    "red",
    "teal",
    "violet",
    "white",
    "yellow"
}

RTL_LANGUAGES = {"arabic", "hebrew"}

def parse_begin_layout(parser, outfile):
    """parses a layout, from \\begin layout to \\end_layout."""
    assert parser.current_command() == "\\begin_layout"
    parameters = parser.current_parameters()
    assert len(parameters) >= 1
    layout_type = " ".join(parameters)
    if layout_type in TEXT_LAYOUTS:
        parse_text_layout(parser, outfile)
    elif layout_type == LYX_CODE_LAYOUT:
        outfile.write('<div class="lyx-code">')
        parse_lyx_code(parser, outfile)
        outfile.write('</div>')
    elif layout_type in LIST_LAYOUTS:
        parse_list_layout(parser, outfile)
    else:
        raise Exception(f"Unsupported layout type in {parser.current_line[:-1]}")


def parse_lyx_code(parser, outfile, indent=0):
    """ parses the lyx code"""
    while True:
        if parser.current_command() != "\\begin_layout" or \
             parser.current_parameters()[0] != LYX_CODE_LAYOUT:
            break
        parser.advance()

        if not parser.is_current_command():
            outfile.write('<div>')
            parse_text(parser, outfile, indent=indent)
            outfile.write('</div>')

        if parser.current_command() == "\\end_layout" and \
                parser.next_command() == "\\begin_deeper":
            assert parser.current_command() == "\\end_layout"
            parser.advance()  # \end_layout
            assert parser.current_command() == "\\begin_deeper"
            parser.advance()  # \begin_deeper
            parse_lyx_code(parser, outfile, indent=indent + 1)
            assert parser.current_command() == "\\end_deeper"
            parser.advance()  # \end_deeper

        if parser.current_command() == "\\end_layout" and \
                parser.next_command() == "\\begin_layout" and \
                parser.next_parameters()[0] == LYX_CODE_LAYOUT:
            assert parser.current_command() == "\\end_layout"
            parser.advance()
            assert parser.current_command() == "\\begin_layout"
            continue
        elif parser.current_command() == "\\end_layout":
            parser.advance()
            break
        else:
            pass


def parse_text_layout(parser, outfile):
    """parses a text layout, from \\begin layout to \\end_layout."""
    layout_type = " ".join(parser.current_parameters())
    outfile.write(f"<{LAYOUT_TAGS[layout_type]}>")
    if layout_type in LAYOUT_NUMBERING.keys():
        outfile.counter.increase_counter(layout_type.lower())
        outfile.write(outfile.counter.evaluate(LAYOUT_NUMBERING[layout_type]))
    parser.advance()
    parse_text(parser, outfile)
    assert parser.current_command() == "\\end_layout"
    outfile.write(f"</{LAYOUT_TAGS[layout_type].split()[0]}>\n")
    parser.advance()


def parse_list_layout(parser, outfile, level=0):
    """parses itemize and enumerate"""
    layout_type = parser.current_parameters()[0]
    write_list_begin_tag(outfile, layout_type, level)
    while parser.current_command() == "\\begin_layout" \
            and parser.current_parameters()[0] in LIST_LAYOUTS:
        # list type changed from enumerate to itemize or vice versa
        if parser.current_parameters()[0] != layout_type:
            outfile.write(f"</{LIST_TAG[layout_type]}>")
            layout_type = parser.current_parameters()[0]
            write_list_begin_tag(outfile, layout_type, level)
        parse_list_item(parser, outfile, level=level)

    outfile.write(f"</{LIST_TAG[layout_type]}>")


def write_list_begin_tag(outfile, list_type, level):
    if list_type == ENUMERATE_LAYOUT:
        outfile.write(f'<{LIST_TAG[ENUMERATE_LAYOUT]} type="{ENUMERATE_TYPES[level]}">')
    else:
        outfile.write(f"<{LIST_TAG[ITEMIZE_LAYOUT]}>")


def parse_list_item(parser, outfile, level=0):
    assert parser.current_command() == "\\begin_layout" \
        and parser.current_parameters()[0] in LIST_LAYOUTS
    outfile.write(f"<{ITEM_TAG}>")
    parser.advance()
    parse_text(parser, outfile)
    assert parser.current_command() == "\\end_layout"
    parser.advance()
    if parser.current_command() == "\\begin_deeper":
        parser.advance()
        parse_list_layout(parser, outfile, level=level+1)
        assert parser.current_command() == "\\end_deeper"
        parser.advance()
    outfile.write(f"</{ITEM_TAG}>")


def parse_text(parser, outfile, indent=0):
    """parses a text and its styles"""
    language = parser.default_language

    paragraph_styles = {
        "bar": "default",
        "uuline": "default",
        "uwave": "default",
        "series": "default",
        "color": "default",
        "strikeout": "default",
    }

    outfile.write(f'<span style="{get_style(paragraph_styles)}">')
    outfile.write("&nbsp;"*indent*4)
    style_changed = False
    while not parser.is_current_command() or \
            parser.current_command() != "\\end_layout":
        if not parser.is_current_command():
            if style_changed:
                outfile.write(
                    f'</span><span style="{get_style(paragraph_styles)}">')
                style_changed = False
            # The entire line without the newline
            text = parser.current()[:-1]
            if is_rtl(language):  # parentheses should be reversed in rtl languages
                translation_table = str.maketrans("()", ")(")
                text = text.translate(translation_table)
            outfile.write(text)
            parser.advance()
        else:
            if parser.current_command() == "\\begin_inset":
                insets.parse_inset(parser, outfile)
            elif parser.current_command()[1:] in styles:
                param = parser.current_parameters()[0]
                paragraph_styles[parser.current_command()[1:]] = param
                parser.advance()
                style_changed = True
            elif parser.current_command() == "\\lang":
                language = parser.current_parameters()[0]
                parser.advance()
            else:
                parser.advance()
    outfile.write('</span>')


def get_style(style_dict):
    out = ""
    if style_dict["bar"] == "under":
        out += 'text-decoration: underline; '
    if style_dict["uuline"] == "on":
        out += 'text-decoration-line: underline; text-decoration-style: double; '
    if style_dict["uwave"] == "on":
        out += 'text-decoration-line: underline; text-decoration-style: wavy; '

    if style_dict["series"] == "medium":
        out += 'font-weight: normal; '
    elif style_dict["series"] == "bold":
        out += 'font-weight: bold; '

    if style_dict["strikeout"] == "on":
        out += 'text-decoration: line-through; '

    if style_dict["color"] in VALID_COLORS:
        out += f'color: {style_dict["color"]}; '
    return out


def is_rtl(language):
    return language in RTL_LANGUAGES
