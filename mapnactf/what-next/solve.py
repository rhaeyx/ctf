#!/usr/bin/python3

from random import *
from Crypto.Util.number import *

KEY = 23226475334448992634882677537728533150528705952262010830460862502359965393545
enc = 2290064970177041546889165766737348623235283630135906565145883208626788551598431732

print(long_to_bytes(KEY ^ enc).decode())