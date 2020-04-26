import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


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

    # def search(self,item):
    #     current = self.head
    #     found = False
    #     stop = False
    #     while current != None and not found and not stop:
    #         if current.getTimeEvent() == item.time_occ:
    #             found = True
    #         else:
    #             if current.getTimeEvent() > item.time_occ:
    #                 stop = True
    #             else:
    #                 current = current.getNext()

    #     return found

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
    packet_arrival = 0
   
    packet_departure = 0
    queue = Queue()
    # queue.setStart(Event(1,1,"start"))
    queue.setFinish(Event(0,1000,"finish"))
    server = Server()
    i = 1
    packet_to_schedule = None
    packet_in_server = 0
    number_of_packet_system = []
    waits = []
    next_arrival_time = random.expovariate(lam)
    next_service_time = 0
    total_next_arrival_time = next_arrival_time
    total_next_service_time = 0
    while time<queue.getFinish() :
        
        # print("this is the global time",time)
        
        
        if queue.isEmpty() or total_next_arrival_time <= total_next_service_time:
            if queue.isEmpty() and total_next_arrival_time >= total_next_service_time:
                packet_in_server = 0
            time = time + next_arrival_time
            i=i+1
            e = Event(i,time,"Arrival")
            packet_arrival = packet_arrival+1
            next_arrival_time = random.expovariate(lam)
            total_next_arrival_time = time + next_arrival_time
            queue.add(e)
            number_of_packet_system.append(queue.size()+packet_in_server)
       
       
        
                
        else:
            server.setStatus(1)
            # print("-----------------------SERVER STATUS-------------------------\n")
            # print("Packet-Processing ")
            
            time = time + next_service_time
            next_service_time = random.expovariate(u)
            total_next_service_time = time + next_service_time
            packet_to_schedule = queue.getFirtsPacket()
            # print("Service Time: ",next_service_time,"secs")
            # print("ID Packet Scheduled: ", packet_to_schedule.getID())
           
            wait = time  - packet_to_schedule.getTimeEvent()
            waits.append(wait)
            # print("-------------------------------------------------------------\n")
            packet_departure = packet_departure + 1
            packet_in_server = 1
        
        # print("-----------------------QUEUE STATUS--------------------------\n")
        # print("Global Time: ",time,"secs")
        # queue.queueprint()     
        # print("-------------------------------------------------------------\n")
           
        
        
        
    while queue.isNotEmpty():
        
        
        # print("-----------------------SERVER STATUS-------------------------\n")
        # print("Time: ",time)
        # print("Packet-Processing ")
        
        service_time = random.expovariate(u)
        time = time + service_time
        
        
        # print("ID Packet Scheduled: ", packet_to_schedule.getID())
        
        packet_to_schedule = queue.getFirtsPacket()
        wait = time  - packet_to_schedule.getTimeEvent()
        
        waits.append(wait)
        
        # print("-------------------------------------------------------------\n")
        packet_departure = packet_departure + 1
        packet_in_server = 1
        server.setStatus(1)
        
        
        number_of_packet_system.append(queue.size()+packet_in_server)
    
    average_wait = sum(waits)/len(waits)
    
    print("Average WAIT:",average_wait)
    average_number_packets = sum(number_of_packet_system)/len(number_of_packet_system)
   
    
 
    for i in range(len(number_of_packet_system)):
        plt.plot(i,number_of_packet_system[i],marker="|", color="blue")
        
    plt.ylabel("Number of Packets")
    plt.xlabel("Times (secs)")
    plt.show()
    print(average_number_packets)
    
 
    print("Packets Arrivals", packet_arrival, "Packets Departures", packet_departure)
    return average_number_packets, average_wait

def calc_theoretical_n_of_packet(lam,u):
    theor = (lam/u)/(1-(lam/u))
    return theor

def calc_theoretical_wait(lam,u):
    theor = ((lam/u)**2)/(lam*(1-(lam/u)))
    return theor

def main():
   


    lambda_2 = start(1,5)
    lambda_3 = start(2,5)
    lambda_4 = start(3,5)
    lambda_5 = start(4,5)
    
    steady_state1 = calc_theoretical_n_of_packet(1,5)
    steady_state2 = calc_theoretical_n_of_packet(2,5)
    steady_state3 = calc_theoretical_n_of_packet(3,5)
    steady_state4 = calc_theoretical_n_of_packet(4,5)
    
    plt.figure(" Figure for lambda=" )
    this_axis = plt.subplot()
    
    green_patch = mpatches.Patch(color='green', label='Simulation')
    red_patch = mpatches.Patch(color='red', label='Theorethical')
    plt.legend(handles=[green_patch,red_patch])
    
    this_axis.plot(1,lambda_2[0],'go', color="green")
    this_axis.plot(1,steady_state1,'bs', color="red")
    this_axis.plot(2,lambda_3[0],'go', color="green" )
    this_axis.plot(2,steady_state2,'bs', color="red")
    this_axis.plot(3,lambda_4[0],'go', color="green")
    this_axis.plot(3,steady_state3,'bs', color="red")
    this_axis.plot(4,lambda_5[0], 'go',color="green")
    this_axis.plot(4,steady_state4,'bs', color="red")
    this_axis.set_ylabel("Average Number of Packets")
    this_axis.set_xlabel("Lambda Value")
    plt.show()
    
    
    average_wait1 = calc_theoretical_wait(1,5)
    average_wait2 = calc_theoretical_wait(2,5)
    average_wait3 = calc_theoretical_wait(3,5)
    average_wait4 = calc_theoretical_wait(4,5)
   
    
    plt.figure(" Figure for lambda=" )
    blue_patch = mpatches.Patch(color='blue', label='Simulation')
    red_patch = mpatches.Patch(color='red', label='Theorethical')
    plt.legend(handles=[blue_patch,red_patch])
    this_axis2 = plt.subplot()
    
    this_axis2.scatter(1,lambda_2[1], color="blue")
    this_axis2.scatter(1,average_wait1, color="red")
    this_axis2.scatter(2,lambda_3[1], color="blue" )
    this_axis2.scatter(2,average_wait2, color="red")
    this_axis2.scatter(3,lambda_4[1], color="blue")
    this_axis2.scatter(3,average_wait3, color="red")
    this_axis2.scatter(4,lambda_5[1], color="blue")    
    this_axis2.scatter(4,average_wait4, color="red")
    this_axis2.set_ylabel("Average Wait (secs)")
    this_axis2.set_xlabel("Lambda Value")
    plt.show()
    
    
    

if __name__ == "__main__":
    main()
