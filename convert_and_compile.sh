#!/bin/bash
# ========================================
# AMA to MDPI Complete Conversion and Compilation Script
# ========================================

echo ""
echo "========================================"
echo "AMA to MDPI Conversion and Compilation"
echo "========================================"
echo ""

# Step 1: Run the conversion script
echo "[1/5] Running conversion script..."
python ama_to_mdpi_convert.py --source_dir ./ama_source --mdpi_template_dir ./mdpi_template --out_dir ./output
if [ $? -ne 0 ]; then
    echo "ERROR: Conversion failed!"
    exit 1
fi
echo "Conversion completed successfully."
echo ""

# Step 2: Change to output directory
cd output || {
    echo "ERROR: Cannot enter output directory!"
    exit 1
}

# Step 3: First LaTeX pass
echo "[2/5] Running pdflatex (first pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
echo ""

# Step 4: Run bibtex
echo "[3/5] Running bibtex..."
bibtex main
echo ""

# Step 5: Second LaTeX pass
echo "[4/5] Running pdflatex (second pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
echo ""

# Step 6: Final LaTeX pass
echo "[5/5] Running pdflatex (final pass)..."
pdflatex -interaction=nonstopmode main.tex
echo ""

# Check if PDF was generated
if [ -f main.pdf ]; then
    echo "========================================"
    echo "SUCCESS: Compilation complete!"
    echo "========================================"
    echo ""
    echo "Generated files:"
    ls -lh main.pdf
    echo ""
    echo "Output location: $(pwd)/main.pdf"
    echo "Conversion report: $(pwd)/conversion_report.md"
    echo ""
else
    echo "========================================"
    echo "ERROR: PDF generation failed!"
    echo "========================================"
    echo "Check main.log for details"
    echo ""
fi

# Return to original directory
cd ..
