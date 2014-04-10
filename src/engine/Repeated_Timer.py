# Taken from http://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
from threading import Timer

class Repeated_Timer():
    '''
    Creates a timer and starts, stops and runs an event at a given interval.
    @untestable -This module relies on timers and spawning threads which are unpredictable in a testing environment.
    '''
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        '''
        Used by start(self), this is the function that is called every self.interval seconds.
        It restarts the timer and then invokes the function specified by self.function.
        '''
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        '''
        Start the timer if it is not already running.
        '''
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        '''
        Stop the timer from running.
        '''
        self._timer.cancel()
        self.is_running = False
