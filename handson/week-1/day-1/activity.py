# 1. Install required packages
#pip install -q google-genai gradio

# 2. Import libraries
import os
import gradio as gr
from google import genai

# 3. Configure the Gemini API Client
# Replace 'YOUR_API_KEY' with your actual Gemini API key from Google AI Studio
os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
client = genai.Client()

# 4. Define the core AI function
def analyze_inputs(image, text_prompt):
    if image is None and not text_prompt:
        return "Please provide an image or type a prompt!"
    
    # Bundle inputs for the multimodal model
    contents = []
    if image is not None:
        contents.append(image)
    if text_prompt:
        contents.append(text_prompt)
    else:
        # Default prompt if they only upload an image
        contents.append("Describe this image in detail and identify key objects.")
        
    try:
        # Call Gemini 2.5 Flash for instant multimodal analysis
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

# 5. Build the Interactive Web UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Live GenAI Multimodal Classroom Demo")
    gr.Markdown("Upload an image, type a question, and watch the LLM reason in real-time.")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="pil", label="📸 Upload Image or Take Photo")
            input_text = gr.Textbox(label="✍️ Ask something about the image (Optional)", placeholder="e.g., 'Write a poem about this' or 'What is wrong with this plant?'")
            submit_btn = gr.Button("🚀 Run AI Analysis", variant="primary")
        
        with gr.Column():
            output_text = gr.Markdown(label="🧠 AI Response")
            
    submit_btn.click(fn=analyze_inputs, inputs=[input_img, input_text], outputs=output_text)

# 6. Launch the app and generate a PUBLIC shareable link
demo.launch(share=True)
