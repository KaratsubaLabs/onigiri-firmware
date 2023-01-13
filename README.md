
# onigiri-firmware

collection of controller software for each esp8266 device that is used in
**project onigiri**

## devices

devices are each esp8266 enabled module, some potential ones include
- smart switch
- blind controller
- controllable 8 segment display
- music server volume controller (with rotary encoder + dot matrix as display)
- sensor module (bunch of sensors)

## setting up for development

esptool is used to flash firmware and ampy is used to transfer micropython code
onto the board. install both with
```sh
pip install esptool
pip install adafruit-ampy
```

the `yapf` linter/formatter is used, you can install it with:
```sh
pip install yapf
```

then install git hooks
```sh
just devsetup
```

finally, create your own local copy of `config.py`, which contains
configuration information. make sure to fill out variable values with ones that
are relevant to you.
```sh
cp config_example.py config.py
```

## flashing the micropython firmware

to get the esp8266 development board ready to run micropython, we need to flash
the micropython firmware

- [docs](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)
- [video tutorial](https://www.youtube.com/watch?v=j0hgKkwmSlw)

download the firmware from this [page](https://micropython.org/download/esp8266/) for the esp8266 board, and this [page](https://micropython.org/download/esp32/) for the esp32 board.
you can flash the firmware with
```sh
just esp8266_setup
```
or
```sh
just esp32_setup
```

now to get a REPL over serial
```sh
sudo picocom /dev/ttyUSB0 -b115200
```

to copy any python code over to the esp board, you can run
```sh
ampy --port /dev/ttyUSB0 put main.py main.py
```
