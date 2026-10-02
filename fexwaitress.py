import fexchange
import os
import waitress

os.makedirs(fexchange.DATA_DIR, exist_ok=True)
waitress.serve(fexchange.app, port=5000, url_scheme='https', 
               url_prefix='ifn653')

