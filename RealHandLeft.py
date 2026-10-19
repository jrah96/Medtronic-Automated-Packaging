
from realhand import L20
from realhand.exceptions import TimeoutError, ValidationError

import time

OPEN = [
    100, 85, 100, 100,  # Thumb
    50, 100, 100,      # Index
    50, 100, 100,      # Middle
    50, 100, 100,      # Ring
    50, 100, 100       # Pinky
]

READY = [
    27, 70, 100, 73,
    67, 96, 80,
    50, 100, 77,
    50, 94, 77,
    65, 94, 75
]

APPROACH = [
    64, 40, 100, 58,
	64, 84, 48,
	50, 98, 90,
	44, 98, 78,
	22, 96, 72
]

GRASP = [
    56, 45, 32, 84,
	6, 74, 34,
	38, 12, 8,
	38, 36, 24,
	100, 36, 24
]

DELAY = 2.0

hand = L20(
    side="left",
    interface_name="PCAN_USBBUS1",
    interface_type="pcan"
)

try:
    while True:
        for name, angles in [
            ("OPEN", OPEN),
            ("READY", READY),
            ("APPROACH", APPROACH),
            ("GRASP", GRASP)
        ]:
            print(name)
            hand.angle.set_angles(angles)
            time.sleep(DELAY)

        print("Cycle complete.\n")

except KeyboardInterrupt:
    print("\nStopping hand sequence...")

except TimeoutError:
    print("Communication timed out.")

except ValidationError as e:
    print(f"Invalid parameter: {e}")

finally:
    hand.close()
    print("Hand connection closed.")
