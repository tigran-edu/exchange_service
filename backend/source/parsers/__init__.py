# from backend.source.parsers.am import *
from backend.source.parsers.ge import *
from collections import defaultdict
import sys
import inspect


def get_all_banks():
    banks = defaultdict(list)
    logging.info("INIT CONFIG")
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and "Bank" in name:
            country = str(obj).split(".")[-2]
            logging.info(f"Country: {country}, Bank: {name}")
            banks[country].append(obj())
    return banks
