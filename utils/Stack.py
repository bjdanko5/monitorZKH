class Stack:
    def __init__(self):
        self.items = []
        self.up_path = []
        self.down_path = []

    def push(self, item):
        self.items.append(item)
        self.up_path.append(len(self.items))

    def pop(self):
        if not self.is_empty():
            self.down_path.append(len(self.items))
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