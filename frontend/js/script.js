// State
let currentFacing = 'East';
let currentPropertyType = 'Apartment';

function handlePresetChange() {
    const preset = document.getElementById('preset-select').value;
    if (preset !== "Custom Input") {
        document.getElementById('additional-toggle').checked = true;
        toggleAdditionalRequirements();
        const citySelect = document.getElementById('city-tier-select');
        if (citySelect) citySelect.value = "Metro";
        
        if (typeof map !== 'undefined' && CITY_COORDS[preset]) {
            map.flyTo(CITY_COORDS[preset], 13, { duration: 1.5 });
        }
    } else {
        if (typeof map !== 'undefined') map.flyTo(CITY_COORDS["Custom Input"], 4, { duration: 1.5 });
    }
    calculatePrice();
}

function updateStepper(id, delta) {
    const el = document.getElementById(id + '-display');
    let val = parseInt(el.innerText);
    val += delta;
    if(val < 0) val = 0;
    el.innerText = val;
}

function setFacing(facing) {
    currentFacing = facing;
    document.querySelectorAll('.facing-btn').forEach(btn => {
        btn.className = "facing-btn bg-surface-container-highest text-on-surface-variant border-transparent hover:border-outline-variant py-2 rounded-lg text-sm border transition-all";
    });
    const selectedBtn = document.getElementById('facing-' + facing);
    selectedBtn.className = "facing-btn bg-primary-container text-on-primary-container border-primary py-2 rounded-lg text-sm font-bold border transition-all";
}

function setPropertyType(type) {
    currentPropertyType = type;
    document.querySelectorAll('.type-btn').forEach(btn => {
        btn.className = "type-btn bg-surface-container-highest text-on-surface-variant border-transparent hover:border-outline-variant py-2 rounded-lg text-sm border transition-all";
    });
    const selectedBtn = document.getElementById('type-' + type);
    selectedBtn.className = "type-btn bg-primary-container text-on-primary-container border-primary py-2 rounded-lg text-sm font-bold border transition-all";
}

function toggleAdditionalRequirements() {
    const isChecked = document.getElementById('additional-toggle').checked;
    const requirementsDiv = document.getElementById('additional-requirements');
    if (isChecked) {
        requirementsDiv.classList.remove('hidden');
        requirementsDiv.classList.add('flex');
    } else {
        requirementsDiv.classList.add('hidden');
        requirementsDiv.classList.remove('flex');
    }
}

async function calculatePrice() {
    // Extract values from UI
    const area = parseFloat(document.getElementById('area-slider').value);
    const bedrooms = parseFloat(document.getElementById('bedrooms-display').innerText);
    const floor = parseFloat(document.getElementById('floor-display').innerText);
    const parking = parseFloat(document.getElementById('parking-display').innerText);

    const cityTier = document.getElementById('city-tier-select').value;
    const isNewConstruction = document.getElementById('construction-toggle').checked;
    const age = parseFloat(document.getElementById('age-display').innerText);
    const furnishing = document.getElementById('furnishing-select').value;
    const bathrooms = parseFloat(document.getElementById('bathrooms-display').innerText);
    const balconies = parseFloat(document.getElementById('balconies-display').innerText);
    
    const cityPreset = document.getElementById('preset-select').value;
    
    const hasPool = document.getElementById('pool-toggle').checked;
    const hasGym = document.getElementById('gym-toggle').checked;
    const hasSecurity = document.getElementById('security-toggle').checked;
    const hasBackup = document.getElementById('backup-toggle').checked;

    // Show loading state
    document.getElementById('price-output').innerHTML = `<span class="text-on-surface-variant font-normal text-4xl align-top mr-2">Computing...</span>`;

    try {
        // Since the FastAPI backend now serves the frontend, we can just use a relative URL!
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                area: area,
                bedrooms: bedrooms,
                floor: floor,
                parking: parking,
                facing: currentFacing,
                city_tier: cityTier,
                property_type: currentPropertyType,
                is_new_construction: isNewConstruction,
                age: age,
                furnishing: furnishing,
                bathrooms: bathrooms,
                balconies: balconies,
                city_preset: cityPreset,
                has_pool: hasPool,
                has_gym: hasGym,
                has_security: hasSecurity,
                has_backup: hasBackup
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        const lakhs = parseFloat(data.predicted_price_lakhs);
        let priceStr = "";
        if (lakhs >= 100) {
            priceStr = (lakhs / 100).toFixed(2) + " Crores";
        } else {
            priceStr = lakhs.toFixed(2) + " Lakhs";
        }
        
        // Update UI
        document.getElementById('price-output').innerHTML = `<span class="text-[#00d26a] font-normal text-5xl align-top mr-2">₹</span><span class="text-[#00d26a]">${priceStr}</span>`;
    } catch (error) {
        console.error("Failed to fetch price:", error);
        document.getElementById('price-output').innerHTML = `<span class="text-error font-normal text-3xl align-top mr-2">Error connecting to backend</span>`;
    }
}

// Run initial calculation
calculatePrice();

// --- MAP LOGIC ---
let map;
let darkLayer;
let satelliteLayer;

const CITY_COORDS = {
    "Custom Input": [20.5937, 78.9629], // Center of India
    "Mumbai": [19.0596, 72.8295],
    "Bengaluru": [12.9784, 77.6408],
    "Delhi NCR": [28.4595, 77.0266],
    "Hyderabad": [17.4435, 78.3772],
    "Pune": [18.5362, 73.8939],
    "Kolkata": [22.5804, 88.4649],
    "Chennai": [12.9675, 80.2589]
};

function initMap() {
    map = L.map('map', {zoomControl: false}).setView(CITY_COORDS["Custom Input"], 4);
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    });
    
    satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri'
    });

    darkLayer.addTo(map);
}

function setMapLayer(layerType) {
    const btnDark = document.getElementById('btn-dark-map');
    const btnSat = document.getElementById('btn-satellite-map');

    if (layerType === 'dark') {
        map.removeLayer(satelliteLayer);
        darkLayer.addTo(map);
        btnDark.className = "px-4 py-1.5 text-sm font-medium rounded-md bg-primary-container text-on-primary-container transition-all";
        btnSat.className = "px-4 py-1.5 text-sm font-medium rounded-md text-on-surface-variant hover:text-on-surface transition-all";
    } else {
        map.removeLayer(darkLayer);
        satelliteLayer.addTo(map);
        btnSat.className = "px-4 py-1.5 text-sm font-medium rounded-md bg-primary-container text-on-primary-container transition-all";
        btnDark.className = "px-4 py-1.5 text-sm font-medium rounded-md text-on-surface-variant hover:text-on-surface transition-all";
    }
}

document.addEventListener('DOMContentLoaded', initMap);

// --- SIDEBAR RESIZER LOGIC ---
const sidebar = document.getElementById('sidebar');
const resizer = document.getElementById('resizer');

let isResizing = false;

if (resizer && sidebar) {
    resizer.addEventListener('mousedown', (e) => {
        isResizing = true;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        let newWidth = e.clientX;
        if (newWidth < 300) newWidth = 300;
        if (newWidth > 600) newWidth = 600;
        sidebar.style.width = newWidth + 'px';
    });

    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            document.body.style.cursor = 'default';
            document.body.style.userSelect = 'auto';
            if (typeof map !== 'undefined' && map) {
                setTimeout(() => map.invalidateSize(), 100);
            }
        }
    });
}
