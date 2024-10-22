class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None
            #raise IndexError("Stack is empty")
    def peek_id(self):
        if not self.is_empty():
            return self.items[-1].get("id")
        else:
            return None
            #raise IndexError("Stack is empty")
    def peek_id_str(self):
        if not self.is_empty():
            return str(self.items[-1].get("id"))
        else:
            return ""
            #raise IndexError("Stack is empty")        
    #def clear_not_in_subsystem(self, id_subsystem):     
    #    if id_subsystem:
    #        self.items = [item for item in self.items if item.get("id_subsystem") == id_subsystem]        
    def get(self, index):
        if index < 0:
            raise IndexError("Index cannot be negative")
        if index >= len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]

    def is_empty(self):
        return len(self.items) == 0

    def __iter__(self):
        if self.is_empty():
            return iter([])
        return iter(self.items)
    def __repr__(self):
        return f"Stack({self.items})"
    
class DatumsParentStack(Stack):
    def __init__(self, id_subsystem=None):
        super().__init__()
        self.id_subsystem = id_subsystem
    def clear_not_in_subsystem(self):           
        if self.id_subsystem:
            self.items = [item for item in self.items if item.get("id_subsystem") == self.id_subsystem]        
    def set_id_subsystem(self,id_subsystem):           
         self.id_subsystem = id_subsystem
         self.clear_not_in_subsystem()
    def get_id_subsystem(self):           
         return self.id_subsystem
         
 