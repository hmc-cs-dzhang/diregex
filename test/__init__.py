import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__)) + '/../src/'

sys.path.insert(0, src_path + "parser")
sys.path.insert(0, src_path + "ir")
sys.path.insert(0, src_path + "semantics")


