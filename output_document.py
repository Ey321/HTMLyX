from counter import Counter
import pathlib

NORMAL_BODY = "normal_body"
FLOATING_FIGURE_BODY = "floating_figure_body"
FLOATING_ALGORITHM_BODY = "algorithm_body"


class OutputDocument:
    def __init__(self, outfile_path):
        self.directory = outfile_path
        self.current_pt = 0
        self.file_path = pathlib.Path(self.directory) / f"pt{self.current_pt}"
        self.file = open(self.file_path, "w")
        self.counter = Counter()
        self.current_body = NORMAL_BODY
        self.write_beginning()

    def write_beginning(self):
        self.write("<!DOCTYPE html>")
        self.write("<html>\n")
        self.write("<head>\n")
        self.write('<meta http-equiv="Content-type" '
                      'content="text/html;charset=UTF-8"/>\n')
        self.write(
            """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.15.2/dist/katex.min.css" integrity="sha384-MlJdn/WNKDGXveldHDdyRP1R4CTHr3FeuDNfhsLPYrq2t0UBkUdK2jyTnXPEK1NQ" crossorigin="anonymous">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
        )
        self.write("""
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
        self.write('</head\n>')

    def new_file(self):
        self.close()
        self.current_pt += 1
        self.file_path = pathlib.Path(self.directory) / f"pt{self.current_pt}"
        self.file = open(self.file_path, "w")
        self.write_beginning()

    def write_end(self):
        self.write("</html>")

    def write(self, string):
        self.file.write(string)

    def close(self):
        self.write_end()
        self.file.close()

