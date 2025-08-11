import time

class Sequence:
    def __init__(self, auto_clear_seconds=None):
        self.sequence = []
        self.auto_clear_seconds = auto_clear_seconds if auto_clear_seconds and auto_clear_seconds > 0 else None
        self.last_update_time = None
        
    def add(self, tile):
        self.sequence.append(tile)
        self.last_update_time = time.time()

    def clear(self):
        self.sequence.clear()
        self.last_update_time = time.time()

    def get_sequence(self): 
        if not self.sequence:
            return "(empty)"
        return " → ".join(self.sequence)

    def should_auto_clear(self):
        if not self.auto_clear_seconds or not self.last_update_time:
            return False
        return (time.time() - self.last_update_time) >= self.auto_clear_seconds
