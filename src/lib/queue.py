import Queue

class Job:
    def __init__(self, priority, description=False):
        self.desc=description
        self.priority=priority # select a value between 0 and 1!

    def __cmp__(self, other):
        if not isinstance(other, Job)
            return None
        return cmp(self.priority, other.priority)


