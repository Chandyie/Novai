import gradio as gr
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_fn(message, history):
    # Convert Gradio history tuples to OpenAI chat format
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for role, content in history:
        if role == "user":
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "assistant", "content": content})
    
    # Add current user message
    messages.append({"role": "user", "content": message})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message["content"]
    history.append(("user", message))
    history.append(("assistant", reply))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Say something", placeholder="Type here...")
    send_btn = gr.Button("Send")

    # Connect inputs
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])
    send_btn.click(chat_fn, [msg, chatbot], [chatbot, chatbot])

demo.launch(server_name="0.0.0.0", server_port=10000)

