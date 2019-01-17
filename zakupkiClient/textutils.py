import re
from string import punctuation

from .util import load_JSON_data


def clear_purchace_row(content, element):
    element[re.sub(' +', ' ', content[0])] = re.sub(' +', ' ', content[1])


def clear_price(content):
    """
    Removes words from price cell and kopeiki as well
    :param content:
    :return:
    """
    numbers = re.findall(r'\d+', content)
    return "".join(numbers[:-1])

def clear_text(content):
    tmp = content.replace("\n", "").replace("\t", "").replace("\r", "")
    tmp = re.sub(' +', ' ', tmp).lstrip().rstrip()
    return tmp

def get_id_from_url(content):
    return content[content.find("regNumber=") + len("regNumber="):]

def preprocess(stub, flag, data=None):
    if data is None:
        data = load_JSON_data(stub=stub, filename=stub.get_purchase_db_name())
    # lowers all
    text_lower = [text.lower() for text in data]
    # delete punctuation
    text_letters = [''.join(c for c in s if c not in punctuation) for s in text_lower]
    text_final = []
    if flag == "EN":
        text_final = [re.sub(r'[^A-Za-z]+', ' ', x) for x in text_letters]
    elif flag == "RU":
        text_final = [re.sub(r'[^А-Яа-я]+', ' ', x) for x in text_letters]
    return text_final