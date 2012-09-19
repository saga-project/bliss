__author__    = "Klesti Muco"
__copyright__ = "Copyright 200 B.C.-2012, KlustKreations"
__license__   = "to kill"

import bliss.saga as saga
import os
import unittest
import random

############################################################################

class IQTests(unittest.TestCase):

     def iqFinder():
          print 'Your IQ is: ', randrange(50,250)
          return True
