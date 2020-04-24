import random


class Event:
    def __init__(self,id_pack, time_occ=None, event_type=None):
        self.id_pack = id_pack
        self.time_occ = time_occ
        self.event_type = event_type
        self.next = None
        
    def printEvent(self):
        
        print("Event-ID:",self.id_pack," Event-time: ",self.time_occ,"secs Type: ", self.event_type)

    def getTimeEvent(self):
        return self.time_occ
    
    def getID(self):
        return self.id_pack

    def getNext(self):
        return self.next

    def setNext(self,newnext):
        self.next = newnext

class Server:
    def __init__(self):
        self.status = 0
        self.service_time = 0
        self.departure_time = 0
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status
    
    def setServiceTime(self, service_time):
        self.service_time = service_time


class Queue:
    def __init__(self):
        self.head = None
        self.finish = None
        
    def setFinish(self,finishval):
        self.finish = finishval
    
    def setStart(self, startval):
        self.head = startval
    
    def getFinish(self):
        return self.finish.time_occ
    
    def getStart(self):
        return self.head
    
    def getFirtsPacket(self):
        if self.head == None:
            print("coda vuota")
        else:
            
            temp = self.head
            self.head = temp.getNext()
            
            return temp

    def search(self,item):
        current = self.head
        found = False
        stop = False
        while current != None and not found and not stop:
            if current.getTimeEvent() == item.time_occ:
                found = True
            else:
                if current.getTimeEvent() > item.time_occ:
                    stop = True
                else:
                    current = current.getNext()

        return found

    def add(self,event):
        current = self.head
        previous = None
        stop = False
        while current != None and not stop:
            if current.getTimeEvent() > event.time_occ:
                stop = True
            else:
                previous = current
                current = current.getNext()

        temp = event
        if previous == None:
            temp.setNext(self.head)
            self.head = temp
        else:
            temp.setNext(current)
            previous.setNext(temp)

    def isNotEmpty(self):
        return self.head != None
    
        

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count
    
    def queueprint(self):
        
        if(self.head==None):
            print("Queue is empty")
            return
        printval = self.head
        while printval is not None:
            if printval.time_occ==self.finish.time_occ:
                print("End of the queue!")
                return
            
            printval.printEvent()
            printval = printval.next



def start(lam, u):
    time = 0
    start_simulation = 0
    finish_simulation = 0
    packet_arrival = 1
    arrival_time = 0
    packet_departure = 0
    total_packet_processed = 0
    queue = Queue()
    queue.setStart(Event(1,1,"start"))
    queue.setFinish(Event(0,1000,"finish"))
    server = Server()
    server_time = 0
    time_dep = 0
    i = 1
    packet_to_schedule = None
    packet_in_server = 0
    number_of_packet_system = []
    
    while time<queue.getFinish() :
        time = time+1
        
        if time>arrival_time:
            arrival_time = arrival_time + random.expovariate(lam)
            i=i+1
            e = Event(i,arrival_time,"Arrival")
            packet_arrival = packet_arrival+1
            queue.add(e)
        
        print("-----------------------QUEUE STATUS--------------------------\n")
        print("Global Time: ",time,"secs")
        queue.queueprint()     
        print("-------------------------------------------------------------\n")
        

        if server.getStatus()==1:
            if time<time_dep:
                print("Server is Processing ID: ",packet_to_schedule.getID(),"\n")
                packet_in_server = 1
            else:
                print("Packet ID: ", packet_to_schedule.getID()," has been processed at time:", time,"secs")
                server.setStatus(0)
                packet_in_server = 0
            
        
        
        if server.getStatus()==0:
            if queue.isNotEmpty():
                print("-----------------------SERVER STATUS-------------------------\n")
                print("Packet-Processing ")
                server_time = server_time + random.expovariate(u)
                packet_to_schedule = queue.getFirtsPacket()
                print("ID Packet Scheduled: ", packet_to_schedule.getID())
                print("Server Processing Time: ",server_time,"secs")
                time_dep = (time + server_time)
                print("Expected Departure Time: ",time_dep,"secs\n")
                print("-------------------------------------------------------------\n")
                packet_departure = packet_departure + 1
                packet_in_server = 1
                server.setStatus(1)
        
        number_of_packet_system.append(queue.size()+packet_in_server)
        
    while queue.isNotEmpty():
        time = time + 1
        print("-----------------------QUEUE STATUS--------------------------\n")
        queue.queueprint()     
        print("-------------------------------------------------------------\n")

        if server.getStatus()==1:
            if time<time_dep:
                print("Server is Processing ID: ",packet_to_schedule.getID(),"\n")
                packet_in_server=1
            else:
                print("Packet ID: ", packet_to_schedule.getID()," has been processed at time:", time,"secs\n")
                server.setStatus(0)
                packet_in_server=0
            
        
        
        if server.getStatus()==0:
            if queue.isNotEmpty():
                print("-----------------------SERVER STATUS-------------------------\n")
                print("Packet-Processing ")
                server_time = server_time + random.expovariate(u)
                packet_to_schedule = queue.getFirtsPacket()
                print("ID Packet Scheduled: ", packet_to_schedule.getID())
                print("Server Processing Time: ",server_time,"secs")
                time_dep = (time + server_time)
                print("Expected Departure Time: ",time_dep,"secs\n")
                print("-------------------------------------------------------------\n")
                packet_departure = packet_departure + 1
                packet_in_server=1
                server.setStatus(1)
                
        number_of_packet_system.append(queue.size()+packet_in_server)

    
    print(number_of_packet_system)
    queue.queueprint()
    print("Packets Arrivals", packet_arrival, "Packets Departures", packet_departure)


def main():
    start(0.09,5)
  

if __name__ == "__main__":
    main()