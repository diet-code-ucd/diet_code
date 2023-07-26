from . import db, models

DATABASE = {
    'provider': 'mysql',
    'host': 'localhost',
    'user': 'its_admin',
    'password': 'test123',
    'db': 'its-mysql'
}

db.bind(DATABASE)
db.generate_mapping(create_tables=True)
