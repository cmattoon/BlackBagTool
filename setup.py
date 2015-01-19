from setuptools import setup
config = {
    'name': 'BlackBagTool',
    'author': 'Curtis Mattoon',
    'author_email': 'cmattoon@cmattoon.com',
    'packages': ['bbtlib', 
                 'bbtlib.platforms', 
                 'bbtlib.applications', 
                 'bbtlib.passwords',
                 'bbtlib.contrib'
                 ],
    'scripts': ['bin/bbt-main'],
    'version': '0.1.0dev'
}
setup(**config)
