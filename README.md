# HTMLyX

> **HTMLyX** is still in early stages of development, and most features available in LyX are currently unsupported.

**HTMLyX** is a cross-platform LyX to HTML compiler.

## Motivation

[LyX](https://www.lyx.org/) is an open-source document processor. Usually, it export document as `.tex` file which are then compiled to `.pdf` using some installation of TeX. However, the multiple TeX instances of different operating systems make it difficult to compile files on different computers.

## Usage

```
usage: python main.py [-h] input_file output_file

Convert .lyx file to .html files.

positional arguments:
  input_file   path to a valid .lyx file
  output_file  where to store the resulting .html file

optional arguments:
  -h, --help   show this help message and exit
```

## What's currently supported

* Standard layout

* Titles and *numbered* parts **only** (the numbers are not currently rendered)

* Math insets

* Supported styles: **Series** (bold) and <u>bar</u> (underline)

## TODO:

- [ ] Support all default layout types:
  
  - [x] Standard
  
  - [ ] LyX-Code
  
  - [ ] Quotation
  
  - [ ] Quote
  
  - [ ] Verse
  
  - [ ] Verbatim/Verbatim*
  
  - [ ] Part/Part*
  
  - [ ] Section/Section*
  
  - [ ] Subsection/Subsection*
  
  - [ ] Subsubsection/Subsubsection*
  
  - [ ] Paragraph/Paragraph*
  
  - [ ] Subparagraph/Subparagraph*
  
  - [x] Title
  
  - [ ] Author
  
  - [ ] Date
  
  - [ ] Abstract
  
  - [ ] Address
  
  - [ ] Right Address
  
  - [ ] Labeling
  
  - [ ] Itemize
  
  - [ ] Enumerate
  
  - [ ] Description

- [ ] All text formatting:
  
  - [x] Series
  
  - [ ] Shape
  
  - [ ] Size
  
  - [ ] Color
  
  - [ ] Underlining
  
  - [ ] Strikethrough

- [ ] Math
  
  - [x] Inline math
  
  - [x] Display mode math
  
  - [ ] Math macros

- [ ] Boxes

- [ ] Support ams-article layout types

- [ ] Tables

- [ ] Images

- [ ] Floating figures, algorithms and tables

- [ ] Table of contents, table of algorithms

- [ ] Bibliography

- [ ] Labels & Cross references

- [ ] Hyperlinks

- [ ] Reverse parenthesis for RTL languages

## Requirements

1. [Python 3.X](https://www.python.org/)

2. In order to view the outputed .html file with a browser, it must be located in the same directory with an installation of [KaTeX](https://github.com/KaTeX/KaTeX). The `.html` file should be placed inside the directory called `katex`.

## License

**HTMLyX** is released under the GNU GPL version 3.0. The license is can be found in `LICENSE`, but if for some reason it wasn't included with the code, you can find it [here](https://www.gnu.org/licenses/gpl-3.0.txt).
