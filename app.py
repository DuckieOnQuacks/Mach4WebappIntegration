import ctypes
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from pythonWrapper import Mach4Control

app = Flask(__name__)

# Initialize Mach4 control
dll_path = "C:\\Mach4Industrial\\Mach4IPC-x64.dll"
ip_address = "localhost"
mach4 = Mach4Control(dll_path, ip_address)

# Ensure IPC is set up at startup
try:
    mach4.do_connect()
except Exception as e:
    print(f"Initialization error: {e}")

@app.route('/set_starting_pallet', methods=['POST'])
def set_starting_pallet():
    data = request.json
    starting_pallet = data.get('startingPallet')

    if starting_pallet is None:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        mach4.set_pound_var(200, starting_pallet)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': True}), 200

@app.route('/set_ending_pallet', methods=['POST'])
def set_ending_pallet():
    data = request.json
    ending_pallet = data.get('endingPallet')

    if ending_pallet is None:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        mach4.set_pound_var(203, ending_pallet)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': True}), 200


@app.route('/get_starting_pallet', methods=['GET'])
def get_starting_pallet():
    try:
        starting_pallet = mach4.get_pound_var(201)
        return jsonify(success=True, startingPallet=starting_pallet)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_ending_pallet', methods=['GET'])
def get_ending_pallet():
    try:
        ending_pallet = mach4.get_pound_var(203)
        return jsonify(success=True, endingPallet=ending_pallet)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_io_status', methods=['GET'])
def get_io_status():
    io_path = request.args.get('path')
    if not io_path:
        return jsonify({'error': 'Invalid data'}), 400
    try:
        print(io_path)
        hIo = mach4.get_signal_handle(io_path)
        state = mach4.get_signal_state(hIo)
        return jsonify({'success': True, 'state': state}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/cycle_start', methods=['POST'])
def cycle_start():
    try:
        mach4.cycleStart()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/cycle_stop', methods=['POST'])
def cycle_stop():
    try:
        mach4.cycleStop()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/enable', methods=['POST'])
def enable():
    try:
        mach4.enable()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'success': True}), 200

@app.route('/disable', methods=['POST'])
def disable():
    try:
        mach4.disable()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'success': True}), 200

@app.route('/get_z_position', methods=['GET'])
def get_z_position():
    try:
        z_pos = mach4.getZPos()
        return jsonify(success=True, zPos=z_pos)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_x_position', methods=['GET'])
def get_x_position():
    try:
        x_pos = mach4.getXPos()  # Assuming 0 is the pound variable for X position
        return jsonify(success=True, xPos=x_pos)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_y_position', methods=['GET'])
def get_y_position():
    try:
        y_pos = mach4.getYPos() # Assuming 1 is the pound variable for Y position
        return jsonify(success=True, yPos=y_pos)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Initialization error: {e}")
