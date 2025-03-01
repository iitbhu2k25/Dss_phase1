document.addEventListener('DOMContentLoaded', () => {
    const methodsDropdown = document.getElementById('methods_dropdown');
    const demandTypeField = document.getElementById('demand_type');
    const stateDropdown = document.getElementById('state_dropdown');
    const districtDropdown = document.getElementById('district_dropdown');
    const subdistrictDropdown = document.getElementById('subdistrict_dropdown');
    const yearDropdown = document.getElementById('year_dropdown');
    const populationField = document.getElementById('population_field');
    const domesticfield = document.getElementById('domestic_field')
    // const floatingField = document.getElementById('floating_field');
    // const enuDropdown = document.getElementById('enu_dropdown');
    // const facilityDropdown = document.getElementById('facility_dropdown');
    const calculateButton = document.getElementById('calculate_button');
    const resultContainer = document.getElementById('result_container');
    const yearContainer = document.getElementById('year_container');
    // const institutionalContainer = document.getElementById('institutional_container');
    // const firefightingContainer = document.getElementById('firefighting_container');
    // const totalDemandField = document.getElementById('totaldemand');
    // const intermediateStageField = document.getElementById('intermediate_stage');
    // const intermediateStagePopulationField = document.getElementById('population_load_intermediate'); // For Intermediate Stage Population
    const populationContainer = document.getElementById('population_container');
    // const floatingContainer = document.getElementById('floating_container');
    // const enuContainer = document.getElementById('enu_container');
    // const facilityContainer = document.getElementById('facility_container');
    const villageContainer = document.getElementById('village-container');
    const selectedVillagesContainer = document.getElementById('selected-villages');
    const demandContainer = document.getElementById('domestic_container');
    const supplyContainer = document.getElementById('supply_container');

    
    demandTypeField.parentElement.classList.add('hidden');
    yearContainer.classList.add('hidden');
    populationContainer.classList.add('hidden');
    // floatingContainer.classList.add('hidden');
    // enuContainer.classList.add('hidden');
    // facilityContainer.classList.add('hidden');
    // institutionalContainer.classList.add('hidden');
    // firefightingContainer.classList.add('hidden');
    // document.getElementById('totaldemand').classList.add('hidden');
    methodsDropdown.addEventListener('change', () => {
        const selectedMethod = methodsDropdown.value;
        console.log('Selected Method:', selectedMethod); // Debugging output

        // Hide all sections initially
        // demandTypeField.parentElement.classList.add('hidden');
        yearContainer.classList.add('hidden');
        populationContainer.classList.add('hidden');
        demandContainer.classList.add('hidden')
        supplyContainer.classList.add('hidden')
        domesticfield.classList.add('hidden')
        // floatingContainer.classList.add('hidden');
        // enuContainer.classList.add('hidden');
        // facilityContainer.classList.add('hidden');
        // institutionalContainer.classList.add('hidden');
        // firefightingContainer.classList.add('hidden');
        // document.getElementById('totaldemand').classList.add('hidden');

        if (selectedMethod === 'sector_based') {
            console.log('Showing Sector-Based Section'); // Debugging output
            demandTypeField.parentElement.classList.remove('hidden');
            
        } else if (selectedMethod === 'water_supply') {
            console.log('Showing Village-Based Section'); // Debugging output
            demandTypeField.parentElement.classList.add('hidden');
            supplyContainer.classList.remove('hidden');
        }
    });
    

    const fetchLocations = (url, dropdown, placeholder) => {
        fetch(url)
            .then(response => response.json())
            .then(locations => {


                locations.sort((a, b) => a.name.localeCompare(b.name));


                dropdown.innerHTML = ''; // Clear existing options
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


    const fetchVillages = (url, container, selectedContainer) => {
        fetch(url)
            .then(response => response.json())
            .then(villages => {
                container.innerHTML = ''; // Clear the container
    
                if (villages.length === 0) {
                    container.innerHTML = '<p class="text-center">No villages available.</p>';
                    return;
                }
    
                // Separate villages with code === 0
                const specialVillage = villages.find(village => village.code === 0);
                const otherVillages = villages.filter(village => village.code !== 0);
    
                // Sort other villages by name in alphabetical order
                otherVillages.sort((a, b) => a.name.localeCompare(b.name));
    
                // Create a function to add a checkbox
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
    
                // Add the special village (code === 0) at the top, with the name "ALL"
                if (specialVillage) {
                    container.appendChild(addCheckbox(specialVillage, ' ALL'));
                }
    
                // Add the remaining villages
                otherVillages.forEach(village => {
                    container.appendChild(addCheckbox(village, village.name));
                });
            })
            .catch(error => console.error('Error fetching villages:', error));
    };
    
    const updateSelectedVillages = (selectedContainer) => {
        const selectedCheckboxes = document.querySelectorAll('#village-container input[type="checkbox"]:checked');
        const selectedVillages = Array.from(selectedCheckboxes).map(checkbox => ({
            code: checkbox.value,        // for sending to the backend
            name: checkbox.dataset.name    // for display purposes
        }));

        selectedContainer.innerHTML = selectedVillages.length
            ? selectedVillages.map(village => `<span class="badge bg-primary me-1">${village.name}</span>`).join('')
            : '<p class="text-muted">No villages selected.</p>';
    };
    


    fetchLocations('waterdemand/get_locations/', stateDropdown, 'Select State');

    stateDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        fetchLocations(`waterdemand/get_locations/?state_code=${stateCode}`, districtDropdown, 'Select District');
    });

    districtDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        const districtCode = districtDropdown.value;
        fetchLocations(`waterdemand/get_locations/?state_code=${stateCode}&district_code=${districtCode}`, subdistrictDropdown, 'Select Subdistrict');
    });

    subdistrictDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        const districtCode = districtDropdown.value;
        const subdistrictCode = subdistrictDropdown.value;

        if (subdistrictCode) {
            const url = `waterdemand/get_locations/?state_code=${stateCode}&district_code=${districtCode}&subdistrict_code=${subdistrictCode}`;
            fetchVillages(url, villageContainer, selectedVillagesContainer);
        }
    });


    


    demandTypeField.addEventListener('change', () => {
        const demandType = demandTypeField.value;
    
        // Reset all sections to hidden by default
        yearContainer.classList.add('hidden');
        populationContainer.classList.add('hidden');
        villageContainer.classList.add('hidden');
        selectedVillagesContainer.classList.add('hidden'); // Hide selected village text
        demandContainer.classList.add('hidden');
    
        // Show/hide fields based on the selected demand type
        if (demandType === 'modeled') {
            yearContainer.classList.remove('hidden');
            populationContainer.classList.remove('hidden');
            
            villageContainer.classList.remove('hidden');
            selectedVillagesContainer.classList.remove('hidden'); // Show selected village text
            subdistrictDropdown.parentElement.classList.remove('hidden'); // Show subdistrict container
        } else if (demandType === 'manual') {
            demandContainer.classList.remove('hidden')
            villageContainer.classList.remove('hidden');
            selectedVillagesContainer.classList.remove('hidden'); // Show selected village text
            subdistrictDropdown.parentElement.classList.remove('hidden'); // Show subdistrict container
            domesticfield.classList.remove('hidden')
        } else {
            // If no valid demand type is selected, hide everything
            resultContainer.textContent = '';
        }
    });
    
    

    yearDropdown.addEventListener('change', () => {
        const stateCode = stateDropdown.value;
        const districtCode = districtDropdown.value;
        const subdistrictCode = subdistrictDropdown.value;
        const selectedVillages = Array.from(
            document.querySelectorAll('#village-container input[type="checkbox"]:checked')
        ).map(checkbox => checkbox.value);
        const year = yearDropdown.value;
    
        console.log("Selected Villages:", selectedVillages);
    
        if (year && stateCode && districtCode && subdistrictCode && selectedVillages.length > 0) {
            // Prepare villages as a query parameter
            const villagesQuery = selectedVillages
                .map(v => `villages[]=${encodeURIComponent(v)}`)
                .join('&');

            
            // Build the URL
            const url = `waterdemand/get_combined_population/?state_code=${stateCode}&district_code=${districtCode}&subdistrict_code=${subdistrictCode}&year=${year}&${villagesQuery}`;
    
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.combined_population) {
                        populationField.value = Math.floor(data.combined_population).toString(); // Auto-populate the field
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('Error fetching combined population data:', error));
        } else {
            alert('Please select all required fields, including at least one village.');
        }
    });
    
    
    

    calculateButton.addEventListener('click', async (event) => {
        event.preventDefault();
        const selectedVillages = Array.from(
            document.querySelectorAll('#village-container input[type="checkbox"]:checked')
        ).map(checkbox => checkbox.value);
    
        if (selectedVillages.length === 0) {
            alert('Please select at least one village.');
            return;
        }
        if (demandTypeField.value === 'modeled') {
            const stateCode = stateDropdown.value;
            const districtCode = districtDropdown.value;
            const subdistrictCode = subdistrictDropdown.value;
            const year = yearDropdown.value;

            if (!year || !stateCode || !districtCode || !subdistrictCode) {
                alert('Please select State, District, and Subdistrict.');
                return;
            }

            try {
                const response = await fetch(`waterdemand/get_combined_population/?state_code=${stateCode}&district_code=${districtCode}&subdistrict_code=${subdistrictCode}&year=${year}&villages[]=${selectedVillages.join('&villages[]=')}`);
                const data = await response.json();
    
                if (data.combined_population) {
                    const population = data.combined_population;
                    const demand = population >= 1000000 ? population * 150/1000000 : population * 135/1000000;
                    const sewage = demand * 0.84;
                    resultContainer.textContent = `Total Generated Sewage Water is: ${sewage.toFixed(2)} MLD`;
                } else if (data.error) {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Error fetching population data:', error);
            }
        }  else if (demandTypeField.value === 'manual') {
                const waterdemand = parseFloat(document.getElementById('domestic_field').value) || 0;
                if (!waterdemand) {
                    alert('Please enter water demand.');
                    return;
                }
                const sewagedemand = waterdemand * 0.84;

                
                resultContainer.textContent = `Total Generated Sewage Water is: ${sewagedemand.toFixed(2)} MLD`;
        } else if (selectedMethod = 'water_supply') {
                const supplydemand = parseFloat(document.getElementById('supply_field').value) || 0;
                if (!supplydemand) {
                    alert('Please enter water supply.');
                    return;
                }
                const sewagedemand = supplydemand * 0.84;

                
                resultContainer.textContent = `Total Generated Sewage Water is: ${sewagedemand.toFixed(2)} MLD`;
        
        } else {
            alert('Please select a valid demand type.');
        }
    });
});