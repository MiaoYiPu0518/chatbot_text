import sys
import os
import openai 
import tkinter as tk
import threading

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.proxy = os.getenv('OPENAI_PROXY') 

GPT4 = "gpt-4"
TITLE = "AI CHAT"
FONT = "Berkeley Mono"
FONT_COLOR = "green"
BACKGROUND_COLOR = "black"

messages = [] # chat history 

def main():
    create_gui()

def create_gui():
    root = tk.Tk()
    root.title("AI Chat")

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)

    text_widget = tk.Text(main_frame, wrap=tk.WORD, font=(FONT, 10), fg=FONT_COLOR, bg=BACKGROUND_COLOR)
    text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X)

    submit_button = tk.Button(input_frame, text="SUBMIT", command=lambda: on_submit(user_input_widget, text_widget))
    submit_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    user_input_widget = tk.Text(input_frame, wrap=tk.WORD, height=4, font=(FONT, 10), fg=FONT_COLOR, bg=BACKGROUND_COLOR, insertbackground=FONT_COLOR)
    user_input_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
    root.update()
    root.mainloop()

def stream_response(completion, text_widget):
    full_response = ""
    text_widget.insert(tk.END, "\n>>> AI: ");
    text_widget.see(tk.END)
    for chunk in completion:
        # Skip the chunk if it doesn't have "content" attribute
        if not hasattr(chunk.choices[0].delta, "content"): continue

        content = chunk.choices[0].delta.content
        text_widget.insert(tk.END, content)
        text_widget.see(tk.END)
        full_response += content

    messages.append({"role": "assistant", "content": full_response})
    text_widget.insert(tk.END, "\n");
    text_widget.see(tk.END)

def on_submit(user_input_widget, text_widget):
    user_input = user_input_widget.get("1.0", tk.END).strip()
    user_input_widget.delete("1.0", tk.END)

    messages.append({"role": "user", "content": user_input})
    text_widget.insert(tk.END, f"\n>>> User: {user_input}\n")
    text_widget.see(tk.END)

    response_thread = threading.Thread(target=stream_response, args=(openai.ChatCompletion.create(model=GPT4, messages=messages, stream=True, temperature=0.7), text_widget))
    response_thread.start()
    

if __name__ == "__main__":
    main()