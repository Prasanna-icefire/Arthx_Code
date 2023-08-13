
# Import the required modules
import cv2
import numpy as np
import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil

# Connect to the vehicle
vehicle = connect("/dev/ttyAMA0", baud=921600, wait_ready=True)

# Define the aruco dictionary and parameters
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters_create()

# Define the camera parameters (adjust according to your camera)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
camera_distortion = np.array([0, 0, 0, 0, 0])

# Define the target distance from the marker in meters
target_distance = 1.0

# Define the target yaw angle in radians
target_yaw = 0.0

# Define the PID controller for distance error
kp_dist = 0.5 # proportional gain
ki_dist = 0.01 # integral gain
kd_dist = 0.1 # derivative gain
prev_dist_error = 0.0 # previous distance error
dist_integral = 0.0 # distance error integral

# Define the PID controller for yaw error
kp_yaw = 0.5 # proportional gain
ki_yaw = 0.01 # integral gain
kd_yaw = 0.1 # derivative gain
prev_yaw_error = 0.0 # previous yaw error
yaw_integral = 0.0 # yaw error integral

# Define a function to send attitude commands to the vehicle
def set_attitude(roll, pitch, yaw_rate, thrust):
    # Create the SET_ATTITUDE_TARGET mavlink message
    msg = vehicle.message_factory.set_attitude_target_encode(
        0, # time_boot_ms
        1, # target system
        1, # target component
        0b00000000, # type mask: bit 1 is LSB
        to_quaternion(roll, pitch), # attitude quaternion
        0, # body roll rate in radian/s
        0, # body pitch rate in radian/s
        yaw_rate, # body yaw rate in radian/s
        thrust # thrust between 0 and 1
    )
    # Send the message to the vehicle
    vehicle.send_mavlink(msg)

# Define a function to convert euler angles to quaternions
def to_quaternion(roll, pitch):
    cy = np.cos(target_yaw * 0.5)
    sy = np.sin(target_yaw * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)

    q = [0] * 4
    q[0] = cy * cr * cp + sy * sr * sp
    q[1] = cy * sr * cp - sy * cr * sp
    q[2] = cy * cr * sp + sy * sr * cp
    q[3] = sy * cr * cp - cy * sr * sp

    return q

# Arm and takeoff the vehicle (refer to dronekit documentation)
arm_and_takeoff(2)

# Set the vehicle mode to GUIDED_NOGPS
vehicle.mode = VehicleMode("GUIDED_NOGPS")

# Start the video capture from the camera (adjust according to your camera)
cap = cv2.VideoCapture(0)

# Loop until the user presses ESC key or the vehicle is not in GUIDED_NOGPS mode
while cv2.waitKey(1) != 27 and vehicle.mode.name == "GUIDED_NOGPS":
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from camera")
        break
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the aruco markers in the frame
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    # If at least one marker is detected
    if ids is not None and len(ids) > 0:
        # Estimate the pose of the first marker
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[0], 0.1, camera_matrix, camera_distortion)

        # Draw the marker and its axes on the frame
        cv2.aruco.drawDetectedMarkers(frame, corners)
        cv2.aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec[0], tvec[0], 0.1)

        # Calculate the distance from the marker in meters
        distance = np.linalg.norm(tvec[0])

        # Calculate the yaw angle from the marker in radians
        yaw = np.arctan2(tvec[0][0][0], tvec[0][0][2])

        # Calculate the distance error
        dist_error = target_distance - distance

        # Calculate the distance error integral
        dist_integral += dist_error

        # Calculate the distance error derivative
        dist_derivative = dist_error - prev_dist_error

        # Update the previous distance error
        prev_dist_error = dist_error

        # Calculate the yaw error
        yaw_error = target_yaw - yaw

        # Calculate the yaw error integral
        yaw_integral += yaw_error

        # Calculate the yaw error derivative
        yaw_derivative = yaw_error - prev_yaw_error

        # Update the previous yaw error
        prev_yaw_error = yaw_error

        # Calculate the roll command using PID controller for distance error
        roll = kp_dist * dist_error + ki_dist * dist_integral + kd_dist * dist_derivative

        # Limit the roll command to [-1, 1] range
        roll = np.clip(roll, -1, 1)

        # Calculate the yaw rate command using PID controller for yaw error
        yaw_rate = kp_yaw * yaw_error + ki_yaw * yaw_integral + kd_yaw * yaw_derivative

        # Limit the yaw rate command to [-1, 1] range
        yaw_rate = np.clip(yaw_rate, -1, 1)

        # Set the pitch command to zero
        pitch = 0.0

        # Set the thrust command to a constant value
        thrust = 0.5

    else:
        # No marker is detected, hover in place
        roll = 0.0
        pitch = 0.0
        yaw_rate = 0.0
        thrust = 0.5
    
    # Send the attitude command to the vehicle
    set_attitude(roll, pitch, yaw_rate, thrust)

    # Display the frame on the screen
    cv2.imshow("Frame", frame)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Land and close the vehicle connection
vehicle.mode = VehicleMode("LAND")
vehicle.close()
