from database.db import db

stock_sector_table = db.Table('stock_sector', 
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.stock_id'), primary_key=True), 
    db.Column('sector_id', db.Integer, db.ForeignKey('sector.sector_id'), primary_key=True)
)

stock_exchange_table = db.Table('stock_exchange', 
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.stock_id'), primary_key=True), 
    db.Column('exchange_id', db.Integer, db.ForeignKey('exchange.exchange_id'), primary_key=True)
)

stock_index_table = db.Table('stock_index', 
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.stock_id'), primary_key=True), 
    db.Column('index_id', db.Integer, db.ForeignKey('index.index_id'), primary_key=True)
)


class Stock(db.Model):
    __tablename__ = 'stock'

    stock_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(50))
    market_capitalization = db.Column(db.Integer)
    isin = db.Column(db.String(20))
    symbol = db.Column(db.String(20))

    sectors = db.relationship('Sector', secondary=stock_sector_table)
    exchanges = db.relationship('Exchange', secondary=stock_exchange_table)
    indices = db.relationship('Index', secondary=stock_index_table)

    def __init__(self, name, country, market_capitalization, isin, symbol):
        self.name = name
        self.country = country
        self.market_capitalization = market_capitalization
        self.isin = isin
        self.symbol = symbol

    def serialize(self):
        return {
            'stock_id': self.stock_id,
            'name': self.name,
            'country': self.country,
            'market_capitalization': self.market_capitalization,
            'isin': self.isin,
            'symbol': self.symbol,
            'sectors': [],
            'exchanges': [],
            'indices': [],
        }

class Sector(db.Model):
    __tablename__ = 'sector'

    sector_id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, sector_id, language, name):
        self.sector_id = sector_id
        self.language = language
        self.name = name

    def serialize(self):
        return {
            'sector_id': self.sector_id,
            'language': self.language,
            'name': self.name,
        }

class Exchange(db.Model):
    __tablename__ = 'exchange'

    exchange_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(50))
    symbol = db.Column(db.String(20))

    def __init__(self, exchange_id, name, country, symbol):
        self.exchange_id = exchange_id
        self.name = name
        self.country = country
        self.symbol = symbol

    def serialize(self):
        return {
            'exchange_id': self.exchange_id,
            'name': self.name,
            'country': self.country,
            'symbol': self.symbol,
        }

class Index(db.Model):
    __tablename__ = 'index'

    index_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(50))

    def __init__(self, index_id, name, country):
        self.index_id = index_id
        self.name = name
        self.country = country

    def serialize(self):
        return {
            'index_id': self.index_id,
            'name': self.name,
            'country': self.country,
        }

