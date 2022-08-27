from setuptools import setup

setup(
    name = 'budget_insights',
    version = '0.1',
    description = 'Budget helper',
    author = 'Sam',
    author_email = 'sbriley.0@gmail.com',
    packages = ['budget_insights'],
    install_requires = [
        'matplotlib==3.4.3',
    ],
    entry_points = {
        'console_scripts': [
            'budget=budget_insights.gui:main'
        ]
    },
)