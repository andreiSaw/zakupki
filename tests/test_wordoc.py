import docx

# TODO test_wordoc
def test_wordoc():
    wordDoc = docx.Document('../data/demo.docx')
    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                print(cell.text)
