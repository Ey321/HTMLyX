katex_elements_count = 0


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
