import time

# --- Simulated BMS Components ---

class HVAC:
    def __init__(self):
        self.temperature = 22.0 # Celsius
        self.setpoint = 21.0    # Celsius
        self.fan_speed = 'medium'

    def update(self):
        # Simple simulation: adjust temp towards setpoint
        if self.temperature > self.setpoint + 0.5:
            self.temperature -= 0.2
        elif self.temperature < self.setpoint - 0.5:
            self.temperature += 0.2
        print(f"HVAC: Temp={self.temperature:.1f}°C, Setpoint={self.setpoint}°C, Fan={self.fan_speed}")

class Lighting:
    def __init__(self):
        self.level = 50 # Percentage
        self.on = True

    def update(self):
        status = 'ON' if self.on else 'OFF'
        print(f"Lighting: Level={self.level}%, Status={status}")

# --- Simulated Communication Protocols ---

class BACnetSimulator:
    def __init__(self, hvac, lighting):
        self.hvac = hvac
        self.lighting = lighting
        print("BACnet Simulator Initialized")

    def read_hvac_temp(self):
        # Simulates reading a BACnet object (e.g., Analog Input for temperature)
        print("BACnet: Reading HVAC Temperature...")
        return self.hvac.temperature

    def write_hvac_setpoint(self, value):
        # Simulates writing to a BACnet object (e.g., Analog Output for setpoint)
        print(f"BACnet: Writing HVAC Setpoint to {value}°C...")
        self.hvac.setpoint = value

    def read_lighting_status(self):
        # Simulates reading a BACnet object (e.g., Binary Input for status)
        print("BACnet: Reading Lighting Status...")
        return self.lighting.on

class ModbusSimulator:
    def __init__(self, hvac):
        self.hvac = hvac
        print("Modbus Simulator Initialized")

    def read_register(self, address):
        # Simulates reading a Modbus register
        print(f"Modbus: Reading Register {address}...")
        if address == 101: # Example: HVAC Fan Speed Register
            return self.hvac.fan_speed
        return None

    def write_register(self, address, value):
        # Simulates writing to a Modbus register
        print(f"Modbus: Writing Register {address} with {value}...")
        if address == 102: # Example: HVAC Fan Speed Control Register
            self.hvac.fan_speed = value

class KNXSimulator:
    def __init__(self, lighting):
        self.lighting = lighting
        print("KNX Simulator Initialized")

    def send_telegram(self, group_address, payload):
        # Simulates sending a KNX telegram
        print(f"KNX: Sending Telegram to {group_address} with payload {payload}...")
        if group_address == '1/1/1': # Example: Lighting On/Off Group Address
            self.lighting.on = bool(payload)
        elif group_address == '1/1/2': # Example: Lighting Level Group Address
            self.lighting.level = payload

# --- Main Simulation Loop ---

if __name__ == "__main__":
    # Instantiate simulated building systems
    hvac_system = HVAC()
    lighting_system = Lighting()

    # Instantiate simulated BMS controllers for each protocol
    bacnet_controller = BACnetSimulator(hvac_system, lighting_system)
    modbus_controller = ModbusSimulator(hvac_system)
    knx_controller = KNXSimulator(lighting_system)

    print("\n--- Starting BMS Simulation ---")

    for i in range(5):
        print(f"\n--- Simulation Step {i+1} ---")

        # Simulate HVAC control via BACnet
        current_temp = bacnet_controller.read_hvac_temp()
        if current_temp > 21.5:
            bacnet_controller.write_hvac_setpoint(20.0)
        elif current_temp < 20.5:
            bacnet_controller.write_hvac_setpoint(22.0)

        # Simulate HVAC fan control via Modbus
        if hvac_system.temperature > 22.0:
            modbus_controller.write_register(102, 'high')
        else:
            modbus_controller.write_register(102, 'low')

        # Simulate lighting control via KNX
        if i % 2 == 0:
            knx_controller.send_telegram('1/1/1', 1) # Turn ON
            knx_controller.send_telegram('1/1/2', 75) # Set level to 75%
        else:
            knx_controller.send_telegram('1/1/1', 0) # Turn OFF

        # Update the actual systems based on controller actions
        hvac_system.update()
        lighting_system.update()

        time.sleep(1) # Pause for readability

    print("\n--- BMS Simulation Ended ---")
