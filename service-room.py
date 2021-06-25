from nameko.rpc import rpc
import uuid

import db_dependencies

class ServiceRoom:
    
    name = "service_room"

    db = db_dependencies.DBProvider()

    @rpc
    def get_all_roomtype(self):
        result = self.db.get_all_roomtype()
        self.db.close_connection()
        return result

    @rpc
    def update_roomtype(self, typeid):
        result = self.db.update_room_type(typeid)
        self.db.close_connection()
        return result

    @rpc
    def add_roomtype(self, _name, _price, _capacity, _last_update_by):
        result = self.db.add_room_type(_name, _price, _capacity, _last_update_by)
        self.db.close_connection()
        return result

    @rpc
    def delete_roomtype(self, typeid):
        result = self.db.delete_room_type(typeid)
        self.db.close_connection()
        return result

    @rpc
    def get_count_room(self):
        result = self.db.get_count_room()
        self.db.close_connection()
        return result

    @rpc
    def update_room(self, roomid, idlogin):
        result = self.db.update_room(roomid, idlogin)
        self.db.close_connection()
        return result

    @rpc
    def add_room(self, typeid, roomnum, updateby):
        result = self.db.add_room(typeid, roomnum, updateby)
        self.db.close_connection()
        return result

    @rpc
    def delete_room(self, roomid):
        result = self.db.delete_room(roomid)
        self.db.close_connection()
        return result

    @rpc
    def get_checkin_detail(self, roomid):
        result = self.db.get_detail(roomid)
        self.db.close_connection()
        return result


    
    
            