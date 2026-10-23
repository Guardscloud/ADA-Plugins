"""Dated Filenames: ADA puts today's date at the start of every report/file name it creates.

Example: 2026-10-23_sales_report.xlsx. Makes outputs easy to sort and find later.
"""
from datetime import date

from ada import kernel


@kernel.system
def dated_filenames() -> str:
    return (f"Plugin rule (Dated Filenames): when you create a document, spreadsheet, presentation, PDF, chart or "
            f"other output file, start its file name with today's date in YYYY-MM-DD format followed by an "
            f"underscore, e.g. {date.today():%Y-%m-%d}_report.docx. Do not rename existing user files.")
