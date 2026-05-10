class Queue:
    def __init__(self):
        self._data = []
        self._front = 0   # index of current front element

    def enqueue(self, value):
        self._data.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        value = self._data[self._front]
        self._front += 1

        # Periodically compact the list to avoid memory growth
        if self._front > 50 and self._front > len(self._data) // 2:
            self._data = self._data[self._front:]
            self._front = 0

        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._front]

    def size(self):
        return len(self._data) - self._front

    def is_empty(self):
        return self.size() == 0
