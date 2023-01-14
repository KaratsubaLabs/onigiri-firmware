
usb_port := "/dev/ttyUSB0"

shell:
    picocom {{usb_port}} -b115200

esp8266_setup firmware_file:
    esptool.py --port {{usb_port}} erase_flash
    esptool.py --port {{usb_port}} write_flash --flash_size=detect -fm qio 0x00000 {{firmware_file}}

esp32_setup firmware_file:
    esptool.py --chip esp32 --port {{usb_port}} erase_flash
    esptool.py --chip esp32 --port {{usb_port}} --baud 460800 write_flash -z 0x1000 {{firmware_file}}

cp-lcd:
    ampy --port {{usb_port}} put main.py main.py
    ampy --port {{usb_port}} put lcd_module/config.py config.py
    ampy --port {{usb_port}} put lcd_module/server.py server.py 
    ampy --port {{usb_port}} put lcd_module/lcd.py lcd.py 

cp-switch:
    ampy --port {{usb_port}} put main.py main.py
    ampy --port {{usb_port}} put switch_module/config.py config.py
    ampy --port {{usb_port}} put switch_module/server.py server.py

cp-light:
    ampy --port {{usb_port}} put main.py main.py
    ampy --port {{usb_port}} put light_module/config.py config.py
    ampy --port {{usb_port}} put light_module/server.py server.py
    ampy --port {{usb_port}} put light_module/servo.py servo.py

cp-light-sock:
    ampy --port {{usb_port}} put main.py main.py
    ampy --port {{usb_port}} put light_module_sock/config.py config.py
    ampy --port {{usb_port}} put light_module_sock/server.py server.py

cp-curtain:
    ampy --port {{usb_port}} put main.py main.py
    ampy --port {{usb_port}} put curtain_module/config.py config.py
    ampy --port {{usb_port}} put curtain_module/server.py server.py
    ampy --port {{usb_port}} put curtain_module/motor.py motor.py

devsetup:
    cp dev/hooks/* .git/hooks

fmt:
    yapf -i -r .
