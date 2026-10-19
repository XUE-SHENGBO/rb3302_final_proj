#!/usr/bin/env python3
# /usr/local/bin/rplidar_motor_daemon.py

import serial
import os
import time
import signal
import sys

PORT       = '/dev/rplidar'
WANTS_PORT = '/tmp/rplidar_node_wants_port'
STOP_FLAG  = '/tmp/rplidar_motor_stop'

ser = None

def hold_rts_low():
    global ser
    while True:
        try:
            ser = serial.Serial(PORT, baudrate=115200, timeout=1)
            ser.setRTS(False)
            print("[motor_daemon] RTS low, motor off.")
            return ser
        except Exception as e:
            print(f"[motor_daemon] Failed to open port: {e}, retrying...")
            time.sleep(0.1)

def handle_sigterm(sig, frame):
    global ser
    print("[motor_daemon] SIGTERM received, exiting.")
    if ser and ser.is_open:
        ser.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

print("[motor_daemon] Starting...")

# Wait for device at boot
while not os.path.exists(PORT):
    print(f"[motor_daemon] Waiting for {PORT}...")
    time.sleep(0.5)

ser = hold_rts_low()

while True:
    # Check if device was unplugged
    if not os.path.exists(PORT):
        print("[motor_daemon] Device unplugged, waiting for replug...")
        if ser and ser.is_open:
            try:
                ser.close()
            except:
                pass
        # Wait for device to reappear
        while not os.path.exists(PORT):
            time.sleep(0.1)
        print("[motor_daemon] Device replugged, claiming port immediately...")
        # Claim port as fast as possible to pull RTS low
        ser = hold_rts_low()

    # Check if ROS node wants the port
    if os.path.exists(WANTS_PORT):
        print("[motor_daemon] Releasing port for rplidar node...")
        ser.close()
        os.remove(WANTS_PORT)

        # Wait for ROS node to finish
        while not os.path.exists(STOP_FLAG):
            # Also watch for unplug during node operation
            if not os.path.exists(PORT):
                print("[motor_daemon] Device unplugged during node operation.")
                break
            time.sleep(0.1)

        if os.path.exists(STOP_FLAG):
            os.remove(STOP_FLAG)

        print("[motor_daemon] Reclaiming port, setting RTS low...")
        time.sleep(0.2)
        ser = hold_rts_low()

    time.sleep(0.05)  # tighter polling loop for faster response