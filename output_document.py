from counter import Counter


class OutputDocument:
    def __init__(self, outfile_path):
        self.file = open(outfile_path, "w")
        self.counter = Counter()

    def write(self, string):
        self.file.write(string)

    def close(self):
        self.file.close()
