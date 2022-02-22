# HTMLyX

> **HTMLyX** is still in early stages of development, and most features available in LyX are currently unsupported.

**HTMLyX** is a cross-platform LyX to HTML compiler.

## Motivation

[LyX](https://www.lyx.org/) is an open-source document processor. Usually, it export document as `.tex` file which are
then compiled to `.pdf` using some installation of TeX. However, the multiple TeX instances of different operating
systems make it difficult to compile files on different computers.

Moreover, the `.pdf` documents generated are not easily viewed on mobile devices with small screens.
Attempts have been made to compile both LyX and LaTeX documents into html code, but such attempts are lacking in terms
of _Right-to-Left support_ and _support of math equations_. This project claim to provide adequate support for both.

## Usage

```
usage: python main.py [-h] input_file output_file

Convert .lyx files to .html files.

positional arguments:
  input_file   path to a valid .lyx file
  output_file  where to store the resulting .html file

optional arguments:
  -h, --help   show this help message and exit
```

## What's currently supported

* Standard layout

* Titles and *numbered* parts **only** (the numbers are not currently rendered)

* Math insets (inline, display mode and math macros)

* Supported styles: **Series** (bold) and <u>bar</u> (underline)

## TODO:

- [ ] Support all default layout types:
  
  - [x] Standard
  
  - [X] LyX-Code.
    **note**: *the separator which LyX adds after the LyX-Code is not currently
    supported*
  
  - [ ] Quotation
  
  - [ ] Quote
  
  - [ ] Verse
  
  - [ ] Verbatim/Verbatim*
  
  - [x] Part/Part*
  
  - [x] Section/Section*
  
  - [x] Subsection/Subsection*
  
  - [x] Subsubsection/Subsubsection*
  
  - [x] Paragraph/Paragraph*
  
  - [x] Subparagraph/Subparagraph*
  
  - [x] Title
  
  - [ ] Author
  
  - [ ] Date
  
  - [ ] Abstract
  
  - [ ] Address
  
  - [ ] Right Address
  
  - [ ] Labeling
  
  - [x] Itemize
  
  - [x] Enumerate
  
  - [X] Description

- [ ] All text formatting:
  
  - [x] Series
  
  - [ ] Shape
  
  - [ ] Size
  
  - [x] Color
  
  - [ ] Underlining
  
  - [ ] Strikethrough

- [ ] Boxes

- [ ] Support ams-article layout types

- [ ] Tables

- [ ] Images - not fully supported yet but can be inserted and scaled uniformly using scale%.

- [x] Floating figures, algorithms and tables

- [ ] Table of contents, table oparenthesis for RTLf algorithms

- [ ] Bibliography

- [ ] Labels & Cross references

- [ ] Hyperlinks

- [ ] Reverse parenthesis for RTL languages

## Requirements

1. [Python 3.8+](https://www.python.org/)

2. [NodeJS](https://nodejs.org) with [KaTeX](https://github.com/KaTeX/KaTeX) installed.

## License

**HTMLyX** is released under the GNU GPL version 3.0. The license can be found in `LICENSE`, but if for some reason it
wasn't included with the code, you can find it [here](https://www.gnu.org/licenses/gpl-3.0.txt).
