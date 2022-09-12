from setuptools import setup, find_packages

setup(
    name = 'transformo',
    version = '0.0.1',
    author = 'David Romero Organvídez',
    author_email = 'drorganvidez@us.es',
    description = 'A tool for database migration using software product lines',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/diverso-lab/transformo',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.10',
    install_requires = [
        'python-dotenv',
        'mysql-connector-python',
        'Jinja2',
    ]
)
