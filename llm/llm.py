import os
import time

import google.generativeai as genai

import voicing.voice_generator as vg
import config as cfg

def configure_model():
    """Configure and create an instance of the generative AI model."""
    genai.configure(api_key=cfg.GEMINI_API_KEY)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    return model

def create_chat_session(model, char_background):
    """Create an initial chat session with the model."""
    initial_prompt = "[SYSTEM]\n"
    initial_prompt += char_background + "\n"
    initial_prompt += (
        "You will now be talking to V. Only respond with what you want to answer.\n"
        "Not with any comments about what you are doing.\n"
        "Not with any description about your facial expressions.\n"
        "You should ONLY respond with what actually comes out of your mouth.\n"
        "No emojis.\n"
        "Don't make your answers too long. Answer like in a natural conversation.\n"
        "You can trigger things like hugging and kissing by answering "
        "with <KISS> or <HUG> if you see it fitting.\n"
        "If you feel like you need more information on things that happened,"
        "answer with <RETRIEVE: \"\"> and the information you want to retrieve between the quotes.\n"
        "Understood?"
    )

    print("\nInitial prompt:\n")
    print(initial_prompt + "\n")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(initial_prompt)
    print("Initial response:\n")
    print(response.text)

    return chat_session


def process_message(chat_session, message):
    """Process a message using the chat session and generate a response."""
    # Voice V
    if cfg.VOICE_V:
        vg.voice_message(message, "V")
    time.sleep(1)
    # Write a response file
    # Potentially deleting the previous one
    with open(cfg.RESPONSE_FPATH, "w", encoding="utf-8") as f:
        message = "V: " + message
        print(f"Sending message: {message}")
        response = chat_session.send_message(message)
        print(f"Response: {response.text}")
        # Write to the response file
        # for communication with the game
        f.write(response.text)
    # Voice the NPC
    if cfg.VOICE_NPCS:
        vg.voice_message(response.text, "PanamPalmer")  # TODO hardcoded

