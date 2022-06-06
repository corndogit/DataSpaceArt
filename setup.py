try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

req_file = open('requirements.txt')
requirements = []
for req in req_file.readlines():
    requirements.append(req.strip('\n'))
req_file.close()  # todo tidy this section up

config = {
    'description' : 'Data-driven pattern generation',
    'author': 'corndogit',
    'url': 'https://github.com/corndogit/DataSpaceArt',
    'author_email': 'contact@sferic.me',
    'version': '0.1-dev',
    'license': 'MIT',
    'install_requires': requirements,
    'scripts': [],
    'name': 'DataSpaceArt'
}

# setup(**config)