from counter import Counter

NORMAL_BODY = "normal_body"
FLOATING_FIGURE_BODY = "floating_figure_body"
FLOATING_ALGORITHM_BODY = "algorithm_body"


class OutputDocument:
    def __init__(self, outfile_path):
        self.file = open(outfile_path, "w")
        self.file_path = outfile_path
        self.counter = Counter()
        self.current_body = NORMAL_BODY

    def write(self, string):
        self.file.write(string)

    def close(self):
        self.file.close()

