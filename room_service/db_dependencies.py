from nameko.extensions import DependencyProvider

import pymysqlpool
import pymysql

from datetime import date

class RoomWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    # GET ALL ROOM TYPES
    def get_all_room_type(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room_type'
        cursor.execute(sql)
        return cursor.fetchall()
    
    # GET ROOM TYPE BY ID
    def get_all_room_type_by_id(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM room_type WHERE id = {}'.format(id)
        cursor.execute(sql)
        return cursor.fetchall()

    # UPDATE ROOM TYPE STATUS BY ID
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
        # print(todaydate)
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        temp = 'SELECT * FROM room_type'
        cursor.execute(temp)
        tempp= cursor.fetchall()
        # print(tempp)
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
    
    # DELETE ROOM TYPE BY ID
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

    #DELETE ROOM BY ID
    def delete_room(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'DELETE FROM room WHERE id = {}'
        sql = sql.format(id)
        cursor.execute(sql)
        return "Delete room success."

    def get_room_num(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT room_number FROM room WHERE id = {}'
        sql = sql.format(id)
        cursor.execute(sql)
        return cursor.fetchone()

    #UPDATE CANCEL ROOM BY BOOKING ID
    def update_cancel_room_by_booking(self, id, idlogin):
        todaydate = date.today().strftime("%Y-%m-%d")

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE room SET status = {}, last_update = {}, last_update_by = {} WHERE id in (SELECT id_room FROM booking WHERE id = {})'.format(2, todaydate, idlogin, id)
        cursor.execute(sql)

        return "Room {} updated!".format(id)

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