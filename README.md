# IMU and GPS Fusion for Inertial Navigation

This project implements an Inertial Navigation System (INS) using sensor fusion of IMU (Inertial Measurement Unit) and GPS data. The system is designed to run on a Raspberry Pi and uses shared memory for inter-process communication.

## Main Components

### 1. main_imu.py

This Python script is responsible for:

- Reading data from the IMU (MPU-9250) and GPS module
- Calibrating the sensor data
- Writing the processed data to shared memory
- Handling GPS NMEA parsing

Key features:
- Uses the Madgwick algorithm for sensor fusion
- Implements calibration factors for IMU data
- Reads GPS data via serial communication
- Updates shared memory with sensor and GPS data

### 2. main.c

This C program is responsible for:

- Reading the sensor and GPS data from shared memory
- Applying the Madgwick AHRS algorithm for orientation estimation
- Converting quaternions to Euler angles
- Performing quaternion rotations

Key features:
- Implements the Madgwick AHRS algorithm
- Converts quaternions to Euler angles
- Uses shared memory for inter-process communication with the Python script
- Processes data at 100Hz

## Dependencies

### For main_imu.py:
- sysv_ipc
- pynmea2
- RPi.GPIO
- serial
- mpu9250_i2c (custom module)
- Madgwick (custom module)

### For main.c:
- myshm (custom module for shared memory operations)
- MadgwickAHRS (custom implementation of the Madgwick algorithm)
- quaternion_rotate (custom module for quaternion operations)

## Setup and Usage

1. Ensure all dependencies are installed.
2. Connect the IMU and GPS module to the Raspberry Pi.
3. Run the main_imu.py script to start data collection and processing.
4. Compile and run the main.c program to perform sensor fusion and orientation estimation.

## Notes

- The system is designed to run at 100Hz.
- Calibration factors are applied to the raw IMU data for improved accuracy.
- The GPS data is updated at a lower rate than the IMU data.
- Shared memory is used to pass data between the Python script and C program.

## Future Improvements

- Implement Kalman filtering for better sensor fusion
- Add error handling and logging
- Optimize performance for real-time applications
