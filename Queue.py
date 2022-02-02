class Queue:
    def __init__(self):
        self.front = None
        self.back = None

    #add element to queue
    def add(self,element):
        element = QueueElement(element)
        if self.front is None:
            self.front = element
            self.back = element
        else:
            self.back.next = element
            self.back = element

    #remove and return front element of queue
    def remove(self):
        out = self.front
        if self.front is None:
            return None
        self.front = self.front.next
        if self.front is None:
            self.back = None
        return out

    #return the items in the queue as an array
    def toArray(self):
        arr = []
        curr = self.front
        while curr != None:
            arr.append(curr)
            curr = curr.next
        return arr

    def __repr__(self):
        QStr = "["
        curr = self.front
        while curr != None:
            QStr += str(curr) + ", "
            curr = curr.next
        return QStr + "]"
    

#represents a queue element
class QueueElement:
    def __init__(self,val):
        self.val = val
        #next is the element in the queue after the current
        self.next = None

    def __repr__(self):
        return str(self.val)

