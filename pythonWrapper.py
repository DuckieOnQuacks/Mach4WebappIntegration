import ctypes

class Mach4Control:
    def __init__(self, dll_path, ip_address):
        self.dll = ctypes.cdll.LoadLibrary(dll_path)
        self.ip_address = ip_address.encode('utf-8')
        self.mInst = None
        self.connected = False

        # Define function prototypes
        self.dll.mcIpcInit.argtypes = [ctypes.c_char_p]
        self.dll.mcIpcInit.restype = ctypes.c_int

        self.dll.mcCntlGetPoundVar.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self.dll.mcCntlGetPoundVar.restype = ctypes.c_int

        self.dll.mcCntlSetPoundVar.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
        self.dll.mcCntlSetPoundVar.restype = ctypes.c_int

        self.dll.mcIoGetHandle.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
        self.dll.mcIoGetHandle.restype = ctypes.c_int

        self.dll.mcIoGetState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_bool)]
        self.dll.mcIoGetState.restype = ctypes.c_int
        
        self.dll.mcCntlCycleStart.argtypes = [ctypes.c_int]
        self.dll.mcCntlCycleStart.restype = ctypes.c_int
        
        self.dll.mcCntlCycleStop.argtypes = [ctypes.c_int]
        self.dll.mcCntlCycleStop.restype = ctypes.c_int
        
        self.dll.mcCntlEnable.argtypes = [ctypes.c_int, ctypes.c_bool]
        self.dll.mcCntlEnable.restype = ctypes.c_int
        
        self.dll.mcAxisGetPos.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self.dll.mcAxisGetPos.restype = ctypes.c_int

    def do_connect(self):
        if self.dll.mcIpcInit is not None:
            self.mInst = self.dll.mcIpcInit(self.ip_address)
            self.connected = (self.mInst != 0)
            if not self.connected:
                raise Exception("Failed to connect to Mach4")

    def load_gcode_file(self, file_path):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlLoadGcodeFile(self.mInst, file_path.encode('utf-8'))
        if result != 0:
            raise Exception(f"Failed to load G-code file: Error code {result}")

    def get_pound_var(self, param):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        value = ctypes.c_double()
        result = self.dll.mcCntlGetPoundVar(self.mInst, param, ctypes.byref(value))
        if result != 0:
            raise Exception(f"Failed to get pound variable #{param}: Error code {result}")
        return value.value

    def set_pound_var(self, param, value):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlSetPoundVar(self.mInst, param, value)
        if result != 0:
            raise Exception(f"Failed to set pound variable #{param}: Error code {result}")

    def get_signal_handle(self, signal_id):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        hIo = ctypes.c_void_p()
        result = self.dll.mcIoGetHandle(self.mInst, signal_id.encode('utf-8'), ctypes.byref(hIo))
        if result != 0:
            raise Exception(f"Failed to get IO handle for signal ID {signal_id}: Error code {result}")
        return hIo

    def get_signal_state(self, hIo):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        state = ctypes.c_bool()
        result = self.dll.mcIoGetState(hIo, ctypes.byref(state))
        if result != 0:
            raise Exception(f"Failed to get state for IO handle {hIo}: Error code {result}")
        return state.value

    def cycleStart(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlCycleStart(self.mInst)
        if result != 0:
            raise Exception(f"Failed to start, enable the machine first")
        
    def cycleStop(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlCycleStop(self.mInst)
        if result != 0:
            raise Exception(f"Failed to stop: Error code {result}")
        
    def enable(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlEnable(self.mInst, True)
        if result != 0:
            raise Exception(f"Failed to enable: Error code {result}")
        
    def disable(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        result = self.dll.mcCntlEnable(self.mInst, False)
        if result != 0:
            raise Exception(f"Failed to disable: Error code {result}")

    def getXPos(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        z_pos = ctypes.c_double()
        result = self.dll.mcAxisGetPos(self.mInst, 0, ctypes.byref(z_pos))
        if result != 0:
            raise Exception(f"Failed to get Z position: Error code {result}")
        return z_pos.value
    
    def getYPos(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        z_pos = ctypes.c_double()
        result = self.dll.mcAxisGetPos(self.mInst, 1, ctypes.byref(z_pos))
        if result != 0:
            raise Exception(f"Failed to get Z position: Error code {result}")
        return z_pos.value
    
    def getZPos(self):
        if self.mInst is None:
            raise Exception("Not connected to Mach4")
        z_pos = ctypes.c_double()
        result = self.dll.mcAxisGetPos(self.mInst, 2, ctypes.byref(z_pos))
        if result != 0:
            raise Exception(f"Failed to get Z position: Error code {result}")
        return z_pos.value
    
