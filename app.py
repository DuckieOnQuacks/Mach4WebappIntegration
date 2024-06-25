from flask import Flask, render_template, request, jsonify
import ctypes

# Load the Mach4 DLL
mach4 = ctypes.cdll.LoadLibrary("C:\Mach4Industrial\Mach4Core.dll")

# Define API function prototypes for type safety
mach4.mcRegGetHandle.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
mach4.mcRegGetHandle.restype = ctypes.c_int

mach4.mcRegSetValue.argtypes = [ctypes.c_void_p, ctypes.c_double]
mach4.mcRegSetValue.restype = ctypes.c_int

mach4.mcRegGetValue.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
mach4.mcRegGetValue.restype = ctypes.c_int

app = Flask(__name__)

@app.route('/set_register', methods=['POST'])
def set_register():
    data = request.json
    register_path = data.get('path')
    value = data.get('value')
    
    if not register_path or value is None:
        return jsonify({'error': 'Invalid data'}), 400

    hReg = ctypes.c_void_p()
    rc = mach4.mcRegGetHandle(0, register_path.encode('utf-8'), ctypes.byref(hReg))
    if rc != 0:
        return jsonify({'error': f"Failed to get register handle: Error code {rc}"}), 500

    rc = mach4.mcRegSetValue(hReg, ctypes.c_double(value))
    if rc != 0:
        return jsonify({'error': f"Failed to set register value: Error code {rc}"}), 500

    return jsonify({'success': True}), 200

@app.route('/get_register', methods=['GET'])
def get_register():
    register_path = request.args.get('path')
    
    if not register_path:
        return jsonify({'error': 'Invalid data'}), 400

    hReg = ctypes.c_void_p()
    rc = mach4.mcRegGetHandle(0, register_path.encode('utf-8'), ctypes.byref(hReg))
    if rc != 0:
        return jsonify({'error': f"Failed to get register handle: Error code {rc}"}), 500

    value = ctypes.c_double()
    rc = mach4.mcRegGetValue(hReg, ctypes.byref(value))
    if rc != 0:
        return jsonify({'error': f"Failed to get register value: Error code {rc}"}), 500

    return jsonify({'value': value.value}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
