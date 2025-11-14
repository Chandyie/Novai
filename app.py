import os
import gradio as gr
from openai import OpenAI

# Make sure you set your OPENAI_API_KEY in Render environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_fn(message, history):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *history,
            {"role": "user", "content": message}
        ]
    )
    
    reply = response.choices[0].message["content"]
    # append new messages to history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Say something")
    send_btn = gr.Button("Send")

    # submit or click both trigger chat
    msg.submit(chat_fn, [msg, chatbot], [chatbot, chatbot])
    send_btn.click(chat_fn, [msg, chatbot], [chatbot, chatbot])

demo.launch(server_name="0.0.0.0", server_port=10000)


    txt.submit(chat_with_ai, [txt, state], [chatbot, state])

demo.launch(server_name="0.0.0.0", server_port=10000)
