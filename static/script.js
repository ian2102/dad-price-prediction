document.addEventListener('DOMContentLoaded', function() {
    const nameSelection = document.getElementById('name-selection');
    const raritySelection = document.getElementById('rarity-selection');
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const priceContainer = document.getElementById('price-container');
    const ppContainer = document.getElementById('pp-container');
    const spContainer = document.getElementById('sp-container');

    nameSelection.addEventListener('change', function() {
        updateBaseStats();
    });

    raritySelection.addEventListener('change', function() {
        updateEnchantments();
    });

    function updateBaseStats() {
        const name = nameSelection.value;
        let items = dataDict["items_to_pp"][name] || [];
        ppContainer.innerHTML = '';
        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            let itemElement = document.createElement('div');
            itemElement.innerHTML = `
                <label for="${item}">${item}:</label>
                <input type="number" id="${item}" name="${item}" step="0.01" placeholder="Enter value" />
            `;
            ppContainer.appendChild(itemElement);
        }
    }
    
    function updateEnchantments() {
        const rarityString = raritySelection.value;
        let rarity = dataDict["rarity_to_property_count"][rarityString] || [];
        spContainer.innerHTML = '';
    
        for (let i = 0; i < rarity; i++) {
            let rarityElement = document.createElement('div');
            let spOptions = dataDict["sp"].map(a => `<option value="${a}">${a}</option>`).join('');
            rarityElement.innerHTML = `
                <select id="enchantment-selection-${i}" name="enchantment-selection-${i}">
                    ${spOptions}
                </select>
                <input type="number" id="enchantment-input-${i}" name="enchantment-input-${i}" step="0.01" placeholder="Enter value" />
            `;
    
            spContainer.appendChild(rarityElement);
        }
    }
    

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
    
        fetch('/submit', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            priceContainer.innerHTML = `<pre>${data}</pre>`;
        })
        .catch(error => {
            console.error('Error:', error);
            priceContainer.innerHTML = 'An error occurred while processing your request.';
        });
    });
    
    document.getElementById('image-upload-box').addEventListener('click', function() {
        document.getElementById('image-upload').click();
    });
    
    const imageUploadBox = document.getElementById('image-upload-box');
    const imageInput = document.getElementById('image-upload');
    
    imageUploadBox.addEventListener('dragover', function(event) {
        event.preventDefault();
        imageUploadBox.classList.add('dragover');
    });
    
    imageUploadBox.addEventListener('dragleave', function() {
        imageUploadBox.classList.remove('dragover');
    });
    
    imageUploadBox.addEventListener('drop', function(event) {
        event.preventDefault();
        imageUploadBox.classList.remove('dragover');
        
        const file = event.dataTransfer.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });
    
    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });
    
    function handleFileUpload(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewImage = document.getElementById('image-preview');
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
     
    
    document.getElementById('upload-btn').addEventListener('click', function() {
        const formData = new FormData(form);
    
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            handleUploadResponse(data);
        })
        .catch(error => {
            console.error('Error:', error);
            resultContainer.innerHTML = 'Error uploading the image.';
        });
    });

    function handleUploadResponse(data) {
        resultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;

        nameSelection.value = data["name"];
        nameSelection.dispatchEvent(new Event('change'));

        raritySelection.value = data["rarity"];
        raritySelection.dispatchEvent(new Event('change'));

        for (let p in data) {
            if (p.startsWith("p")) {
                document.getElementById(p).value = data[p]
            } 
        }

        const divs = spContainer.querySelectorAll('div');
        let count = 0;
        for (let p in data) {
            if (p.startsWith("s")) {
                let div = divs[count];
                count++;
                const select = div.querySelector('select');
                if (select) {
                    select.value = p;
                    select.dispatchEvent(new Event('change'));
                }
                const input = div.querySelector('input');
                if (input) {
                    input.value = data[p];
                    input.dispatchEvent(new Event('change'));
                }
            }
        }
    }
});
