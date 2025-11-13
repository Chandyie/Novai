# app.py
import gradio as gr
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat function
def chat_fn(message, history):
    # Append user message to history
    history.append({"role": "user", "content": message})

    # Send conversation to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # replace with your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *history
        ]
    )

    reply = response.choices[0].message["content"]
    # Append AI response to history
    history.append({"role": "assistant", "content": reply})
    # Return formatted tuples for Gradio
    formatted_history = [(h["role"], h["content"]) for h in history if h["role"] in ["user", "assistant"]]
    return formatted_history, history

# Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Charlie", type="messages")
    msg = gr.Textbox(label="Type your message", placeholder="Say something...")
    send_btn = gr.Button("Send")

    # Define click and enter behavior
    send_btn.click(chat_fn, [msg, chatbot], [chatbot, chatbot])
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])

# Launch
demo.launch(server_name="0.0.0.0", server_port=10000)


    txt.submit(chat_with_ai, [txt, state], [chatbot, state])

demo.launch(server_name="0.0.0.0", server_port=10000)
