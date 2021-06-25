import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'room_gateway'

    room_rpc = RpcProxy('room_service')

    @http('GET', '/get_all_room_type')
    def get_room_type(self, request):
        roomtype = self.room_rpc.get_all_roomtype()
        return json.dumps(roomtype, default=str)
    
    @http('GET', '/get_room/<int:id_room>')
    def get_room(self, request, id_room):
        room = self.room_rpc.get_room_num(id_room)
        return json.dumps(room)
    
    @http('POST', '/add_room_type')
    def add_room_type(self, request):
        data = json.loads(request.get_data(as_text=True))
        new_roomtype = self.room_rpc.add_roomtype(data['name'], data['price'], data['capacity'], data['last_update_by']) 
        return new_roomtype

    @http('PUT', '/update_room_type')
    def update_room_type(self, request):
        data = json.loads(request.get_data(as_text=True))
        roomtype = self.room_rpc.update_roomtype(data['typeid'])
        return roomtype