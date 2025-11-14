import os
from openai import OpenAI
import gradio as gr

# Make sure your OpenAI API key is set as an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_fn(message, history):
    if history is None:
        history = []
    
    # Convert Gradio history into OpenAI chat format
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for role, content in history:
        messages.append({"role": role, "content": content})
    
    # Add the current user message
    messages.append({"role": "user", "content": message})
    
    # Call OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    # Update history
    history.append(("user", message))
    history.append(("assistant", reply))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    txt = gr.Textbox(label="Type your message here...")
    send_btn = gr.Button("Send")

    # Connect submit button and textbox
    txt.submit(chat_fn, [txt, chatbot], [chatbot, chatbot])
    send_btn.click(chat_fn, [txt, chatbot], [chatbot, chatbot])

demo.launch(server_name="0.0.0.0", server_port=10000)


