import serial
import threading

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)
        self.current_status = {
            "power": "OFF",
            "mute": False,
            "mode": "DIRECT",
        }
        self._start_reading_thread()

    def send_command(self, command):
        """Send a command to the receiver."""
        self.ser.write(f"'{command}'".encode())

    def _start_reading_thread(self):
        """Start a background thread to listen to the serial port."""
        threading.Thread(target=self._read_from_serial, daemon=True).start()

    def _read_from_serial(self):
        """Listen for updates from the serial port."""
        while True:
            try:
                response = self.ser.readline().decode().strip()
                if response == "DIM":
                    self.current_status["power"] = "ON"
                # Weitere Logik für andere Befehle kann hier hinzugefügt werden
            except Exception as e:
                print(f"Error reading from serial port: {e}")

    def get_status(self, key):
        """Retrieve the current status."""
        return self.current_status.get(key, None)

