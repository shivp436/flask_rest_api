from setuptools import setup

setup(
    name='FLAK_REST_API',
    version='0.1',
    description='REST API using Flask, SQLAlchemy, and Marshmallow',
    author='Shivanand',
    author_email='',
    packages=['flask_rest_api'],
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-marshmallow',
        'marshmallow-sqlalchemy'
    ],
)
