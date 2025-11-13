import gradio as gr
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for role, content in history:
        messages.append({"role": role, "content": content})
    
    messages.append({"role": "user", "content": message})

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
    txt = gr.Textbox(label="Type your message here...", placeholder="Say hi!", lines=2)
    state = gr.State([])

    txt.submit(chat_with_ai, [txt, state], [chatbot, state])

demo.launch(server_name="0.0.0.0", server_port=10000)
