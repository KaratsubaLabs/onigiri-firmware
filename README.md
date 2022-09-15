
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
```
$ pip install esptool
$ pip install adafruit-ampy
```

the `yapf` linter/formatter is used, you can install it with:
```
$ pip install yapf
```

then install git hooks
```
just devsetup
```

finally, create your own local copy of `config.py`, which contains
configuration information. make sure to fill out variable values with ones that
are relevant to you.
```
$ cp config_example.py config.py
```

## flashing the micropython firmware

to get the esp8266 development board ready to run micropython, we need to flash
the micropython firmware

- [docs](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)
- [video tutorial](https://www.youtube.com/watch?v=j0hgKkwmSlw)

download the firmware from this [page](https://micropython.org/download/esp8266/).
erase the flash on the board with
```
$ esptool.py --port /dev/ttyUSB0 erase_flash
```

and now we can flash the firmware:
```
$ esptool.py --port /dev/ttyUSB0 write_flash --flash_size=detect -fm qio 0x00000 <firmware>.bin
```

now to get a REPL over serial
```
$ sudo picocom /dev/ttyUSB0 -b115200
```

to copy any python code over to the esp board, you can run
```
$ ampy --port /dev/ttyUSB0 put main.py main.py
```
