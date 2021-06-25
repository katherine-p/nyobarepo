from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher

class CalculationService:
    name = "calculation_service"

    service_room = RpcProxy("service_room")
    booking = RpcProxy("booking_service")

    dispatch = EventDispatcher()

    @rpc
    def cancel_booking(self, num):
       result = {
           'is_prime': self.service_room.update_cancel_room(num),
           'is_palundrome': self.palindrome_service.is_palindrome(num),
           'cancel_booking' : self.service_room.update_cancel_room(num) and self.palindrome_service.is_palindrome(num)

       }

       return result


