from bs4 import BeautifulSoup

from .textutils import *
from .util import *


def check_website_up(stub):
    p_id = "31807061497"
    url = stub.get_purchase_tab(p_id=p_id)
    print("loading  " + url)
    page = load_page(stub=stub, p_link=url)
    soup = BeautifulSoup(page, features="lxml")
    infopage = soup.find('div', {'class': "contentTabBoxBlock"})
    if infopage is None:
        return False
    return True


def load_search_page(stub, p):
    # TODO check what happens if site is down
    url = stub.get_search_page_url(p)
    return load_page(stub=stub, p_link=url)


def contain_purchase_data(text):
    htmlsoup = BeautifulSoup(text, features="lxml")
    purchase_list = htmlsoup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def load_page(stub, p_link):
    sess = stub.get_session()
    request = sess.get(p_link)
    return request.text


def parse_search_page(stub, filepath):
    """
    Parsing one single page to retrieve all data (purchase url, id, etc.)
    :param filepath:  saved page path
    :param session:
    :return: results[] represents all search entries from that page
    """
    results = []
    text = read_file(filepath)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        p_link = item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href')
        p_id = get_id_from_url(p_link)

        # TODO parse purchase online
        temp_item = {
            'purchase_link': p_link,
            'purchase_id': p_id
        }
        ppp = load_parse_purchase_page(stub=stub, p_id=p_id)
        temp_item.update(ppp)
        results.append(temp_item)
        print("Parsed %s page" % p_id)
    return results


def load_parse_purchase_page(stub, p_id):
    """
    Walk through purchase page and take first 3 divs then asks to get lots
    :param p_id: puchase id
    :param session:
    :return: dict element represents purchase
    """
    p_link = stub.get_purchase_tab(p_id=p_id)
    page = load_page(stub=stub, p_link=p_link)
    soup = BeautifulSoup(page, features="lxml")
    infopage = soup.find('div', {'class': "contentTabBoxBlock"})
    if infopage is None:
        raise Exception("Site is down")
    divs = infopage.find_all('div', {'class': "noticeTabBoxWrapper"})
    element = {}
    i = 0
    for div in divs:
        trs = div.find_all('tr')
        for tr in trs:
            row = [clear_text(el.text) for el in tr.find_all(['td', 'th']) if el.text]
            if len(row) > 1:
                clear_purchace_row(row, element)
        i += 1
        if i > 2:
            break
    element.update(parse_lots(stub=stub, p_id=p_id))
    return element


def parse_lots(stub, p_id):
    """
    Walk through purchase page and parse lots tab
    :param p_id: purchase id
    :param session:
    :return: dict {lots[],lots_num}
    """
    p_link = stub.get_purchase_tab(p_id=p_id, tab="lot-list")
    page = load_page(stub=stub, p_link=p_link)
    soup = BeautifulSoup(page, features="lxml")
    lotable = soup.find('table', {'id': 'lot'})
    if lotable is None:
        raise Exception("Site is down")
    trs = lotable.find('tbody').find_all('tr')
    lots_num, lots = 0, []
    for row in trs:
        cells = [el for el in row.find_all(['td', 'th']) if el.text]
        if len(cells) == stub.get_len_lot_list():
            tmp = clear_text(cells[1].find('a', {'class': "dLink epz_aware"}).text)
            lots_num += 1
            lot = {"name": tmp,
                   "category": clear_text(cells[5].text),
                   "price": clear_price(clear_text(cells[3].text))}
            lots.append(lot)
    return {"lots": lots, 'lots_num': lots_num}


def parse_protocols(stub, p_id):
    print("Gathering #%s lot\' data" % p_id)
    page = load_page(stub=stub, p_link=stub.get_purchase_tab(p_id=p_id, tab="protocols"))
    soup = BeautifulSoup(page, features="lxml")
    toolTipMenuDiv = soup.find("div", {"class": "toolTipMenu"})
    command = toolTipMenuDiv.find("li").get('onclick')
    link = command[command.find("\'") + 1:]
    link = link[:link.find("\'")]
    fulllink = stub.get_protocol_plug_link() % link
    print("Loading %s" % fulllink)
    page = load_page(stub=stub, p_link=fulllink)
    soup = BeautifulSoup(page, features="lxml")
    tabs1 = soup.find("div", {"id": "tabs-1"})
    trs = tabs1.find_all("tr")
    grades = {}
    i = 0
    k = -1
    for tr in trs:
        td_text = [td.text.strip() for td in tr.find_all("td")]
        grades[i] = td_text
        if "Выбор победителя:" in td_text:
            k = i
            break
        i += 1
    tds = trs[k].find_all("td")
    tds = [clear_text(td.text) for td in tds]
    if "Заявок нет" in tds:
        return "NA"
    trs2 = trs[k + 1].find("td").find("table").find_all("tr")
    return clear_text(trs2[1].text)
