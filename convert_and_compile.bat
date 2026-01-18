@echo off
REM ========================================
REM AMA to MDPI Complete Conversion and Compilation Script
REM ========================================
echo.
echo ========================================
echo AMA to MDPI Conversion and Compilation
echo ========================================
echo.

REM Step 1: Run the conversion script
echo [1/5] Running conversion script...
python ama_to_mdpi_convert.py --source_dir ./ama_source --mdpi_template_dir ./mdpi_template --out_dir ./output
if errorlevel 1 (
    echo ERROR: Conversion failed!
    pause
    exit /b 1
)
echo Conversion completed successfully.
echo.

REM Step 2: Change to output directory
cd output
if errorlevel 1 (
    echo ERROR: Cannot enter output directory!
    cd ..
    pause
    exit /b 1
)

REM Step 3: First LaTeX pass
echo [2/5] Running pdflatex (first pass)...
pdflatex -interaction=nonstopmode main.tex > nul 2>&1
if errorlevel 1 (
    echo Warning: First pass had some issues, continuing...
)
echo.

REM Step 4: Run bibtex
echo [3/5] Running bibtex...
bibtex main
if errorlevel 1 (
    echo Warning: Bibtex had some issues, continuing...
)
echo.

REM Step 5: Second LaTeX pass
echo [4/5] Running pdflatex (second pass)...
pdflatex -interaction=nonstopmode main.tex > nul 2>&1
echo.

REM Step 6: Final LaTeX pass
echo [5/5] Running pdflatex (final pass)...
pdflatex -interaction=nonstopmode main.tex
echo.

REM Check if PDF was generated
if exist main.pdf (
    echo ========================================
    echo SUCCESS: Compilation complete!
    echo ========================================
    echo.
    echo Generated files:
    dir main.pdf
    echo.
    echo Output location: %CD%\main.pdf
    echo Conversion report: %CD%\conversion_report.md
    echo.
) else (
    echo ========================================
    echo ERROR: PDF generation failed!
    echo ========================================
    echo Check main.log for details
    echo.
)

REM Return to original directory
cd ..

echo Press any key to exit...
pause > nul
