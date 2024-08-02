<a href="https://www.buymeacoffee.com/qG6DdXgzah" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# homeassistant-solax-evc-proxy
Proxy integration to simulate Green/Smart functions of SolaX EVC without SolaX X3 Inverter. 

# Intended use
If you have SolaX X3 Inverter you don't need this. Your inverter is capable of all smart functions and is much better.

If you have incompatible or older inverter this integration should help you to simulate smart functions.
You have to be able to read or somehow calculate "Excess PV power".

# What is Excess PV power
I stick to definition which is used by SolaX X3.
Battery charge power is considered surplus and is included in Excess PV power.

## All following expressions are equivalent
Excess PV power = Generated PV power - House load
Excess PV power = Exported Grid power + Battery charge

# How Green mode works
EVC is trying to consume(feed to car) all Excess PV power. In ideal it should be 0, which means we heve no more PV power to use and maximum is going to car.
Car and charger limits apply. Minimum charging power is 5,5A (aprox 1200W). Maximum single phase is 16A or 32A (3600W or 7200W).
Car can limit power on its side.

If there is positive Excess PV, EVC will raise charging power.
If there is negative Excess PV, EVC will lower charging power.

# What is working (v1.0.0-Beta)
- read defined sensor to get "Excess PV power". You can use any HA sensor which has integer state.
- periodicaly write to Modbus TCP (unit=0 - broadcast write). Only Excess PV power registry is used.

None of this is tested in real. I'm going to wire it and test.

# Required wiring

EVC modbus A1B1 connected to Modbus TCP converter (Waveshare or similar). 
EVC configured to use Inverter as data source.

If you are testing with X3, you have to disconnect its Modbus from EVC during tests.
