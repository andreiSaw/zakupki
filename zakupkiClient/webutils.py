import logging

from bs4 import BeautifulSoup

from .textutils import *
from .util import *


def check_website_up(stub):
    p_id = stub.get_p_id_test()
    url = stub.get_purchase_tab(p_id=p_id)
    logging.info("loading  " + url)
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
    :param stub:
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
        ppp = load_parse_purchase_223_page(stub=stub, p_id=p_id)
        temp_item.update(ppp)
        results.append(temp_item)
        print("Parsed %s page" % p_id)
    return results


def load_parse_purchase_223_page(stub, p_id):
    """
    Walk through purchase page and take first 2 divs then asks to get lots
    :param p_id: puchase id
    :param stub:
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
        if i > 1:
            # parse two first blocks
            break
        i += 1
    element.update(parse_lots(stub=stub, p_id=p_id))
    return element


def parse_lots(stub, p_id):
    """
    Walk through purchase page and parse lots tab, get only that have category sequence in OKPD2 classifcation
    :param p_id: purchase id
    :param stub:
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
                   "category": clear_text(cells[4].text),
                   "price": clear_price(clear_text(cells[3].text))}
            lots.append(lot)
    return {"lots": lots, 'lots_num': lots_num}


def parse_protocols(stub, p_id):
    logging.info("Gathering #%s lot\' data" % p_id)
    page = load_page(stub=stub, p_link=stub.get_purchase_tab(p_id=p_id, tab="protocols"))
    soup = BeautifulSoup(page, features="lxml")
    toolTipMenuDiv = soup.find("div", {"class": "toolTipMenu"})
    if not toolTipMenuDiv:
        return "NA"
    command = toolTipMenuDiv.find("li").get('onclick')
    link = command[command.find("\'") + 1:]
    link = link[:link.find("\'")]
    fulllink = stub.get_protocol_plug_link() % link
    logging.info("Loading %s" % fulllink)
    page = load_page(stub=stub, p_link=fulllink)
    soup = BeautifulSoup(page, features="lxml")
    tabs1 = soup.find("div", {"id": "tabs-1"})
    trs = tabs1.find_all("tr")
    grades = {}
    i, k = 0, -1
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
    if not trs[k + 1].find("td").find("table"):
        return "TBD"
    trs2 = trs[k + 1].find("td").find("table").find_all("tr")
    return clear_text(trs2[1].text)


def parse_search_page_xml(stub, filepath):
    """
        Parsing one single page to retrieve all data (purchase url, id, etc.)
        :param filepath:  saved page path
        :param stub:
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
        ppp = load_parse_purchase_223_page_xml(stub=stub, p_id=p_id)
        temp_item.update(ppp)
        results.append(temp_item)
        logging.info("Parsed %s page" % p_id)
    return results


def load_parse_purchase_223_page_xml(stub, p_id):
    logging.info("Gathering #%s lot\' data" % p_id)
    p_link = stub.get_purchase_tab(p_id=p_id, tab="protocols")
    page = load_page(stub=stub, p_link=p_link)
    soup = BeautifulSoup(page, features="lxml")
    toolTipMenuDiv = soup.find("div", {"class": "toolTipMenu"})
    if not toolTipMenuDiv:
        return "NA"
    command = toolTipMenuDiv.find("li").get('onclick')
    link = command[command.find("\'") + 1:]
    link = link[:link.find("\'")]
    fulllink = stub.get_protocol_plug_link() % link
    logging.info("Loading %s" % fulllink)

    page = load_page(stub=stub, p_link=fulllink)
    soup = BeautifulSoup(page, features="lxml")
    xml_data = soup.find("div", {"id": "tabs-2"}).text
    if not xml_data:
        return "NA"

    soup = BeautifulSoup(xml_data, "xml")

    customer_attrs = {}
    customer = soup.find('ns2:customer')
    customer_tags = ['fullName', 'inn']
    for tag in customer_tags:
        customer_attrs[tag] = '{}'.format(customer.find(tag).text)

    lots = []
    lot_tags = ['subject', 'initialSum']
    supplier_tags = ["name", "inn"]

    lotApplicationsList = soup.find('ns2:lotApplicationsList')
    applicationsList = lotApplicationsList.findAll('ns2:protocolLotApplications')
    for app in applicationsList:
        lot_xml = app.find("ns2:lot")
        l_attrs = {}
        if not lot_xml:
            customer_attrs["lots"] = "NA"
            customer_attrs["lots_num"] = 0
            return customer_attrs
        for tag in lot_tags:
            l_attrs[tag] = lot_xml.find("ns2:" + tag).text
        for a in app.findAll("ns2:application"):
            winnerIndication = a.find("ns2:winnerIndication")
            if not winnerIndication:
                continue
            if winnerIndication.text == "F":
                supplier_attrs = {}
                supplier = a.find("ns2:supplierInfo")
                for tag in supplier_tags:
                    supplier_attrs[tag] = supplier.find(tag).text
                price = a.find("ns2:price").text
                l_attrs['price'] = price
                l_attrs['supplier'] = supplier_attrs
        lots.append(l_attrs)
    customer_attrs['lots'] = lots
    customer_attrs['lots_num'] = len(lots)
    return customer_attrs
