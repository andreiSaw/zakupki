import logging

from bs4 import BeautifulSoup

from .textutils import *
from .util import *
from .dbclient import DbApi


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
    html_soup = BeautifulSoup(text, features="lxml")
    purchase_list = html_soup.find('div', {'class': "registerBox registerBoxBank margBtm20"})
    return purchase_list is not None


def load_page(stub, p_link):
    sess = stub.get_session()
    request = sess.get(p_link)
    return request.text


def detect_protocol(soup):
    tool_tip_menu_div = soup.find_all("div", {"class": "toolTipMenu"})
    if len(tool_tip_menu_div) < 1:
        return None
    # detect version of protocol
    protocols = soup.find_all("span", {"class": "protocolName"})
    prot = [clear_text_from_xml(el.text)[-1] for el in protocols]
    k = max(prot)
    ix = prot.index(k)
    logging.info(f'0{k}-protocol')
    targetTip = tool_tip_menu_div[ix]

    command = targetTip.find("li").get('onclick')
    link = command[command.find("\'") + 1:]
    link = link[:link.find("\'")]
    return link


def build_xml_customer(soup):
    customer = {'fullName': "", 'inn': ""}
    customer_xml = soup.find('ns2:customer')
    if not customer_xml:
        logging.error('no customer')
        return None
    for tag in customer.keys():
        cs_tag = customer_xml.find(tag)
        if not cs_tag:
            logging.error('no customer tag ' + cs_tag)
            return None
        customer[tag] = customer_xml.find(tag).text

    customer['fullName'] = clear_text(customer['fullName'])

    return customer


def parse_xml_bid(soup):
    supplier_plug = {"name": None, "inn": None}
    bid_plug = {"bid_date": None, "price": None, "supplier": None}

    price = soup.find("ns2:price")
    if price:
        bid_plug['price'] = price.text
        del price

    date = soup.find("ns2:applicationDate")
    if date:
        bid_plug['bid_date'] = date.text
        del date

    s1 = soup.find("ns2:nonResidentInfo")
    if s1:  # if nonResidentInfo
        supplier_plug["name"] = clear_text_from_xml(s1.text)
    else:  # if resident
        supplier = soup.find("ns2:supplierInfo")
        if supplier:  # if supplier is specified
            for tag in supplier_plug.keys():
                xml_s = supplier.find(tag)
                if xml_s:
                    supplier_plug[tag] = xml_s.text
            supplier_plug['name'] = clear_text(supplier_plug['name'])

    bid_plug['supplier'] = supplier_plug
    return bid_plug


def parse_xml_applications(soup, guid):
    bids = []
    applications = soup.findAll("ns2:application")
    no_of_participants = 0
    for applic in applications:
        one_bid = parse_xml_bid(applic)
        winnerIndication = applic.find("ns2:winnerIndication")
        if winnerIndication and winnerIndication.text == "F":
            one_bid['winnerIndication'] = True
        else:
            one_bid['winnerIndication'] = False
        no_of_participants += 1
        one_bid['guid'] = guid
        bids.append(one_bid)
    logging.info(f'no_of_participants {no_of_participants}')
    return bids


def parse_xml_lots(soup):
    lots = []

    lotApplicationsList = soup.find('ns2:lotApplicationsList')  # Lots+Applications List
    protocolLotApplications = lotApplicationsList.findAll(
        'ns2:protocolLotApplications')  # lot + multiple applications combinations
    for protocolLotApplications in protocolLotApplications:  # for every lot and applications
        lot1 = {'subject': "", 'initialSum': "", "guid": ""}
        # find lot data
        lot_xml = protocolLotApplications.find("ns2:lot")  # find lot data
        if not lot_xml:
            return None
        for tag in lot1.keys():
            attrs = lot_xml.find("ns2:" + tag)
            if not attrs:
                return None
            lot1[tag] = attrs.text
        lot1['subject'] = clear_text(lot1['subject'])
        lot1['bids'] = parse_xml_applications(protocolLotApplications,
                                              lot1['guid'])  # find applications data
        lots.append(lot1)
    return lots


def parse_purchase(stub, **kwargs):
    purchase_plug = {"p_id": "", "inn": "", "lots": [], 'date': None}

    if kwargs is not None:
        if 'p_id' not in kwargs.keys():
            if 'p_link' not in kwargs.keys():
                raise KeyError
            else:
                purchase_plug['p_id'] = get_id_from_url(kwargs['p_link'])
        else:
            purchase_plug['p_id'] = kwargs['p_id']

    logging.info(f"Parsing {kwargs}")

    # logging.info("Gathering #%s lot\' data" % p_id)

    page = load_page(stub=stub, p_link=stub.get_purchase_tab(p_id=purchase_plug['p_id'], tab="protocols"))
    soup = BeautifulSoup(page, features="lxml")

    link = detect_protocol(soup)
    if not link:
        return purchase_plug

    link = stub.get_protocol_plug_link() % link
    logging.info("Loading %s" % link)

    page = load_page(stub=stub, p_link=link)
    soup = BeautifulSoup(page, features="lxml")
    xml_data = soup.find("div", {"id": "tabs-2"}).text
    if not xml_data:
        return purchase_plug

    soup = BeautifulSoup(xml_data, "xml")
    customer = build_xml_customer(soup)
    purchase_plug.update(customer)

    purchase_plug['date'] = soup.find("ns2:publicationDateTime").text

    lots = parse_xml_lots(soup)

    if lots:
        purchase_plug['lots'] = lots
    else:
        purchase_plug['lots'] = []

    logging.info(f"Done {purchase_plug['p_id']}")
    # dump to database
    DbApi().push(purchase_plug)


def parse_search_page(stub, filepath):
    """
        Parsing one single page to retrieve all data (purchase url, id, etc.)
        :param filepath:  saved page path
        :param stub:
        """
    text = read_file(filepath)

    soup = BeautifulSoup(text, features="lxml")
    purchase_list = soup.find('div', {'class': 'parametrs margBtm10'})
    items = purchase_list.find_all('div', {'class': ['registerBox registerBoxBank margBtm20']})
    for item in items:
        ppp = parse_purchase(stub=stub, p_link=item.find('td', {'class': 'descriptTenderTd'}).find('a').get('href'))
        print(ppp)
