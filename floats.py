import output_document
import main

FIGURE = "figure"
ALGORITHM = "algorithm"

FLOATS_DIVS = {
    FIGURE: 'div class="floating-figure"',
    ALGORITHM: 'div class="algorithm"'
}

FLOATS_BODIES = {
    FIGURE: output_document.FLOATING_FIGURE_BODY,
    ALGORITHM: output_document.FLOATING_ALGORITHM_BODY
}

def parse_float(parser, outfile):
    assert parser.current_command() == "\\begin_inset"
    assert parser.current_parameters()[0] == "Float"
    float_type = parser.current_parameters()[1]
    outfile.write(f'<{FLOATS_DIVS[float_type]}>')
    parser.advance()  # \begin_inset Float _______
    body_type = outfile.current_body
    outfile.current_body = FLOATS_BODIES[float_type]

    # discard float parameters
    while not parser.is_current_command():
        parser.advance()

    main.parse_multiple_text_layouts(parser, outfile)
    outfile.current_body = body_type
    parser.advance()  # \end_inset
    outfile.write(f"</{FLOATS_DIVS[float_type].split()[0]}>")

