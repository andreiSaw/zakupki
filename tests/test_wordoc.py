import os

import docx


# TODO test_wordoc
def test_wordoc():
    print("working in " + os.getcwd())
    wordDoc = docx.Document(os.getcwd() + '/data/demo.docx')
    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                pass
                # print(cell.text)
