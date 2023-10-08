from heapq import *


class StreamingMedian:
    def __init__(self):
        self.low = []
        self.high = []

    def add_value(self, val):
        if len(self.low) == len(self.high):
            ins = -heappushpop(self.low, -val)
            heappush(self.high, ins)
        else:
            ins = -heappushpop(self.high, val)
            heappush(self.low, ins)

    def median(self):
        if len(self.high) > len(self.low):
            return float(self.high[0])

        else:
            return float(self.high[0] - self.low[0]) / 2.0


if __name__ == "__main__":
    import numpy as np

    s_len = 40
    seq = np.random.randn(1, s_len)

    i = 1

    sm = StreamingMedian()

    while i < s_len:
        slice = seq[0, :i]
        sm.add_value(slice[-1])
        median = np.median(slice)

        assert sm.median() == median
        i += 1
