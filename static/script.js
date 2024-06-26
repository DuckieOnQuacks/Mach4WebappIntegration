document.addEventListener("DOMContentLoaded", () => {
    let activeInputField = null;

    const btns = document.querySelectorAll(".pinpad-btn");
    const submitBtn = document.getElementById("submit-btn");
    const delBtn = document.getElementById("delete-btn");
    const startingPalletInput = document.getElementById('startingPallet');
    const endingPalletInput = document.getElementById('endingPallet');
    const result = document.getElementById("result");
    const buttonResult = document.getElementById("buttonResult");
    const zPosResult = document.getElementById("zPosResult");
    const xPosResult = document.getElementById("xPosResult");
    const yPosResult = document.getElementById("yPosResult");
    const getZPosBtn = document.getElementById("getZPos");
    const getXPosBtn = document.getElementById("getXPos");
    const getYPosBtn = document.getElementById("getYPos");
    const getStartingPalletBtn = document.getElementById("getStartingPallet");
    const getEndingPalletBtn = document.getElementById("getEndingPallet");
    const startingPalletSuccess = document.getElementById("startingPalletSuccess");
    const endingPalletSuccess = document.getElementById("endingPalletSuccess");

    btns.forEach(btn => {
        if (!btn.id.includes("submit-btn") && !btn.id.includes("delete-btn")) {
            btn.addEventListener("click", (e) => {
                if (activeInputField) {
                    activeInputField.value += e.target.value;
                }
            });
        }
    });

    submitBtn?.addEventListener("click", handleSubmit);
    delBtn?.addEventListener("click", handleDelete);
    startingPalletInput?.addEventListener('focus', () => activeInputField = startingPalletInput);
    endingPalletInput?.addEventListener('focus', () => activeInputField = endingPalletInput);

    document.getElementById('getIoStatusForm').addEventListener('submit', handleIOStatus);
    document.getElementById('cycleStart').addEventListener('click', toggleCycle);
    document.getElementById('enable').addEventListener('click', toggleEnable);
    getZPosBtn.addEventListener('click', getZPosition);
    getXPosBtn.addEventListener('click', getXPosition);
    getYPosBtn.addEventListener('click', getYPosition);
    getStartingPalletBtn.addEventListener('click', getStartingPalletValue);
    getEndingPalletBtn.addEventListener('click', getEndingPalletValue);

    function handleSubmit() {
        if (!activeInputField || !activeInputField.value.trim()) {
            alert("Please enter a value first");
            return;
        }
        const isStartingPallet = activeInputField.id === "startingPallet";
        const method = isStartingPallet ? submitStartingPallet : submitEndingPallet;
        method(activeInputField.value.trim());
        activeInputField.value = ""; // Reset the input
    }

    function handleDelete() {
        if (activeInputField?.value) {
            activeInputField.value = activeInputField.value.slice(0, -1);
        }
    }

    function submitStartingPallet(value) {
        postValue('/set_starting_pallet', { startingPallet: parseFloat(value) }, 'Starting pallet register set successfully.', 'Please enter a valid number for Starting Pallet.', startingPalletSuccess);
    }

    function submitEndingPallet(value) {
        postValue('/set_ending_pallet', { endingPallet: parseFloat(value) }, 'Ending pallet register set successfully.', 'Please enter a valid number for Ending Pallet.', endingPalletSuccess);
    }

    function handleIOStatus(e) {
        e.preventDefault();
        const ioPath = document.getElementById('ioPath').value;
        fetch('/get_io_status?path=' + encodeURIComponent(ioPath))
            .then(response => response.json())
            .then(data => {
                document.getElementById('ioResult').innerText = data.state !== undefined ? 'IO state: ' + (data.state ? 'Enabled' : 'Disabled') : 'Error: ' + data.error;
            })
            .catch(error => {
                document.getElementById('ioResult').innerText = 'Error: ' + error.message;
            });
    }

    function toggleCycle() {
        const isStarting = this.textContent.trim() === "Cycle Start";
        const route = isStarting ? '/cycle_start' : '/cycle_stop';
        fetch(route, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            buttonResult.innerText = data.success ? (isStarting ? 'Cycle started successfully.' : 'Cycle stopped successfully.') : 'Error: ' + data.error;
        })
        .catch(error => {
            buttonResult.innerText = 'Error: ' + error.message;
        });

        this.classList.toggle('btn-green');
        this.classList.toggle('btn-red');
        this.textContent = isStarting ? "Cycle Stop" : "Cycle Start";
    }

    function toggleEnable() {
        const isEnabled = this.textContent.trim() === "Enable";
        const route = isEnabled ? '/enable' : '/disable';
        fetch(route, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            buttonResult.innerText = data.success ? (isEnabled ? 'Enabled successfully.' : 'Disabled successfully.') : 'Error: ' + data.error;
        })
        .catch(error => {
            buttonResult.innerText = 'Error: ' + error.message;
        });

        this.textContent = isEnabled ? "Disable" : "Enable";
        this.classList.toggle('btn-green');
        this.classList.toggle('btn-red');
    }

    function getZPosition() {
        fetch('/get_z_position', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            zPosResult.innerText = data.success ? 'Z Position: ' + data.zPos : 'Error: ' + data.error;
        })
        .catch(error => {
            zPosResult.innerText = 'Error: ' + error.message;
        });
    }

    function getXPosition() {
        fetch('/get_x_position', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            xPosResult.innerText = data.success ? 'X Position: ' + data.xPos : 'Error: ' + data.error;
        })
        .catch(error => {
            xPosResult.innerText = 'Error: ' + error.message;
        });
    }

    function getYPosition() {
        fetch('/get_y_position', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            yPosResult.innerText = data.success ? 'Y Position: ' + data.yPos : 'Error: ' + data.error;
        })
        .catch(error => {
            yPosResult.innerText = 'Error: ' + error.message;
        });
    }

    function getStartingPalletValue() {
        fetch('/get_starting_pallet', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            const startingPalletResult = document.getElementById('startingPalletResult');
            startingPalletResult.innerText = data.success ? 'Starting Pallet: ' + data.startingPallet : 'Error: ' + data.error;
        })
        .catch(error => {
            const startingPalletResult = document.getElementById('startingPalletResult');
            startingPalletResult.innerText = 'Error: ' + error.message;
        });
    }

    function getEndingPalletValue() {
        fetch('/get_ending_pallet', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            const endingPalletResult = document.getElementById('endingPalletResult');
            endingPalletResult.innerText = data.success ? 'Ending Pallet: ' + data.endingPallet : 'Error: ' + data.error;
        })
        .catch(error => {
            const endingPalletResult = document.getElementById('endingPalletResult');
            endingPalletResult.innerText = 'Error: ' + error.message;
        });
    }

    function postValue(url, body, successMessage, errorMessage, successElement) {
        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(response => response.text())
        .then(text => {
            try {
                const data = JSON.parse(text);
                result.innerText = data.success ? successMessage : 'Error: ' + data.error;
                if (data.success) {
                    successElement.innerText = successMessage;
                    setTimeout(() => {
                        successElement.innerText = '';
                    }, 3000);
                }
            } catch (error) {
                result.innerText = 'Error: Invalid JSON response';
                console.error('Invalid JSON response:', text);
            }
        })
        .catch(error => {
            result.innerText = errorMessage + error.message;
        });
    }
});
