"""
Creates abstract doc from extracted text and creates row entry
in the overall combined spreadsheet.
"""

import io
from googleapiclient.http import MediaIoBaseUpload
import pandas as pd
import re
from Google import Create_Service
import create_abstract_doc

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "how", "what", "why", "when", "where", "which",
    "on", "in", "of", "for", "to", "and", "or",
    "does", "do", "did", "can", "will", "shall",
    "from", "with", "about", "using", "via",
    "should", "would", "could", "there",
    "toward", "towards", "beyond", "developing",
    "new", "model", "modeling", "modelling",
    "human", "application", "measuring", "effects",
    "effect", "method", "analysis", "data", "testing",
    "test", "simple", "assessing", "theories", "theory",
    "comparing", "measures", "study", "some", "role",
    "evaluating", "measurement", "no", "any", "bayesian",
    "many", "applications", "we", "every"
}


def first_substantive_word(title):
    # tokenize & lowercase
    words = re.findall(r"[A-Za-z0-9'-]+", title)

    for w in words:
        if w.isdigit():  # skip standalone numbers
            continue
        if w.lower() in STOPWORDS:  # skip any common words
            continue
        if "'" in w:    # skip words with apostrophe
            continue
        if "-" in w:  # replace hyphen with underscore
            w = w.replace('-', '_')

        # Return word as is if all caps or titlecase, else make it titlecase
        if w[0].isupper():
            return w
        else:
            # capitalize first letter
            return w.capitalize()

    return None


def append_data_row(year=None, spreadsheet_id=None, cell_range_insert=None, values=None):
    worksheet_name = f'combined_sheet!'
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()


def make_and_update_abstract(year=None, spreadsheet_id=None, combined_sheet_id=None, abstracts_folder_id=None):
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        majorDimension='ROWS',
        range=f'smp{year}_program'
    ).execute()

    # Create and get folder id for this year's abstract docs
    parent_folder_id = create_abstract_doc.create_year_folder(year, abstracts_folder_id)

    # Create df of spreadsheet
    columns = response['values'][0]
    data = response['values'][1:]
    df = pd.DataFrame(data, columns=columns)
    df = df.rename(columns={
        "author(s)": "authors",
        "affiliation(s)": "affiliations"
    })
    # small_df = df[:5]
    rest_of_df = df[5:]

    for row in rest_of_df.itertuples(index=False):
        # Get first author last name amd title keyword
        first_author_full_name = row.authors.split(',', 1)[0]
        first_author = first_author_full_name.split(' ')[-1]
        title_word = first_substantive_word(row.title)

        # Get abstract text, or n/a if blank
        if row.abstract:
            abstract_text = row.abstract
        else:
            abstract_text = 'n/a'

        # Replace hyphen with underscore in hyphenated last names
        if '-' in first_author:
            first_author = first_author.replace('-', '_')

        file_name = f"{year}-{first_author}-{title_word}"

        print(file_name)

        _, abstract_url = create_abstract_doc.create_and_write_file(
            file_name,
            parent_folder_id,
            abstract_text
        )

        row_data = [[
            year,
            row.authors,
            row.affiliations,
            row.title,
            row.type,     # type (talk, plenary, poster, symposium, etc.)
            abstract_url
        ]]

        append_data_row(year, combined_sheet_id, 'A2', row_data)

