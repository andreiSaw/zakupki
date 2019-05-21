import re
import dateutil.parser


def clear_text(content):
    tmp = content.replace("\n", u' ').replace("\t", u' ').replace("\r", u' ').replace(u'\xa0', u' ')
    tmp = re.sub(' +', ' ', tmp).lstrip().rstrip()
    return tmp


def get_id_from_url(content):
    return content[content.find("regNumber=") + len("regNumber="):]


def create_query(content):
    return u"+".join(content.split(u' '))
