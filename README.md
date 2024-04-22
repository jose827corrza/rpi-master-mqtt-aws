# MQTT IoT AWS Core Project

This intends to be a functional fully online weather station, available for whole internet.

Using MQTT protocol to make it lighter, and according to other technologies used in Internet Of Things.


## In this repo

You can find the code that runs in the weather station "Raspberry Pi 4B". this microcontroller reads information comming from different sensors(listed below) that bring relevant information for forecasting.

- BMP280


The different magnitures measured with the mentioned before sensors are:

- Pressure

## Data Structure

```json
{
    "device": "rpi-master",
    "mode": "STATION",
    "signal": null,
    "data": {
        "pressure": {
            "value": "1023",
            "magnitude": "Pa"
        },
        "humidity": {
            "value": "80",
            "magnitude": "%"
        }
    }
}
```