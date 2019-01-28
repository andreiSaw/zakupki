from .parserv import ParserV
from .stub import Stub
from .textutils import (clear_text, clear_purchace_row, clear_price, get_id_from_url, preprocess)
from .util import (load_JSON_data, read_file, saving, iscategory)
from .webutils import (load_page, iscategory, parse_protocols, load_search_page, contain_purchase_data,
                       check_website_up)

__version__ = "0.1"
