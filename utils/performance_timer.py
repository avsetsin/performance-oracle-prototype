from time import perf_counter


class PerformanceTimer:
    def __init__(self):
        self.last_tick = perf_counter()

    def tick(self):
        previous = self.last_tick
        self.last_tick = perf_counter()
        return "(in {time:.3f} sec)".format(time=self.last_tick - previous)
