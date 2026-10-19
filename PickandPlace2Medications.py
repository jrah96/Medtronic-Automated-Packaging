
from realhand import L20
from realhand.exceptions import TimeoutError, ValidationError

# Hand poses
OPEN = [
    90, 100, 100, 100,
    60, 100, 100,
    50, 100, 100,
    40, 100, 100,
    30, 100, 100
]

SPREAD = [
    100, 100, 100, 100,
    95, 100, 100,
    75, 100, 100,
    29, 100, 100,
    0, 100, 100
]

ONE_FINGER_PREGRAB = [
    21, 70, 100, 52,
    75, 100, 100,
    51, 0, 0,
    54, 0, 0,
    50, 0, 0
]

ONE_FINGER_GRAB = [
    21, 70, 90, 52,
    75, 0, 55,
    51, 0, 0,
    54, 0, 0,
    50, 0, 0
]

OPEN_RING_PINKY = [
    21, 57, 82, 52,
    50, 0, 55,
    51, 0, 0,
    40, 100, 5,
    40, 100, 16
]

OPEN_RING_PINKY_TIPS = [
    21, 57, 82, 52,
    50, 0, 55,
    51, 0, 0,
    60, 100, 45,
    15, 100, 65
]

CLOSE_PINKY_ABDUCTION = [
    21, 57, 82, 52,
    50, 0, 55,
    51, 0, 0,
    30, 100, 45,
    100, 100, 65
]

OPEN_PINKY = [
    21, 57, 82, 52,
    50, 0, 55,
    51, 0, 0,
    30, 100, 45,
    0, 100, 65
]

RELEASE = [
    21, 52, 100, 52,
    50, 100, 100,
    51, 0, 0,
    54, 0, 0,
    50, 0, 0
]

BACK_OPEN = [
    100, 100, 100, 100,
    50, 100, 100,
    50, 100, 100,
    50, 100, 100,
    50, 100, 100
]

# Sequence of poses
POSES = [
    ("OPEN", OPEN),
    ("SPREAD", SPREAD),
    ("TWO FINGER PREGRAB", ONE_FINGER_PREGRAB),
    ("TWO FINGER GRAB", ONE_FINGER_GRAB),
    ("OPEN RING AND PINKY", OPEN_RING_PINKY),
    ("OPEN RING AND PINKY TIPS", OPEN_RING_PINKY_TIPS),
    ("CLOSE PINKY ABDUCTION", CLOSE_PINKY_ABDUCTION),
    ("OPEN PINKY", OPEN_PINKY),
    ("TWO FINGER PREGRAB (RELEASE)", RELEASE),
    ("BACK OPEN", BACK_OPEN)
]

hand = None

try:
    hand = L20(
        side="left",
        interface_name="PCAN_USBBUS1",
        interface_type="pcan"
    )

    print("RealHand L20 connected.")
    print("Press ENTER to advance to the next pose.")
    print("Type Q and press ENTER to quit.\n")

    while True:
        for i, (name, angles) in enumerate(POSES, start=1):

            command = input(
                f"[{i}/{len(POSES)}] "
                f"Press ENTER for {name}: "
            )

            if command.strip().lower() == "q":
                raise KeyboardInterrupt

            print(f"Moving to {name}...")
            hand.angle.set_angles(angles)
            print(f"{name} command sent.\n")

        print("Sequence complete!")
        print("Restarting sequence...\n")

except KeyboardInterrupt:
    print("\nStopping hand sequence...")

except TimeoutError:
    print("Communication timed out.")

except ValidationError as e:
    print(f"Invalid parameter: {e}")

finally:
    if hand is not None:
        hand.close()
        print("Hand connection closed.")
