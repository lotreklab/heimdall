from raspi.controller import Controller
from raspi.controller import COMMAND_LIGTH_ON, COMMAND_LIGTH_OFF, COMMAND_STOP
from raspi.controller import LIGHT_CHANNEL, RED_LIGHT_CHANNEL


def test_light_functions(mocker):

    GPIO = mocker.patch('raspi.controller.GPIO')

    c = Controller()

    assert c._light_status == False
    assert c._red_light_status == False

    c.light_on()
    assert c._light_status == True
    assert c._red_light_status == False
    GPIO.output.assert_called_with(LIGHT_CHANNEL, GPIO.HIGH)

    c.red_light_on()
    assert c._light_status == True
    assert c._red_light_status == True
    GPIO.output.assert_called_with(RED_LIGHT_CHANNEL, GPIO.HIGH)

    c.light_off()
    assert c._light_status == False
    assert c._red_light_status == True
    GPIO.output.assert_called_with(LIGHT_CHANNEL, GPIO.LOW)

    c.red_light_off()
    assert c._light_status == False
    assert c._red_light_status == False
    GPIO.output.assert_called_with(RED_LIGHT_CHANNEL, GPIO.LOW)


def test_commands(mocker):

    GPIO = mocker.patch('raspi.controller.GPIO')

    c = Controller()
    c._running = True

    assert c._light_status == False

    c.execute(COMMAND_STOP)
    assert c._running == False

    c.execute(COMMAND_LIGTH_ON)
    assert c.is_enlightening == True
    GPIO.output.assert_called_with(LIGHT_CHANNEL, GPIO.HIGH)

    c.execute(COMMAND_LIGTH_OFF)
    assert c.is_enlightening == False
    GPIO.output.assert_called_with(LIGHT_CHANNEL, GPIO.LOW)
