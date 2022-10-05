
shell:
    picocom /dev/ttyUSB0 -b115200

cp-lcd:
    ampy --port /dev/ttyUSB0 put main.py main.py
    ampy --port /dev/ttyUSB0 put lcd_module/config.py config.py
    ampy --port /dev/ttyUSB0 put lcd_module/server.py server.py 
    ampy --port /dev/ttyUSB0 put lcd_module/lcd.py lcd.py 

cp-switch:
    ampy --port /dev/ttyUSB0 put main.py main.py
    ampy --port /dev/ttyUSB0 put switch_module/config.py config.py
    ampy --port /dev/ttyUSB0 put switch_module/server.py server.py

cp-light:
    ampy --port /dev/ttyUSB0 put main.py main.py
    ampy --port /dev/ttyUSB0 put light_module/config.py config.py
    ampy --port /dev/ttyUSB0 put light_module/server.py server.py
    ampy --port /dev/ttyUSB0 put light_module/servo.py servo.py

devsetup:
    cp dev/hooks/* .git/hooks

fmt:
    yapf -i -r .
