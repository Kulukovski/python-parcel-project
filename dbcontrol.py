from sqldb import db

dbe = db()

dbe.validate_list()
dbe.retrieve_data()

print(f"Last ID used: {dbe.get_last_id()}")

dbe.close_table()
