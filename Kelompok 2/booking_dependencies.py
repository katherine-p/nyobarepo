from nameko.extensions import DependencyProvider

import pymysqlpool
import pymysql

from datetime import date

class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection
        
    def get_all_room_type(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM room_type"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'capacity': row['capacity'],
                'status': row['status'],
                'last_update' : row['last_update'],
                'last_update_by' : row['last_update_by']
            })
        cursor.close()
        return result

    def add_customer(self, name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, last_update, last_update_by):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO customer VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, last_update, last_update_by)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_customer = "SELECT id FROM customer ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_customer)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id
    
    def get_all_customer(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM customer"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'citizen_number': row['citizen_number'],
                'date_of_birth': row['date_of_birth'],
                'gender': row['gender'],
                'address' : row['address'],
                'email' : row['email'],
                'phone_number1' : row['phone_number1'],
                'phone_number2' : row['phone_number2'],
                'status' : row['status'],
                'last_update' : row['last_update'],
                'last_update_by' : row['last_update_by']
            })
        cursor.close()
        return result

    def get_customer_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM customer WHERE id = {}".format((id))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    #JADI DIPAKE
    def add_booking(self, id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO booking VALUES (NULL,%s,%s,%s,%s,NOW(),%s,%s,%s,%s)"
        val = (id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_booking = "SELECT id FROM booking ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_booking)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    #JADI DIPAKE
    def update_booking_room(self, id_booking, id_room_new, id_room_type_new):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE booking SET id_room_type = %s , id_room = %s where id = %s"
        val = (id_room_type_new, id_room_new, id_booking)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_updated_booking = "SELECT * FROM booking WHERE id = {}".format((id_booking))
        cursor.execute(sql_updated_booking)
        result = cursor.fetchone()
        cursor.close()
        
        return result

    def get_all_booking(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM booking"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'id_customer': row['id_customer'],
                'id_room_type': row['id_room_type'],
                'id_room': row['id_room'],
                'id_employee': row['id_employee'],
                'booking_date' : row['booking_date'],
                'start_date' : row['start_date'],
                'end_date' : row['end_date'],
                'description' : row['description'],
                'status' : row['status']
            })
        cursor.close()
        return result

    #BARUUUUUUUUUUUUUUUUUUUUUU
    def get_customer_by_citizenNum(self, ktp):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM `customer` WHERE citizen_number = {}".format((ktp))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    #BARUUUUUUUUUUUUUUUUUUUUUU
    def get_booking_by_id_customer(self, id_customer):
        cursor = self.connection.cursor(dictionary=True,buffered=True)
        sql = "SELECT * FROM booking WHERE id_customer = {}".format((id_customer))
        cursor.execute(sql)
        result=[]
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'id_customer': row['id_customer'],
                'id_room_type': row['id_room_type'],
                'id_room': row['id_room'],
                'id_employee': row['id_employee'],
                'booking_date' : row['booking_date'],
                'start_date' : row['start_date'],
                'end_date' : row['end_date'],
                'description' : row['description'],
                'status' : row['status']
            })
        cursor.close()
        return result


    #Jadi dipake
    def get_booking_by_room(self, id_room, start_date, end_date):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM booking WHERE ((%s BETWEEN start_date AND end_date) AND %s BETWEEN start_date AND end_date) AND id_room = %s AND status <> 3 AND status <> 2"
        val = (start_date, end_date, id_room)
        cursor.execute(sql, val)
        cursor.fetchall()
        result = cursor.rowcount
        print(result)
        cursor.close()
        if result == 0:
            return True
        else:
            return False

    def get_booking_by_id(self, booking_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM booking WHERE id = {}".format((booking_id))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def add_service(self, name, cost, status, last_update, last_update_by):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO service VALUES (NULL,%s,%s,%s,%s,%s)"
        val = (name, cost, status, last_update, last_update_by)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_service = "SELECT id FROM service ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_service)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    def get_all_service(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM service"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'cost': row['cost'],
                'status': row['status'],
                'last_update': row['last_update'],
                'last_update_by' : row['last_update_by']
            })
        cursor.close()
        return result

    def get_service_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM service WHERE id = {}".format((id))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def add_detail_booking(self, id_service, id_booking, qty, price):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO detail_booking VALUES (NULL,%s,%s,%s,%s)"
        val = (id_service, id_booking, qty, price)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_detail_booking = "SELECT id FROM detail_booking ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_detail_booking)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    def get_all_detail_booking(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM detail_booking"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'id_service': row['id_service'],
                'id_booking': row['id_booking'],
                'qty': row['qty'],
                'price': row['price']
            })
        cursor.close()
        return result

    def get_detail_booking_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM detail_booking WHERE id = {}".format((id))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def get_all_service_by_booking_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT name FROM service WHERE id = ANY(SELECT id_service FROM detail_booking WHERE id_booking = {})".format((id))
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    #UNTUK KELOMPOK 3
    def update_bookingstatus_by_id(self, id, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE booking SET status = %s where id = %s"
        val = (status, id)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_updated_booking = "SELECT * FROM booking WHERE id = {}".format((id))
        cursor.execute(sql_updated_booking)
        result = cursor.fetchone()
        cursor.close()
        
        return result
    
    def get_booking_by_status(self, status):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM booking WHERE status = {}".format((status))
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'id_customer': row['id_customer'],
                'id_room_type': row['id_room_type'],
                'id_room': row['id_room'],
                'id_employee': row['id_employee'],
                'booking_date' : row['booking_date'],
                'start_date' : row['start_date'],
                'end_date' : row['end_date'],
                'description' : row['description'],
                'status' : row['status']
            })
        cursor.close()
        return result
    
    def update_booking_status_fromroom(self, type_id, idlogin):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE booking SET status = {}, id_employee = {} WHERE id = {}'.format(2, idlogin,type_id)
        cursor.execute(sql)
    
        return "Room {} updated!".format(type_id)

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        config = {
            'host': 'localhost', 
            'user': 'root', 
            'password': '', 
            'database': 'hotel', 
            'autocommit': True
        }
        self.connection_pool = pymysqlpool.ConnectionPool(size=20, name='DB Pool', **config)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
