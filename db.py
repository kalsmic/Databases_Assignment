from os import environ

import psycopg2
from psycopg2.extras import RealDictCursor




class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(environ.get('DATABASE_URL'))
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("connected")
            self.create_tables()
        except (Exception, psycopg2.Error) as e:
            print(e)

    def create_tables(self):
        """Creates tables in the database"""
        create_human_table = """CREATE TABLE if not exists Human
            (
            id   SERIAL PRIMARY KEY ,
            name  varchar(25) UNIQUE,
            address  varchar(100),
            age     int,
            single  BOOLEAN DEFAULT TRUE
            );"""
            
        create_simcard_table = """CREATE TABLE IF NOT EXISTS Simcard
            (
                serial SERIAL PRIMARY KEY,
                name VARCHAR(50),
                phone_number integer UNIQUE,
                service_provider VARCHAR(100),
                is_active BOOLEAN,
                human_id integer
                constraint human_id_pkey
                references Human
                on update cascade on delete cascade
            );"""
        self.cursor.execute(create_human_table)
        self.cursor.execute(create_simcard_table)
    

    def add_a_human(self,name,address,age,single):

        sql =f"""INSERT INTO Human (name,address,age,single)
              VALUES ('{name}','{address}','{age}','{single}')"""

        if self.check_if_human_exists(name)["count"]:
            return "Name already exists"
        else:
            self.cursor.execute(sql)
            return "Record inserted"
    

    def get_a_human_record(self,id):
        self.cursor.execute(f"SELECT * FROM Human where id='{id}'")
        result = self.cursor.fetchall()        
        return result
    
        
    def get_all_human_records(self):
       
        self.cursor.execute(f"SELECT * FROM Human")

        results = self.cursor.fetchall()

        return results

    def delete_a_human(self,id):
       
        delete_query = f"DELETE FROM Human where id='{id}'"
       
        if self.cursor.execute(delete_query):
            return f"Record with id '{id}' Successfully Deleted "
        else:
            return f"Record with id '{id}' does not exist "
    def edit_a_human_status(self,id,status):
       
        edit_query = f"UPDATE Human SET single ='{status}' WHERE id='{id}'"
       
        if self.cursor.execute(edit_query):
            return f"Record with id '{id}' Successfully updated "
        else:
            return f"Record with id '{id}' does not exist "

    def check_if_human_exists(self,name):
        self.cursor.execute(f"SELECT COUNT(*) FROM Human where name='{name}'")
        result = self.cursor.fetchone()
               
        return result

    def get_simcards(self):


        self.cursor.execute("""SELECT * FROM Simcard""")
        
        return self.cursor.fetchall()

    def get_simcard(self,id):
        self.cursor.execute(f"""SELECT * FROM Simcard WHERE human_id='{id}'""")
        
        return self.cursor.fetchall()

    def add_simcard(self,**kwargs):
        human_id = kwargs['human_id']
        name = kwargs['name']
        phone_number = kwargs['phone_number']
        service_provider = kwargs['service_provider']

        self.cursor.execute(f"""SELECT COUNT(*) FROM Human where id='{human_id}'""")
        
        if self.cursor.fetchone()['count']==1:
            self.cursor.execute(f"""INSERT INTO Simcard(name,phone_number, service_provider, human_id)
            VALUES('{name}','{phone_number}','{service_provider}','{human_id}')""")

    def delete_simcard(self,id):
        delete_query =f"""DELETE FROM Simcard where serial='{id}'"""
        if self.cursor.execute(delete_query):
            return "Simcard deleted"
        else:
            return "Error Deleting Simcard"
    

if __name__ == "__main__":
    
    db = Database()
    print(db.add_a_human("Mark","Kampala",19,"False"))
    print(db.add_simcard(name="arthur",phone_number="0772019937",service_provider="MTN",human_id=1))
    print(db.get_all_human_records())
    print(db.get_simcard(1))
    print(db.delete_simcard('1677223232'))
