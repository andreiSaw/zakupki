import re

def clear_text_from_xml(content):
    tmp = content.replace("\n", u' ').replace("\t", u' ').replace("\r", u' ').replace(u'\xa0', u' ')
    tmp = re.sub(' +', ' ', tmp).lstrip().rstrip()
    return tmp


def clear_text(content):
    tmp = content.lower()
    tmp = re.sub("[^A-Za-zА-Яа-я0-9]+", " ", tmp)
    tmp = re.sub(' +', ' ', tmp).lstrip().rstrip()
    return tmp


def get_id_from_url(content):
    """

    :param content: url string
    :return: only id
    """
    return content[content.find("regNumber=") + len("regNumber="):]


def create_query(content):
    """

    :param content: string query with spaces
    :return: spaces are replaced with +
    """
    return u"+".join(content.split(u' '))
