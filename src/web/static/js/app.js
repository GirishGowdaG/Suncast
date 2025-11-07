// SunCast Web Application
// Handles form submission and API communication
// 
// Author: Girish G
// GitHub: https://github.com/GirishGowdaG/

const API_URL = '/predict';

// Preset weather conditions
const presets = {
    sunny: {
        irradiance: 950.0,
        temp: 28.5,
        wind_speed: 3.2
    },
    cloudy: {
        irradiance: 350.0,
        temp: 22.0,
        wind_speed: 5.5
    },
    night: {
        irradiance: 0.0,
        temp: 15.0,
        wind_speed: 2.0
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    setupPresetButtons();
    setDefaultDateTime();
});

function initializeForm() {
    const form = document.getElementById('predictForm');
    form.addEventListener('submit', handleSubmit);
}

function setupPresetButtons() {
    const presetButtons = document.querySelectorAll('.btn-preset');
    presetButtons.forEach(button => {
        button.addEventListener('click', function() {
            const presetType = this.dataset.preset;
            applyPreset(presetType);
        });
    });
}

function setDefaultDateTime() {
    const now = new Date();
    // Round to next hour
    now.setHours(now.getHours() + 1);
    now.setMinutes(0);
    now.setSeconds(0);
    
    const datetimeLocal = now.toISOString().slice(0, 16);
    document.getElementById('timestamp').value = datetimeLocal;
}

function applyPreset(presetType) {
    const preset = presets[presetType];
    if (!preset) return;

    document.getElementById('irradiance').value = preset.irradiance;
    document.getElementById('temp').value = preset.temp;
    document.getElementById('wind_speed').value = preset.wind_speed;

    // If night preset, set time to midnight
    if (presetType === 'night') {
        const timestamp = document.getElementById('timestamp');
        const date = new Date(timestamp.value);
        date.setHours(2, 0, 0, 0);
        timestamp.value = date.toISOString().slice(0, 16);
    }
    // If sunny preset, set time to noon
    else if (presetType === 'sunny') {
        const timestamp = document.getElementById('timestamp');
        const date = new Date(timestamp.value);
        date.setHours(13, 0, 0, 0);
        timestamp.value = date.toISOString().slice(0, 16);
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    
    hideMessages();
    setLoading(true);

    const formData = getFormData();
    
    try {
        const prediction = await makePrediction(formData);
        displayResult(prediction, formData);
    } catch (error) {
        displayError(error.message);
    } finally {
        setLoading(false);
    }
}

function getFormData() {
    const timestamp = document.getElementById('timestamp').value;
    const irradiance = parseFloat(document.getElementById('irradiance').value);
    const temp = parseFloat(document.getElementById('temp').value);
    const wind_speed = parseFloat(document.getElementById('wind_speed').value);

    // Convert datetime-local to ISO format
    const isoTimestamp = new Date(timestamp).toISOString();

    return {
        timestamp: isoTimestamp,
        irradiance: irradiance,
        temp: temp,
        wind_speed: wind_speed
    };
}

async function makePrediction(data) {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

function displayResult(prediction, inputData) {
    const resultCard = document.getElementById('result');
    const predictionValue = document.getElementById('predictionValue');
    
    // Display prediction value
    predictionValue.textContent = prediction.prediction.toFixed(2);

    // Display input details
    const timestamp = new Date(inputData.timestamp);
    document.getElementById('resultTimestamp').textContent = 
        timestamp.toLocaleString('en-US', { 
            dateStyle: 'medium', 
            timeStyle: 'short' 
        });
    document.getElementById('resultIrradiance').textContent = 
        `${inputData.irradiance.toFixed(1)} W/m²`;
    document.getElementById('resultTemp').textContent = 
        `${inputData.temp.toFixed(1)} °C`;
    document.getElementById('resultWind').textContent = 
        `${inputData.wind_speed.toFixed(1)} m/s`;

    // Show result with animation
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayError(message) {
    const errorCard = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideMessages() {
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
}

function setLoading(isLoading) {
    const submitButton = document.querySelector('.btn-primary');
    const buttonText = submitButton.querySelector('.btn-text');
    const spinner = submitButton.querySelector('.spinner');

    if (isLoading) {
        submitButton.disabled = true;
        buttonText.textContent = 'Predicting...';
        spinner.style.display = 'inline-block';
    } else {
        submitButton.disabled = false;
        buttonText.textContent = 'Predict Power Output';
        spinner.style.display = 'none';
    }
}

// Add form validation feedback
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        if (this.validity.valid) {
            this.style.borderColor = '#e0e0e0';
        } else {
            this.style.borderColor = '#e63946';
        }
    });
});
