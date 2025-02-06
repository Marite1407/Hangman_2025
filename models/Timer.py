class Timer:
    def __init__(self, scheduled_callback, cancel_callback, interval, callback):
        """
        Ajasti, mis käivitab funktsiooni teatud intervalli tagant
        :param scheduled_callback: funktsioon mis planeerib uue ajastuse
        :param cancel_callback: funktsioon, mis tühistab ajastuse
        :param interval: ajaintervall millisekundites
        :param callback: funktsioon, mis kutsutakse pärast intervalli
        """

        self.scheduled_callback = scheduled_callback
        self.cancel_callback = cancel_callback
        self.interval = interval
        self.callback = callback
        self.timer_id = None

    def start(self):
        """käivitab ajasti"""
        self.stop()
        self.timer_id = self.scheduled_callback(self.interval, self._run)

    def stop(self):
        """peatab ajasti"""
        if self.timer_id:
            self.cancel_callback(self.timer_id)
            self.timer_id = None

    def _run(self):
        """käivitab callbacki ja jätkab ajastamist"""
        self.callback()
        self.start()

