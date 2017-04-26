import os
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

from threading import Thread


GPIO.setmode(GPIO.BOARD)

COMMAND_LIGTH_ON = 'LIGHT_ON'
COMMAND_LIGTH_OFF = 'LIGHT_OFF'
COMMAND_STOP = 'STOP'

LIGHT_CHANNEL = 16
RED_LIGHT_CHANNEL = 18

GPIO.setup(LIGHT_CHANNEL, GPIO.OUT)
GPIO.setup(RED_LIGHT_CHANNEL, GPIO.OUT)

pipe_name = '/tmp/heimdall'


class Controller(object):

    _light_status = False
    _red_light_status = False
    _running = False

    def start(self):
        thread_commands = Thread(target=self._listen_to_commands)
        thread_onrunning = Thread(target=self._on_running)
        self._running = True
        thread_commands.start()
        thread_onrunning.start()

    def _listen_to_commands(self):
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        with open(pipe_name) as f:
            while self._running:
                command = f.read()
                if command:
                    command = command.rstrip('\r\n')
                    print ('Received: {0}'.format(command))
                    self.execute(command)
            os.remove(pipe_name)

    def _on_running(self):
        while self._running:
            time.sleep(1)
            if self.is_enlightening:
                self.red_light_off()
            else:
                self.red_light_on()
                time.sleep(0.2)
                self.red_light_off()
        GPIO.cleanup()

    @property
    def is_enlightening(self):
        return self._light_status

    def light_on(self):
        GPIO.output(LIGHT_CHANNEL, GPIO.HIGH)
        self._light_status = True

    def light_off(self):
        GPIO.output(LIGHT_CHANNEL, GPIO.LOW)
        self._light_status = False

    def red_light_on(self):
        GPIO.output(RED_LIGHT_CHANNEL, GPIO.HIGH)
        self._red_light_status = True

    def red_light_off(self):
        GPIO.output(RED_LIGHT_CHANNEL, GPIO.LOW)
        self._red_light_status = False

    def stop(self):
        self._running = False

    def execute(self, command):
        if command == COMMAND_LIGTH_ON:
            self.light_on()
        elif command == COMMAND_LIGTH_OFF:
            self.light_off()
        elif command == COMMAND_STOP:
            self.light_off()
            self.red_light_off()
            self.stop()
