from .parserinterface import ParserInterface
from .util import _dump_JSON_data, _checkDirectory_if_not_create
from .webutils import *


class Parser44(ParserInterface):
    def __init__(self, stub):
        self.__stub = stub

