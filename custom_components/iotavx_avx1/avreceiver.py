import serial
import threading

class AVReceiver:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=1)
        self.current_status = {
            "power": "OFF",
            "mute": False,
            "mode": "DIRECT",
            "volume": 0,  # Lautstärke wird hier gespeichert
        }
        self.callbacks = []
        self._start_reading_thread()

    def send_command(self, command):
        """Send a command to the receiver."""
        self.ser.write(f"'{command}'".encode())

    def register_callback(self, callback):
        """Register a callback to notify on status changes."""
        self.callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify all registered callbacks about a status update."""
        for callback in self.callbacks:
            callback()

    def _start_reading_thread(self):
        """Start a background thread to listen to the serial port."""
        threading.Thread(target=self._read_from_serial, daemon=True).start()

    def _read_from_serial(self):
        """Listen for updates from the serial port."""
        while True:
            try:
                response = self.ser.readline().decode().strip()
                if response.startswith("@14K"):
                    volume_raw = response[4:]
                    if volume_raw.isdigit():
                        volume = int(volume_raw) / 10.0
                        if volume != self.current_status["volume"]:
                            self.current_status["volume"] = volume
                            self._notify_callbacks()
                elif response == "DIM":
                    self.current_status["power"] = "ON"
                    self._notify_callbacks()
                # Weitere Logik für andere Befehle kann hier hinzugefügt werden
            except Exception as e:
                print(f"Error reading from serial port: {e}")

    def get_status(self, key):
        """Retrieve the current status."""
        return self.current_status.get(key, None)

