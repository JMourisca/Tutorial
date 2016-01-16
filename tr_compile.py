#!flaskenv/bin/python
import os
pybabel = 'flaskenv/bin/pybabel'
os.system(pybabel + ' compile -d ../app/translations')