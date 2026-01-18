# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a LaTeX document conversion tool that migrates AMA (American Medical Association) format LaTeX papers to MDPI (Multidisciplinary Digital Publishing Institute) template format. The project consists of a Python script that automates the conversion process and batch scripts for one-click compilation.

## Commands

### One-Click Conversion and Compilation (Recommended)

**Windows:**
```cmd
convert_and_compile.bat
```

**Linux/Mac:**
```bash
./convert_and_compile.sh
```

This script automatically:
1. Runs the conversion (AMA → MDPI)
2. Compiles LaTeX with pdflatex (first pass)
3. Processes bibliography with bibtex
4. Compiles LaTeX again (second pass)
5. Final compilation to resolve all references

Output: `output/main.pdf` with complete bibliography

### Manual Steps (Advanced)

#### Run the Full Conversion Only
```bash
python ama_to_mdpi_convert.py \
    --source_dir ./ama_source \
    --mdpi_template_dir ./mdpi_template \
    --out_dir ./output \
    --out_main_tex main.tex \
    --figures_dir figures \
    --bib_name refs.bib
```

#### Compile the Output LaTeX with Bibliography
```bash
cd output
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Or use the provided compilation scripts:
- Windows: `output/compile.bat`
- Linux/Mac: `output/compile.sh`

## Architecture

### Main Conversion Script: `ama_to_mdpi_convert.py`

This is the primary conversion tool that orchestrates the entire migration process. It performs the following operations:

1. **Main File Detection** (`find_main_tex`): Automatically identifies the main .tex file in both AMA source and MDPI template by looking for `\documentclass` and `\begin{document}`. Priority is given to common names like `main.tex`, `manuscript.tex`, etc., with fallback to shortest path depth and largest file size.

2. **Body Extraction** (`extract_document_body`): Extracts content between `\begin{document}` and `\end{document}` from the AMA source file, which is the actual paper content to be migrated.

3. **Citation Normalization** (`normalize_citations`): Converts natbib-style citation commands (`\citep{}`, `\citet{}`) to standard `\cite{}` that MDPI supports. Issues warnings for incompatible commands like `\citeauthor` or `\citeyear`.

4. **Graphics Path Fixing** (`fix_includegraphics_paths`): Rewrites all `\includegraphics{}` paths to use the standardized `figures/<basename>` format, ensuring images are referenced correctly in the output structure.

5. **Image Migration** (`collect_files_by_ext`): Copies all image files (`.png`, `.jpg`, `.jpeg`, `.pdf`, `.eps`, `.svg`) from AMA source to the output `figures/` directory.

6. **Bibliography Merging** (`merge_bib_files`): Merges all `.bib` files from the AMA source into a single `refs.bib` file, detecting and warning about duplicate citation keys.

7. **Template Population**: Copies the entire MDPI template structure (including `Definitions/` directory with style files) and injects the converted AMA body into the MDPI template structure.

8. **Title and Abstract Extraction**: Extracts title from `\title{}` command and abstract from `\section*{Abstract}`, then injects them into MDPI template's `\Title{}` and `\abstract{}` commands respectively, avoiding duplication.

9. **Conversion Report**: Generates a detailed `conversion_report.md` with statistics, warnings, and errors encountered during conversion.

### Object-Oriented Architecture

The conversion script uses a clean object-oriented design with the following classes:

- **`TeXParser`**: Handles TeX file detection, reading, parsing, and content extraction (title, abstract, document body)
- **`ContentProcessor`**: Processes and transforms content (citation normalization, path fixing, removing biblatex commands)
- **`FileHandler`**: Manages file operations (copying images, merging bibliography files, copying template structure)
- **`AMAToMDPIConverter`**: Main controller class that orchestrates the entire conversion workflow
- **`ConversionReport`**: Data structure for tracking conversion results, warnings, and errors

### Directory Structure Expectations

- **ama_source/**: Contains the AMA format LaTeX project
  - Must contain a main `.tex` file with `\documentclass` and `\begin{document}`
  - May contain `.bib` files for references
  - May contain image files in various formats

- **mdpi_template/**: Contains the MDPI LaTeX template
  - Must contain a template `.tex` file (typically `template.tex`)
  - Contains `Definitions/` subdirectory with:
    - `mdpi.cls`: Main MDPI class file
    - `mdpi.bst`, `mdpi_apacite.bst`, `mdpi_chicago.bst`: Bibliography styles
    - `logo-mdpi.eps` and other logo files
    - `journalnames.tex`: Journal name definitions

- **output/**: Generated output directory (created by the script)
  - Contains complete MDPI-formatted project ready to compile
  - Includes `conversion_report.md` with migration details

### Batch Compilation Scripts

The project includes automated compilation scripts:

- **`convert_and_compile.bat`** (Windows) / **`convert_and_compile.sh`** (Linux/Mac): One-click script that runs the complete workflow:
  1. Executes the conversion script
  2. Runs pdflatex (first pass)
  3. Runs bibtex to process bibliography
  4. Runs pdflatex (second pass)
  5. Runs pdflatex (final pass for cross-references)

- **`output/compile.bat`** / **`output/compile.sh`**: Standalone scripts to recompile an already-converted project with bibliography support

### Key Conversion Logic

**Citation Handling**: The tool normalizes citation commands from natbib style (`\citep{}`, `\citet{}`) to standard `\cite{}` that MDPI supports. Warnings are issued for potentially incompatible commands like `\citeauthor` or `\citeyear`.

**Biblatex to Natbib Conversion**: The converter automatically:
- Removes `\printbibliography` commands (biblatex)
- Removes `\addbibresource{}` commands (biblatex)
- Adds `\bibliography{refs}` command (natbib) if not present
- This ensures compatibility with MDPI's natbib-based bibliography system

**Title and Abstract**: Extracts title and abstract from AMA source and injects them into MDPI template commands, preventing duplication in the document body.

**Image Paths**: AMA sources often use relative or nested paths for images. The converter standardizes all paths to `figures/<filename>` format for consistency with MDPI structure.

**Template Preservation**: The entire MDPI template structure is preserved (including all style files, logos, and definition files) to ensure proper compilation. The preamble is updated with extracted metadata (title, abstract) while the document body contains the converted content.

### Error Handling

The conversion script uses a structured `ConvertReport` dataclass to track:
- **Errors**: Fatal issues that prevent successful conversion (missing main files, extraction failures)
- **Warnings**: Non-fatal issues requiring manual review (duplicate bib keys, incompatible citation commands, missing images)

The report is always generated at `output/conversion_report.md` for post-conversion review.
