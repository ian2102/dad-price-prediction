# Dark and Darker Price Prediction

## Project Overview
Dark and Darker Price Prediction is a project designed to predict prices for in-game items in the game **Dark and Darker**. The main features include:
1. **Capturing Process**: Captures, parses, saves item network data.
2. **Machine Learning**: Trains models for price prediction and image recognition.
3. **Web GUI**: Allows users to interact with the models.

### Technologies
- **Backend**: Python, Flask, PyShark, Protobuf
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Pandas, NumPy, Joblib, Scikit-learn

# Demo
https://github.com/user-attachments/assets/efce87ae-7c55-4817-be4c-c6062f2b8e84

## How to Use

### Prerequisites
Before using the project, you need to install the following:

1. **Python**: Make sure Python is installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).

2. **Protocol Buffers**:  
   You need to download and install the **Protocol Buffers** library from [Protocol Buffers GitHub repository](https://github.com/protocolbuffers/protobuf). This library includes `protoc`, the Protocol Buffers compiler, which is essential for compiling the `.proto` files into Python code. Follow these steps:
   - Clone the repository and follow the installation instructions provided to install `protoc`.
   
3. **Extract Proto Files**:  
   To get the `.proto` files required for data parsing, use the **Protodump** tool. Download it from [Protodump GitHub repository](https://github.com/arkadiyt/protodump). This tool allows you to extract `.proto` files from the **Dark and Darker** binary. Follow these steps:
   - Clone the Protodump repository.
   - Follow the installation instructions provided to get the tool up and running.
   - Run the tool on the **Dark and Darker** binary to extract the `.proto` files.

4. **Compile Proto Files**:  
   Once you have the `.proto` files from Protodump, you need to compile them using the `protoc` compiler. You can do this with the following command:
   ```bash
   protoc --python_out=. *.proto
   ```
   - This command will compile all the `.proto` files in the current directory and output the generated Python files in the same directory.
   - After compilation, make sure to add the path to your files to your system's PATH environment variable so that it can be accessed.  
  
5. **Tesseract Installation**: Install Tesseract OCR, which is required for image recognition. You can download it from [Tesseract OCR's GitHub](https://github.com/tesseract-ocr/tesseract). Follow the installation instructions for your operating system.
   - After installation, make sure to set the path to the Tesseract executable in the project by editing the `image.py` file:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR	esseract.exe'
     ```

6. **Install Python Dependencies**: Navigate to the project directory and install the required Python dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

### Capturing Data
Once the configuration is set up:
- Run the `capture.py` file to begin capturing data. The script will automatically start capturing network data from the game and save it to the specified data directory. Press the exit keybind (default: `F7`) to stop the capture process.

### Training the Models
After capturing data:
- Use the example file `train_price.py` to start training with default settings.

### Running the Web Application
To run the Flask web application:
1. Ensure that you have followed the configuration steps and trained the models.
2. Run the app with the following command:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to [http://localhost:5000](http://localhost:5000) to access the web interface.
4. Use the interface to interact with the models, including uploading images for recognition and checking price predictions.

## Configuration
The project requires several configuration settings to properly handle the capturing process, image recognition, and machine learning model training. Below are the key configuration settings you may need to adjust.

### Capture Configuration
The capturing process involves capturing network data, images, and saving it to the appropriate directories. The key parameters for the capture process are defined in the `__init__` method.

- **IMPORTANT** Protocol Buffers: Ensure that the Protocol Buffer files are accessible via the correct path for proper data capture and parsing.
- **IMPORTANT** Network Interface: Set the network interface for capturing data. Default is `'Ethernet'`.

### Image Recognition Configuration
For image recognition, you will need to specify the path to the Tesseract executable and adjust image comparison settings.

- **IMPORTANT** Tesseract Path: Set the path to the Tesseract OCR executable. Default is set to `'C:\Program Files\Tesseract-OCR\tesseract.exe'`.

### Macro Functions
The macro functions in `macros.py` are based on a **1920x1080 resolution** of the game **Dark and Darker**. You can adjust these coordinates using the `point.py` script.

- **IMPORTANT** Screen Resolution: The macros assume a 1920x1080 resolution, and will need adjustments if your screen resolution is different.

### Model Configuration
The machine learning models used for price prediction and image recognition require customization for optimal performance. You can adjust the following:
- Model Type: Choose the model that best suits your needs (e.g., RandomForest, XGBoost, LightGBM, etc.).
- Hyperparameters: Fine-tune the model's hyperparameters (e.g., learning rate, number of estimators, etc.) for better accuracy.

## Known Issues
- **Dropbox Bug**: The image dropbox on the web page is currently not functional.
- **Image Upload Limitation**: You cannot paste images into the upload field; you must manually select a file.
- **Poor Model Performance**: The current models perform poorly, and feature corruption is present.
- **Capture Process Errors**: Occasionally, the capture process encounters packets with incorrect length headers, causing errors. The cause of this issue is unknown.

## Acknowledgments
- Special thanks to **Kokkor** on Discord for their help with this project.
- Special thanks to [DarkerDB](https://darkerdb.com/) and **Anders** on Discord for their help with this project and for allowing me to use a custom Pytesseract model.

## Additional Section
For more details on this project and my motives, visit my website: [https://iansolutions.xyz](https://iansolutions.xyz).

## License
This project is open-source, and you are free to modify, distribute, and use it as you wish.



