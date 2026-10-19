
from cri_lib import CRIController
import time

robot = CRIController()
connected = False
motors_enabled = False

try:
    # Connect to the ReBeL
    print("Connecting to robot...")

    if not robot.connect("192.168.3.11", 3920):
        raise RuntimeError("Connection failed")

    connected = True
    time.sleep(2)

    # Check referencing
    robot.get_referencing_info()

    if robot.robot_state.referencing_state.global_state.name != "REFERENCED":
        raise RuntimeError("Robot is not fully referenced")

    # Acquire control
    if not robot.set_active_control(True):
        raise RuntimeError("Failed to acquire active control")

    # Enable motors
    input("\nClear workspace. Press ENTER to enable motors...")

    if not robot.enable():
        raise RuntimeError("Motor enable failed")

    motors_enabled = True

    # Official SDK readiness check
    if not robot.wait_for_kinematics_ready(10):
        raise RuntimeError("Robot is not ready for movement")

    # Allow positions to settle
    time.sleep(2)

    # Read current joint positions
    joints = robot.robot_state.joints_current

    current = [
        joints.A1,
        joints.A2,
        joints.A3,
        joints.A4,
        joints.A5,
        joints.A6
    ]

    target = current.copy()
    target[5] += 15.0

    print("\nCurrent joints:", current)
    print("Target joints: ", target)
    print(f"\nA6: {current[5]:.2f}° -> {target[5]:.2f}°")

    # Explicit confirmation before movement
    confirmation = input(
        "\nType MOVE to rotate A6 by +15 degrees: "
    )

    if confirmation != "MOVE":
        print("Movement cancelled.")
    else:
        print("\nMoving A6...")

        success = robot.move_joints(
            *target,
            0.0, 0.0, 0.0,
            velocity=5.0,
            wait_move_finished=True,
            move_finished_timeout=120
        )

        print("Movement command result:", success)

        time.sleep(1)
        print("Final joints:", robot.robot_state.joints_current)

finally:
    if connected:
        if motors_enabled:
            print("\nDisabling motors...")
            try:
                robot.disable()
            except Exception as e:
                print("Disable error:", e)

        robot.close()
        print("Disconnected.")