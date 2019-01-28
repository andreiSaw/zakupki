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
        ppp = load_parse_purchase_page(stub=stub, p_id=p_id)
        temp_item.update(ppp)
        results.append(temp_item)
        logging.info("Parsed %s page" % p_id)
    return results


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
            t = clear_text(cells[4].text)

            lot = {"name": tmp,
                   "category": t[:t.find(" ")]}
            lots.append(lot)
    return lots, lots_num


def detect_protocol(soup):
    toolTipMenuDiv = soup.find_all("div", {"class": "toolTipMenu"})
    if len(toolTipMenuDiv) < 1:
        return None
    # detect version of protocol
    protocols = soup.find_all("span", {"class": "protocolName"})
    prot = [clear_text(el.text)[-1] for el in protocols]
    k = max(prot)
    ix = prot.index(k)
    logging.info(f'0{k}-protocol')
    targetTip = toolTipMenuDiv[ix]

    command = targetTip.find("li").get('onclick')
    link = command[command.find("\'") + 1:]
    link = link[:link.find("\'")]
    return link


def parse_xml_customer(soup):
    customer = {'fullName': "", 'inn': ""}
    customer_xml = soup.find('ns2:customer')
    if not customer_xml:
        return None
    for tag in customer.keys():
        cstag = customer_xml.find(tag)
        if not cstag:
            return None
        customer[tag] = customer_xml.find(tag).text
    date_xml = soup.find('ns2:createDateTime')
    customer["date"] = date_xml.text
    return customer


def parse_xml_supplier(soup):
    supplier1 = {"name": "", "inn": ""}
    supplier = soup.find("ns2:supplierInfo")
    for tag in supplier1.keys():
        supplier1[tag] = supplier.find(tag).text
    price = soup.find("ns2:price").text
    supplier1['price'] = price
    return supplier1


def parse_xml_applications(soup):
    applications = soup.findAll("ns2:application")
    for applic in applications:
        winnerIndication = applic.find("ns2:winnerIndication")
        if not winnerIndication:
            continue
        # first pos
        if winnerIndication.text == "F":
            supplier = parse_xml_supplier(applic)
            return supplier
    return None


def parse_xml_lots(soup):
    lots = []

    lotApplicationsList = soup.find('ns2:lotApplicationsList')
    aList = lotApplicationsList.findAll('ns2:protocolLotApplications')
    for protocolLotApplications in aList:
        lot1 = {'subject': "", 'initialSum': ""}
        # find lot data
        lot_xml = protocolLotApplications.find("ns2:lot")
        if not lot_xml:
            return None
        for tag in lot1.keys():
            attrs = lot_xml.find("ns2:" + tag)
            if not attrs:
                return None
            lot1[tag] = attrs.text
        # find applications data
        application = parse_xml_applications(protocolLotApplications)
        lot1['supplier'] = application
        lots.append(lot1)
    return lots


def load_parse_purchase_page(stub, p_id):
    plug = {"fullName": "", "inn": "", "lots": [], "lots_num": 0, }

    logging.info("Gathering #%s lot\' data" % p_id)

    l2, l2_num = parse_lots(stub, p_id)

    p_link = stub.get_purchase_tab(p_id=p_id, tab="protocols")
    page = load_page(stub=stub, p_link=p_link)
    soup = BeautifulSoup(page, features="lxml")

    link = detect_protocol(soup)
    if not link:
        return plug

    fulllink = stub.get_protocol_plug_link() % link
    logging.info("Loading %s" % fulllink)

    page = load_page(stub=stub, p_link=fulllink)
    soup = BeautifulSoup(page, features="lxml")
    xml_data = soup.find("div", {"id": "tabs-2"}).text
    if not xml_data:
        return plug

    soup = BeautifulSoup(xml_data, "xml")
    customer = parse_xml_customer(soup)
    if not customer:
        return plug
    plug.update(customer)

    lots = parse_xml_lots(soup)
    l1 = 0
    if not lots:
        lots = []
    else:
        i = 0
        l1 = len(lots)
        for t in lots:
            t['category'] = l2[i]["category"]
            i += 1

    plug['lots'] = lots
    plug['lots_num'] = l1
    return plug
