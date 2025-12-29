#! python3
"""Create Abstract Docs

Using Google Drive API to create a Google Doc for each paper's abstract for a specific year's SMP
conference. This creates each doc one at a time for now because the abstract text extraction for 1999
doesn't automate well.

Learned to use API through tutorials by Jie Jenn:
https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/#google_vignette
https://www.youtube.com/watch?v=9K2P2bWEd90&list=PL3JVwFmb_BnTamTxXbmlwpspYdpmaHdbz
"""
import create_abstract_doc
import sheets_edit
import os


def main(year=None):
    parent_folder_id = []
    abstracts_folder_id = []

    with open("abstracts_folder_id.txt") as f:
        abstracts_folder_id.append(f.read())

    with open("year_sheet_id.txt") as f:
        program_sheet_id = f.read()

    with open("combined_sheet_id.txt") as f:
        combined_sheet_id = f.read()

    sheets_edit.make_and_update_abstract(year, program_sheet_id, combined_sheet_id, abstracts_folder_id)


if __name__ == '__main__':
    main(year='2011')

