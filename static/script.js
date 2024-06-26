document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('connectMach4').addEventListener('click', function() {
        fetch('/connect_mach4', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('connectionResult').textContent = 'Connected to Mach4 successfully!';
            } else {
                document.getElementById('connectionResult').textContent = 'Failed to connect to Mach4: ' + data.error;
            }
        })
        .catch(error => {
            document.getElementById('connectionResult').textContent = 'Error connecting to Mach4: ' + error;
        });
    });

    document.getElementById('getIoStatusForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const ioPath = document.getElementById('ioPath').value;
        fetch(`/get_io_status?path=${ioPath}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('ioResult').textContent = `IO Device State: ${data.state}`;
            } else {
                document.getElementById('ioResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('ioResult').textContent = `Error: ${error}`;
        });
    });

    document.getElementById('getZPos').addEventListener('click', function() {
        fetch('/get_z_position')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('zPosResult').textContent = `Z Position: ${data.zPos}`;
            } else {
                document.getElementById('zPosResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('zPosResult').textContent = `Error: ${error}`;
        });
    });

    document.getElementById('getXPos').addEventListener('click', function() {
        fetch('/get_x_position')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('xPosResult').textContent = `X Position: ${data.xPos}`;
            } else {
                document.getElementById('xPosResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('xPosResult').textContent = `Error: ${error}`;
        });
    });

    document.getElementById('getYPos').addEventListener('click', function() {
        fetch('/get_y_position')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('yPosResult').textContent = `Y Position: ${data.yPos}`;
            } else {
                document.getElementById('yPosResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('yPosResult').textContent = `Error: ${error}`;
        });
    });

    document.getElementById('cycleStart').addEventListener('click', function() {
        fetch('/cycle_start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('buttonResult').textContent = 'Cycle started successfully!';
            } else {
                document.getElementById('buttonResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('buttonResult').textContent = `Error: ${error}`;
        });
    });

    document.getElementById('enable').addEventListener('click', function() {
        fetch('/enable', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('buttonResult').textContent = 'Enabled successfully!';
            } else {
                document.getElementById('buttonResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('buttonResult').textContent = `Error: ${error}`;
        });
    });
});
