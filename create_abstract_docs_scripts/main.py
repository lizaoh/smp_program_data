#! python3
"""Create Abstract Docs

Using Google Drive API to create a Google Doc for each paper's abstract for a specific year's SMP
conference. This creates each doc one at a time for now because the abstract text extraction for 1999
doesn't automate well.

Learned to use API through tutorials by Jie Jann:
https://learndataanalysis.org/google-drive-api-in-python-getting-started-lesson-1/#google_vignette
https://www.youtube.com/watch?v=9K2P2bWEd90&list=PL3JVwFmb_BnTamTxXbmlwpspYdpmaHdbz
"""
import create_abstract_doc


def main():
    parent_folder_id = []
    with open("year_folder_id.txt") as f:
        parent_folder_id.append(f.read())

    year = '1999'
    first_author = 'Townsend'
    titleword = 'Hazard'
    file_name = f"{year}-{first_author}-{titleword}"
    text_content = 'A new type of hazard function, based on CDFs rather than survivor functions, is proposed. The integrated version is likewise analogous to the traditional integrated hazard function. Just as the traditional integrated hazard function leads to a useful capacity function in the case of minimum-time (i.e., race = OR) processing, the new integrated hazard function permits derivation of a novel capacity function that is appropriate for exhaustive processing experiments.'

    print(file_name)

    create_abstract_doc.create_and_write_file(
        file_name,
        parent_folder_id,
        text_content
    )


if __name__ == '__main__':
    main()

