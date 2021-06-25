import json
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from nameko.web.handlers import http

import db_dependencies

class ServiceRoom:    
    name = "room_service"

    db = db_dependencies.DBProvider()

    dispatch=EventDispatcher()

    @event_handler("orchestration_service", "room_event")
    def handle_event_method(self, payload):
        print(payload)

    @rpc
    def get_all_roomtype(self):
        result = self.db.get_all_room_type()
        self.db.close_connection()
        return result

    @rpc
    def update_room_type(self, typeid):
        result = self.db.update_room_type(typeid)
        self.db.close_connection()
        return result

    @rpc
    def add_roomtype(self, _name, _price, _capacity, _last_update_by):
        result = self.db.add_room_type(_name, _price, _capacity, _last_update_by)
        self.db.close_connection()
        return result

    @rpc
    def delete_room_type(self, typeid):
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
    def get_room_num(self, roomid):
        result = self.db.get_room_num(roomid)
        self.db.close_connection()
        return result

    @rpc
    def update_cancel_room(self, typeid, idlogin):
        result = self.db.update_cancel_room(typeid, idlogin)
        self.db.close_connection()
        return result

    @rpc
    def update_cancel_room_bybooking(self, idbook, idlogin):
        result = self.db.update_cancel_room_by_booking(idbook, idlogin)
        self.db.close_connection()
        return result

    
    
            