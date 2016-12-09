import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(src_path, 'parser'))
sys.path.insert(0, os.path.join(src_path, 'ir'))
sys.path.insert(0, os.path.join(src_path, 'semantics'))

__all__ = ['parser', 'ir', 'semantics']


