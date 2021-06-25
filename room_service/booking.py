from nameko.rpc import rpc

import booking_dependencies

class BookingService:

    name = 'booking_service'

    database = booking_dependencies.Database()

    @rpc
    def get_all_room_type(self):
        room_types = self.database.get_all_room_type()
        return room_types

    @rpc
    def add_customer(self, name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, last_update, last_update_by):
        customer = self.database.add_customer(name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, last_update, last_update_by)
        return customer

    @rpc
    def get_all_customer(self):
        customer = self.database.get_all_customer()
        return customer

    @rpc
    def get_customer_by_id(self, id):
        customer = self.database.get_customer_by_id(id)
        return customer

    #BARUUUUUUUUUUUUUUUUUUUUUU
    @rpc
    def get_customer_by_citizenNum(self, ktp):
        customer = self.database.get_customer_by_citizenNum(ktp)
        return customer    

    #jadi dipake
    @rpc
    def add_booking (self, id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status):
        booking = self.database.add_booking(id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status)
        return booking
    
    #jadi dipake
    @rpc
    def update_booking_room(self, id_booking, id_room_new, id_room_type_new):
        updated_booking = self.database.update_booking_room(id_booking, id_room_new, id_room_type_new)
        return updated_booking
    
    #jadi dipake
    @rpc
    def get_booking_by_room(self, id_room, start_date, end_date):
        booking = self.database.get_booking_by_room(id_room, start_date, end_date)
        return booking

    #jadi dipake
    @rpc
    def get_booking_by_id(self, booking_id):
        booking = self.database.get_booking_by_id(booking_id)
        return booking


    @rpc
    def get_all_booking(self):
        booking = self.database.get_all_booking()
        return booking

     #BARUUUUUUUUUUUUUUUUUUUUUU
    @rpc
    def get_booking_by_id_customer(self, id_customer):
        booking = self.database.get_booking_by_id_customer(id_customer)
        return booking

    @rpc
    def add_service (self, name, cost, status, last_update, last_update_by):
        service = self.database.add_service(name, cost, status, last_update, last_update_by)
        return service

    @rpc
    def get_all_service(self):
        service = self.database.get_all_service()
        return service

    @rpc
    def get_service_by_id(self, id):
        service = self.database.get_service_by_id(id)
        return service

    @rpc
    def add_detail_booking (self, id_service, id_booking, qty, price):
        detail_booking = self.database.add_detail_booking(id_service, id_booking, qty, price)
        return detail_booking

    @rpc
    def get_all_detail_booking(self):
        detail_booking = self.database.get_all_detail_booking()
        return detail_booking

    @rpc
    def get_detail_booking_by_id(self, id):
        detail_booking = self.database.get_detail_booking_by_id(id)
        return detail_booking

    @rpc
    def get_all_service_by_booking_id(self, id):
        detail_service_booking = self.database.get_all_service_by_booking_id(id)
        return detail_service_booking

    #UNTUK KELOMPOK 3
    @rpc
    def update_bookingstatus_by_id(self, id, status):
        updated_booking = self.database.update_bookingstatus_by_id(id , status)
        return updated_booking
    
    @rpc
    def get_booking_by_status(self, status):
        return self.database.get_booking_by_status(status)

    @rpc
    def update_booking_status_from_room(self, type_id, idlogin):
        updated_booking_room =  self.database.update_booking_status_fromroom(type_id,idlogin)
        return updated_booking_room

    