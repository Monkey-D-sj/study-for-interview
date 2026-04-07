import pymupdf

doc = pymupdf.open("test.pdf")
for page in doc:
    print(page.get_text())

