import os
from openai import OpenAI
import gradio as gr

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_fn(message, history):
    if history is None:
        history = []

    messages = [{"role": "system", "content": "You are a helpful assistant."}] + history + [{"role": "user", "content": message}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content  # <-- FIXED
    except Exception as e:
        reply = f"Error: {str(e)}"

    # Store history as dictionaries
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    txt = gr.Textbox(label="Type your message here...")
    send_btn = gr.Button("Send")

    txt.submit(chat_fn, [txt, chatbot], [chatbot, chatbot])
    send_btn.click(chat_fn, [txt, chatbot], [chatbot, chatbot])

demo.launch(server_name="0.0.0.0", server_port=10000)


