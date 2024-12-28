# homeassistant-iotavx

configuration.yaml:

sensor:
  - platform: iotavx_avx1
    port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
    name: "IOTAVX AV Receiver Sensor" 

switch:
  - platform: iotavx_avx1
    port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
    name: "IOTAVX AV Receiver Switch"

button:
  - platform: iotavx_avx1
    port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
    name: "IOTAVX AV Receiver Button"

number:
  - platform: iotavx_avx1
    port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
    name: "IOTAVX AV Receiver Volume"

select:
  - platform: iotavx_avx1
    port: /dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0
    name: "IOTAVX AV Receiver Input Select"

automation:

alias: Update Volume Slider with Sensor Value
description: Update Volume Slider with Sensor Value.
triggers:
  - entity_id:
      - sensor.iotavx_avx1_volume
    trigger: state
conditions: []
actions:
  - action: number.set_value
    metadata: {}
    data:
      value: "{{ states.sensor.iotavx_avx1_volume.state }}"
    target:
      entity_id: number.volume_slider
