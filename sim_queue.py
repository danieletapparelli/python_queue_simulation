
class Event:
    def __init__(self, time_occ=None, event_type=None):
        
        self.time_occ = time_occ
        self.event_type = event_type
        self.next = None
        
    def printEvent(self):
        
        print("Event-time: ",self.time_occ,"Type: ", self.event_type)

    def getTimeEvent(self):
        return self.time_occ

    def getNext(self):
        return self.next

    def setNext(self,newnext):
        self.next = newnext


class Queue:
    def __init__(self):
        self.head = None
        self.finish = None
        
    def setFinish(self,finishval):
        self.finish = finishval
    
    def setStart(self, startval):
        self.head = startval

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

    def isEmpty(self):
        return self.head == None

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count
    
    def queueprint(self):
        printval = self.head
        while printval is not None:
            if printval.time_occ==self.finish.time_occ:
                print("End of the queue!")
                return
            
            printval.printEvent()
            printval = printval.next


# class Event:
#     def __init__(self, time_occ=None, event_type=None):
#         self.time_occ = time_occ
#         self.event_type = event_type
#         self.nextval = None
        
#     def printEvent(self):
        
#         print("Event-time: ",self.time_occ,"Type: ", self.event_type)

# class Queue:
#     def __init__(self):
#         self.headval = None
#         self.finishval = None
    
#     def queueprint(self):
#         printval = self.headval
#         while printval is not None:
#             if printval.time_occ==self.finishval.time_occ:
#                 print("End of the queue!")
#                 return
            
#             printval.printEvent()
#             printval = printval.nextval
        


def start():
    time = 0
    start_simulation = 0
    finish_simulation = 0
    packet_arrival = 0
    packet_departure = 0
    
    queue = Queue()
    queue.setStart(Event(1,"start"))
    queue.setFinish(Event(1000,"finish"))
    
    queue.add(Event(10,"diocarlo"))
    queue.add(Event(50,"diocarlo"))
    queue.add(Event(12,"diocarlo"))
    queue.add(Event(9,"diocarlo"))
    # start_event = Event(time+1,"start queue")
    # time = time + 1
    # finish_event = Event(1000,"finish queue")
    # trigger_event = Event(1000, "finish queue")
    # queue.headval = start_event
    # start_event.nextval = trigger_event
    
    
    # queue.finishval = finish_event
    
    #events = []
    
    #for i in range (5):
    #    time = time + 1 
    #    events.append(Event(time, "arrival"))
    
    #queue.headval = events[0]
    #events[0].nextval = events[1]    
    #events[1].nextval = events[2]  
    
    print(start_simulation,finish_simulation)
    queue.queueprint()
    print(time)


def main():
    start()
  

if __name__ == "__main__":
    main()
