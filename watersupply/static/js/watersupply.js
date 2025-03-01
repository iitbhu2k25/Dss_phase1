document.addEventListener('DOMContentLoaded', () => {
    // Location and result elements
    const stateDropdown = document.getElementById('state_dropdown');
    const districtDropdown = document.getElementById('district_dropdown');
    const subdistrictDropdown = document.getElementById('subdistrict_dropdown');
    const calculateButton = document.getElementById('calculate_button');
    const resultContainer = document.getElementById('result_container');
    const villageContainer = document.getElementById('village-container');
    const selectedVillagesContainer = document.getElementById('selected-villages');

    // Groundwater supply input elements
    const directGroundwaterInput = document.getElementById("direct_groundwater");
    const numTubewells = document.getElementById("num_tubewells");
    const dischargeRate = document.getElementById("discharge_rate");
    const operatingHours = document.getElementById("operating_hours");

    // Alternate water supply input elements
    const directAlternateInput = document.getElementById("direct_alternate");
    const rooftopTankInput = document.getElementById("rooftop_tank");
    const aquiferRechargeInput = document.getElementById("aquifer_recharge");
    const surfaceRunoffInput = document.getElementById("surface_runoff");
    const reuseWaterInput = document.getElementById("reuse_water");



    // ========================
    // Groundwater Disable Logic
    // ========================
    function updateGroundwaterDisableState() {
        // If direct groundwater field is not empty, disable tube-well fields
        if (directGroundwaterInput.value.trim() !== "") {
            numTubewells.disabled = true;
            dischargeRate.disabled = true;
            operatingHours.disabled = true;
            // Allow clearing the direct field so user can change it
        } 
        // Else if any tube-well field is not empty, disable direct groundwater field
        else if (numTubewells.value.trim() !== "" ||
                 dischargeRate.value.trim() !== "" ||
                 operatingHours.value.trim() !== "") {
            directGroundwaterInput.disabled = true;
            // Keep tube-well fields enabled
            numTubewells.disabled = false;
            dischargeRate.disabled = false;
            operatingHours.disabled = false;
        } 
        // If both sides are empty, enable all groundwater fields
        else {
            directGroundwaterInput.disabled = false;
            numTubewells.disabled = false;
            dischargeRate.disabled = false;
            operatingHours.disabled = false;
        }
    }

    // Add event listeners for groundwater inputs
    directGroundwaterInput.addEventListener("input", updateGroundwaterDisableState);
    numTubewells.addEventListener("input", updateGroundwaterDisableState);
    dischargeRate.addEventListener("input", updateGroundwaterDisableState);
    operatingHours.addEventListener("input", updateGroundwaterDisableState);

    // ============================
    // Alternate Water Disable Logic
    // ============================
    function updateAlternateDisableState() {
        // If the direct alternate field has a value, disable calculation fields
        if (directAlternateInput.value.trim() !== "") {
            rooftopTankInput.disabled = true;
            aquiferRechargeInput.disabled = true;
            surfaceRunoffInput.disabled = true;
            reuseWaterInput.disabled = true;
        } 
        // Else if any calculation field is not empty, disable the direct alternate field
        else if (rooftopTankInput.value.trim() !== "" ||
                 aquiferRechargeInput.value.trim() !== "" ||
                 surfaceRunoffInput.value.trim() !== "" ||
                 reuseWaterInput.value.trim() !== "") {
            directAlternateInput.disabled = true;
            // Keep calculation fields enabled
            rooftopTankInput.disabled = false;
            aquiferRechargeInput.disabled = false;
            surfaceRunoffInput.disabled = false;
            reuseWaterInput.disabled = false;
        } 
        // If both sides are empty, enable all alternate fields
        else {
            directAlternateInput.disabled = false;
            rooftopTankInput.disabled = false;
            aquiferRechargeInput.disabled = false;
            surfaceRunoffInput.disabled = false;
            reuseWaterInput.disabled = false;
        }
    }

    // Add event listeners for alternate water supply inputs
    directAlternateInput.addEventListener("input", updateAlternateDisableState);
    rooftopTankInput.addEventListener("input", updateAlternateDisableState);
    aquiferRechargeInput.addEventListener("input", updateAlternateDisableState);
    surfaceRunoffInput.addEventListener("input", updateAlternateDisableState);
    reuseWaterInput.addEventListener("input", updateAlternateDisableState);

    // ===========================================
    // Location, Villages, and Selected Villages Code
    // ===========================================
    const fetchLocations = (url, dropdown, placeholder) => {
        fetch(url)
            .then(response => response.json())
            .then(locations => {
                locations.sort((a, b) => a.name.localeCompare(b.name));
                dropdown.innerHTML = '';
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = placeholder;
                dropdown.appendChild(defaultOption);
                locations.forEach(location => {
                    const option = document.createElement('option');
                    option.value = location.code;
                    option.textContent = location.name;
                    dropdown.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching locations:', error));
    };

    // fetch Regions
    const fetchVillages = (url, container, selectedContainer) => {
        fetch(url)
            .then(response => response.json())
            .then(villages => {
                container.innerHTML = '';
                if (villages.length === 0) {
                    container.innerHTML = '<p class="text-center">No villages available.</p>';
                    return;
                }
                const specialVillage = villages.find(village => village.code === 0);
                const otherVillages = villages.filter(village => village.code !== 0);
                otherVillages.sort((a, b) => a.name.localeCompare(b.name));

                const addCheckbox = (village, displayName) => {
                    const checkboxWrapper = document.createElement('div');
                    checkboxWrapper.classList.add('form-check');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.classList.add('form-check-input');
                    checkbox.id = `village_${village.code}`;
                    checkbox.value = village.code;
                    checkbox.dataset.name = village.name;
                    const label = document.createElement('label');
                    label.classList.add('form-check-label');
                    label.htmlFor = `village_${village.code}`;
                    label.textContent = displayName;
                    checkbox.addEventListener('change', () => {
                        updateSelectedVillages(selectedContainer);
                    });
                    checkboxWrapper.appendChild(checkbox);
                    checkboxWrapper.appendChild(label);
                    return checkboxWrapper;
                };

                if (specialVillage) {
                    container.appendChild(addCheckbox(specialVillage, ' ALL'));
                }
                otherVillages.forEach(village => {
                    container.appendChild(addCheckbox(village, village.name));
                });
            })
            .catch(error => console.error('Error fetching villages:', error));
    };

    // Selected Villages
    const updateSelectedVillages = (selectedContainer) => {
        const selectedCheckboxes = document.querySelectorAll('#village-container input[type="checkbox"]:checked');
        const selectedVillages = Array.from(selectedCheckboxes).map(checkbox => ({
            code: checkbox.value,
            name: checkbox.dataset.name
        }));
        selectedContainer.innerHTML = selectedVillages.length
            ? selectedVillages.map(village => `<span class="badge bg-primary me-1">${village.name}</span>`).join('')
            : '<p class="text-muted">No villages selected.</p>';
    };

    // Populate dropdowns on load and on change events
    fetchLocations('waterdemand/get_locations/', stateDropdown, 'Select State');

    // State dropdown
    stateDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        fetchLocations(`waterdemand/get_locations/?state_code=${stateCode}`, districtDropdown, 'Select District');
    });

    // District dropdown
    districtDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        const districtCode = districtDropdown.value;
        fetchLocations(`waterdemand/get_locations/?state_code=${stateCode}&district_code=${districtCode}`, subdistrictDropdown, 'Select Subdistrict');
    });

    // Subdistrict dropdown
    subdistrictDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        const districtCode = districtDropdown.value;
        const subdistrictCode = subdistrictDropdown.value;
        if (subdistrictCode) {
            const url = `waterdemand/get_locations/?state_code=${stateCode}&district_code=${districtCode}&subdistrict_code=${subdistrictCode}`;
            fetchVillages(url, villageContainer, selectedVillagesContainer);
        }
    });

    // ======================================
    // Calculate Water Supply on Button Click
    // ======================================
    calculateButton.addEventListener('click', () => {
        resultContainer.innerHTML = '';

        // Groundwater inputs
        const surfaceWater = parseFloat(document.getElementById('surface_water').value) || 0;
        const directGroundwaterValue = parseFloat(directGroundwaterInput.value) || 0;
        const numTubewellsValue = parseFloat(numTubewells.value) || 0;
        const dischargeRateValue = parseFloat(dischargeRate.value) || 0;
        const operatingHoursValue = parseFloat(operatingHours.value) || 0;
        const groundwaterCalc = numTubewellsValue * dischargeRateValue * operatingHoursValue;
        if (directGroundwaterValue > 0 &&
            (numTubewellsValue > 0 || dischargeRateValue > 0 || operatingHoursValue > 0)) {
            resultContainer.innerHTML = '<h4 class="text-danger">Error: Provide either direct groundwater supply or calculated groundwater supply, not both.</h4>';
            return;
        }
        const groundwaterSupply = directGroundwaterValue > 0 ? directGroundwaterValue : groundwaterCalc;

        // Alternate water supply inputs
        const directAlternateValue = parseFloat(directAlternateInput.value) || 0;
        const rooftopTankValue = parseFloat(rooftopTankInput.value) || 0;
        const aquiferRechargeValue = parseFloat(aquiferRechargeInput.value) || 0;
        const surfaceRunoffValue = parseFloat(surfaceRunoffInput.value) || 0;
        const reuseWaterValue = parseFloat(reuseWaterInput.value) || 0;
        const alternateCalc = rooftopTankValue + aquiferRechargeValue + surfaceRunoffValue + reuseWaterValue;
        if (directAlternateValue > 0 &&
            (rooftopTankValue > 0 || aquiferRechargeValue > 0 || surfaceRunoffValue > 0 || reuseWaterValue > 0)) {
            resultContainer.innerHTML = '<h4 class="text-danger">Error: Provide either direct alternate water supply or calculated alternate water supply, not both.</h4>';
            return;
        }
        const alternateWaterSupply = directAlternateValue > 0 ? directAlternateValue : alternateCalc;

        const totalWaterSupply = surfaceWater + groundwaterSupply + alternateWaterSupply;
        resultContainer.innerHTML = `<h4>Total Water Supply for Selected Region is: ${totalWaterSupply.toFixed(2)} MLD</h4>`;
    });
});
