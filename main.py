import json
from src.DAO.currencies_dao import CurrenciesDAO
from src.Database.sqlite_client import SQLiteClient


def main():
    # Opening JSON file
    f = open('src/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    dao = CurrenciesDAO(db)
    print(dao.get_concrete_currency('EUR'))


if __name__ == '__main__':
    main()
