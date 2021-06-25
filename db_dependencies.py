from nameko.extensions import DependencyProvider

import pymysqlpool
import pymysql

from datetime import date

class RoomWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    # GET ALL ROOM TYPES
    def get_all_roomtype(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room_type'
        cursor.execute(sql)
        return cursor.fetchall()

    # UPDATE ROOM TYPE STATUS
    def update_room_type(self, type_id):
        updatedstat = 0

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room_type WHERE {}'.format(type_id)
        cursor.execute(sql)
        roomstat = cursor.fetchone()
        if(roomstat['status'] == 0):
            updatedstat = 1

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE room_type SET status = "{}" WHERE id = {}'.format(updatedstat, type_id)
        cursor.execute(sql)

        return "Room type {} updated!".format(type_id)

    # INSERT ROOM TYPE
    def add_room_type(self, name, price, capacity, last_update_by):
        result = ""
        todaydate = date.today().strftime("%Y-%m-%d")
        print(todaydate)
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        temp = 'SELECT * FROM room_type'
        cursor.execute(temp)
        tempp= cursor.fetchall()

        print(tempp)

        available = 0    
        for roomtype in tempp:
            if name == roomtype['name']:
                available = 1
                        
        if(available == 0):
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            sql = 'INSERT INTO room_type VALUES(default, "{}", "{}", "{}","{}","{}","{}")'.format(name, price, capacity,0,todaydate,last_update_by)
            cursor.execute(sql)
            result = "Add room type {} success.".format(name)
        else:
            result = "Room type already exist."
                       
        return result
    
    # DELETE ROOM TYPE
    def delete_room_type(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM room_type WHERE id = {}'
        sql = sql.format(id)
        cursor.execute(sql)
        return "Delete room type success."


    # GET HOW MANY ROOMS AVAILABLE
    def get_count_room(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT COUNT(id) AS qty FROM room WHERE status = 0'
        cursor.execute(sql)
        # print(sql['qty'])
        return cursor.fetchone()    

    # UPDATE ROOM STATUS
    def update_room(self, type_id, idlogin):
        todaydate = date.today().strftime("%Y-%m-%d")
        updatedstat = 0
        txtstat = "available"

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room WHERE id = {}'.format(type_id)
        cursor.execute(sql)
        roomstat = cursor.fetchone()
        if(roomstat['status'] == 0):
            updatedstat = 1
            txtstat = "unavailable"

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE room SET status = "{}", last_update = "{}", last_update_by = "{}" WHERE id = {}'.format(updatedstat, todaydate, idlogin, type_id)
        cursor.execute(sql)

        return "Room {} updated to {}.".format(type_id, txtstat)
    
    #INSERT ROOM
    def add_room(self, typeid, roomnum, updateby):
        result = ""
        todaydate = date.today().strftime("%Y-%m-%d")
        print(todaydate)
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room'
        cursor.execute(sql)
        room = cursor.fetchall()

        available = 0    
        for getroom in room:
            if roomnum == getroom['room_number']:
                available = 1
                        
        if(available == 0):
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            sql = 'INSERT INTO room VALUES(default, "{}", "{}", 0,"{}","{}")'.format(typeid, roomnum, todaydate,updateby)
            cursor.execute(sql)
            result = "Add room {} success.".format(roomnum)
        else:
            result = "Room already exist."
                       
        return result

    #DELETE ROOM
    def delete_room(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM room WHERE id = {}'
        sql = sql.format(id)
        cursor.execute(sql)
        return "Delete room success."

    # GET CHECK IN DETAIL REPORT
    def get_detail(self, room_id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        # sql = 'SELECT c.name, b.booking_date, b.start_date, b.end_date, r.room_number, rt.name, rt.price, rt.capacity FROM `booking` b JOIN room_type rt ON b.id_room_type = rt.id JOIN room r ON b.id_room = r.id JOIN customer c ON b.id_customer = c.id WHERE b.id_room = {}'.format(room_id)

        sql = 'SELECT * FROM `booking` b JOIN room_type rt ON b.id_room_type = rt.id JOIN room r ON b.id_room = r.id JOIN customer c ON b.id_customer = c.id WHERE b.id_room = {}'.format(room_id)
        cursor.execute(sql)
        res = cursor.fetchone()
        result = "Customer: {} \n Booking date: {} \n Checkin: {} | Checkout: {} \n Room number: {} \n Room type: {} | Rp. {} | Room capacity: {} person(s) ".format(res['c.name'], res['booking_date'], res['start_date'], res['end_date'], res['room_number'], res['name'], res['price'], res['capacity'])
        return result

    def close_connection(self):
        self.connection.close()

class DBProvider(DependencyProvider):

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
        return RoomWrapper(self.connection_pool.get_connection())