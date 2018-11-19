from zakupki.zakupkiapi.poisk import parse_page

if __name__ == '__main__':
    lst = parse_page("./user_data/page_1.html")
    print(lst[0])
