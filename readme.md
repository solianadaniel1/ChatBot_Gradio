# Gradio Chatbot with Groq API Integration

This project integrates the Groq API with a Gradio-based chatbot interface, allowing users to interact with a conversational agent powered by different Groq models. Users can upload images, PDFs, and Word files for analysis and receive responses in a conversational format.

## Features

- **Multi-file Support**: Upload images, PDFs, and Word documents for text extraction and analysis.
- **Conversational Interface**: Interact with the chatbot using natural language.
- **Feedback Mechanism**: Provide feedback on the responses to improve the chatbot's performance.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.7 or higher
- pip

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv myenv
    myenv\Scripts\activate  # On Windows
    # source myenv/bin/activate  # On macOS/Linux
    ```

3. **Install required packages**:
    ```bash
    pip install pytesseract
    pip install PyMuPDF  # For PDF handling
    pip install python-docx  # For Word file handling
    pip install gradio==3.39.0
    pip uninstall typer -y
    pip install "typer<0.10.0,>=0.3.0"
    pip install swarmauri[full]==0.4.1 python-dotenv
    pip install groq
    pip install openai==0.28
    pip install --upgrade openai
    ```

4. **Install Tesseract OCR**:
   - Follow the steps below to install Tesseract OCR on your system:

    **For Windows**:
    - Run PowerShell as an administrator and execute the following command:
      ```powershell
      Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
      ```
    - After installing Chocolatey, run:
      ```powershell
      choco install tesseract
      ```
    - Verify the installation by running:
      ```powershell
      tesseract --version
      ```

## Usage

1. **Create a `.env` file** in the project directory and add your Groq API key:
    ```plaintext
    GROQ_API_KEY=your_groq_api_key
    ```

2. **Run the application**:
    ```bash
    python app.py
    ```

3. **Access the chatbot** in your web browser at `http://127.0.0.1:7860`.


## Acknowledgements

- [Gradio](https://gradio.app/)
- [Groq](https://groq.ai/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
