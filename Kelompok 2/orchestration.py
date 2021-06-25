from nameko.rpc import RpcProxy, rpc
from nameko.events import EventDispatcher,event_handler

class OrchestrationService:
    
    name = "orchestration_service"

    room_service = RpcProxy("room_service")
    booking_service = RpcProxy("booking_service")

    dispatch = EventDispatcher()

    resultgetroomtype = {
        'get_room_type':None
    }

    resultgettotal = {
        'get_total_room':None
    }

    resultaddroomtype = {
        'add_room_type':None
    }

    resultaddroom = {
        'add_room':None
    }

    resultcheckin = {
        'get_checkin':None

    }

    resultcancel = {
        'cancel_booking':None

    }

    resultbookingstatus = {
        'book_stat':None
    }

    # pubsub
    @rpc
    def dispatch_method(self,payload):
        self.dispatch("room_event",payload)

    # orchestration
    @rpc
    # get_room_type
    def get_room_type(self):
        resultgetroomtype={
            'get_room_type':self.room_service.get_all_roomtype(),
            
        }
        return resultgetroomtype

    @rpc
    def get_total_room(self):
        resultgettotal = {
            'get_total_room':self.room_service.get_count_room(),
        }
        return resultgettotal
    
    @rpc
    def add_room_type(self,_name, _price, _capacity, _last_update_by):
        resultaddroomtype = {
            'add_room_type':self.room_service.add_roomtype(_name, _price, _capacity, _last_update_by)
        }
        return resultaddroomtype

    @rpc
    def add_room(self,typeid, roomnum, updateby):
        resultaddroom={
            'add_room':self.room_service.add_room(typeid, roomnum, updateby)
        }
        return resultaddroom
    
    @rpc    
    def get_checkin(self,roomid):
        resultcheckin={
            'get_checkin':self.room_service.get_checkin_detail(roomid)
        }
        return resultcheckin

    # @rpc
    # def booking_status(self, type_id, idlogin):
    #     resultbookingstatus={
    #         'book_stat':self.booking_service.update_booking_status_from_room(type_id,idlogin)
    #     }
    #     return resultbookingstatus

    @rpc
    def cancel_booking(self, idbooking, idlogin):
       resultcancel = {
           'cancel_booking' : self.room_service.update_cancel_room_bybooking(idbooking, idlogin) and self.booking_service.update_booking_status_from_room(idbooking, idlogin)
       }
       return resultcancel

