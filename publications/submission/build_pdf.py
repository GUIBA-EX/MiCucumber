"""Build editable submission files; export PDFs with Word or LibreOffice."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("build_docx.py")),run_name="__main__")
print("DOCX files rebuilt. Export to PDF and inspect pagination before replacing checked PDFs.")
