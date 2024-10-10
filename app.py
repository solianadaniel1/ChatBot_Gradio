from dotenv import load_dotenv
from PIL import Image
import pytesseract  # For OCR, if you want to extract text from images
import pandas as pd  # For handling CSV files
import os
import fitz  # For handling PDF files
import gradio as gr
from docx import Document  # For handling Word files
from swarmauri.standard.llms.concrete.GroqModel import GroqModel
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage
from swarmauri.standard.agents.concrete.SimpleConversationAgent import SimpleConversationAgent
from swarmauri.standard.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv("GROQ_API_KEY")
if API_KEY is None:
    raise ValueError("API key not found. Please check your .env file.")

# Initialize the GroqModel with the API key to access allowed models
llm = GroqModel(api_key=API_KEY)

# Get the available models from the llm instance
allowed_models = llm.allowed_models

# Initialize a MaxSystemContextConversation instance
conversation = MaxSystemContextConversation()

def analyze_image(image):
    # Convert the image to text using OCR
    text = pytesseract.image_to_string(image)
    return text

def analyze_pdf(file):
    text = ""
    # Open the PDF file
    pdf_document = fitz.open(file.name)
    # Extract text from each page
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text

def analyze_word(file):
    # Read the Word file and extract text
    doc = Document(file.name)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def analyze_file(file):
    # Check file type and process accordingly
    if file.name.endswith('.txt'):
        # Read text file
        with open(file.name, 'r') as f:
            return f.read()
    elif file.name.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(file.name)
        return df.head().to_string()  # Return the first few rows as a string
    elif file.name.endswith('.pdf'):
        # Analyze PDF file
        return analyze_pdf(file)
    elif file.name.endswith('.docx'):
        # Analyze Word file
        return analyze_word(file)
    # Add more file types as needed
    return "Unsupported file type."

def handle_feedback(user_feedback, history):
    # Save feedback to a file or a database with UTF-8 encoding
    with open("feedback.txt", "a", encoding='utf-8') as f:  # Specify encoding
        f.write(f"User Feedback: {user_feedback}\n")
        f.write("User Interaction History:\n")
        for entry in history:
            f.write(f"User: {entry[0]}\nAgent: {entry[1]}\n")
        f.write("\n" + "-"*40 + "\n\n")
    
    return "Thank you for your feedback!"

def converse(input_text, history=None, system_context="", model_name="", image=None, file=None, feedback=""):
    # Initialize history if it's None
    if history is None:
        history = []

    # Handle image input
    if image is not None:
        input_text += " " + analyze_image(image)

    # Handle file input
    if file is not None:
        input_text += " " + analyze_file(file)

    # Load the model and initialize the agent
    llm = GroqModel(api_key=API_KEY, name=model_name)
    agent = SimpleConversationAgent(llm=llm, conversation=conversation)
    agent.conversation.system_context = SystemMessage(content=system_context)

    # Strip and validate input
    input_text = str(input_text).strip()
    if not input_text:
        return "Please enter a message.", history, "", ""

    # Execute the command
    try:
        result = agent.exec(input_text)

        # Ensure result is a string
        if isinstance(result, str):
            result_str = result
        else:
            result_str = "An unexpected response format was received."

    except Exception as e:
        result_str = f"An error occurred: {str(e)}"

    # Clean up the result string
    result_str = result_str.replace("\n", " ").replace("\r", " ")

    # Append to history as a tuple
    history.append((input_text, result_str))

    # Handle user feedback
    feedback_response = ""
    if feedback:
        feedback_response = handle_feedback(feedback, history)

    # Format history for display
    formatted_history = "\n".join([f"Q: {entry[0]}\nA: {entry[1]}" for entry in history])

    # Return the result string, updated history, feedback response, and formatted history
    return result_str, history, feedback_response, formatted_history  # Add formatted history to outputs

# Set up the Gradio chat interface
demo = gr.Interface(
    fn=converse,
    inputs=[
        gr.Textbox(label="User Input"),            # Input from the user
        gr.State(),                                 # Maintain state for history
        gr.Textbox(label="System Context"),        # System context from the user
        gr.Dropdown(label="Model Name", choices=allowed_models, value=allowed_models[0]),
        gr.Image(type="pil", label="Upload Image"),  # Input for images
        gr.File(label="Upload File"),                # Input for files
        gr.Textbox(label="Feedback", placeholder="Provide your feedback here...")  # User feedback
    ],
    outputs=[
        gr.Textbox(label="Response"),              # Output response from the model
        gr.State(),                                 # Updated conversation history
        gr.Textbox(label="Feedback Response"),      # Acknowledge feedback submission
        gr.Textbox(label="Conversation History", placeholder="History of questions asked...", interactive=False)  # History output
    ],
    title="A System Context Conversation",
    description="Interact with the agent using a selected model and system context"
)

# Launch the demo
if __name__ == "__main__":
    demo.launch(share=True)