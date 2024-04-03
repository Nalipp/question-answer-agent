from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def read_prompt_from_file(filename):
    """Reads a prompt from a file in the current directory."""
    with open(filename, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    return prompt


def generate_response(prompt, response_person, memory):
    """Generates a response to a given prompt using the OpenAI client with the chat model."""
    hayden_context1 = read_prompt_from_file('hayden.txt')
    hayden_context2 = read_prompt_from_file('hayden-additional.txt')
    nate_context1 = read_prompt_from_file('nate.txt')

    if response_person == 'nate':
        context = nate_context1

    if response_person == 'hayden':
        context = hayden_context1 + hayden_context2
    
    try:
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-0125-preview",
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                *memory,
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def playback_audio(file_path):
    os.system(f'afplay "{file_path}"')


def generate_audio(string, file_path, voiceType):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voiceType,
        input=string,
    )

    response.stream_to_file(f"{file_path}.mp3")
    playback_audio(f"{file_path}.mp3")


def simulate_conversation(initial_hayden_prompt, turns=2):
    """Simulates a conversation between two AI agents based on initial prompts."""
    memory = []
    hayden_prompt = initial_hayden_prompt

    for turn in range(turns):
        print(f"-----Question {turn+1} ---------------------------------------------------")
        nate_response = generate_response(hayden_prompt, 'nate', memory)
        file_path = f"./audio-files/hayden_prompt-{turns}"
        print("Hayden: ", hayden_prompt)
        generate_audio(hayden_prompt, file_path, 'alloy')
        file_path = f"./audio-files/nate_response-{turns}"
        print("Nate:", nate_response)
        generate_audio(nate_response, file_path, 'onyx')

        memory.append({ "role": "user", "content": f'nates prompt: {hayden_prompt}' })
        memory.append({ "role": "user", "content": f'haydens response: {nate_response}' })

        hayden_prompt = generate_response('generate a new question on the topic of george washington', 'hayden', memory)


def start_conversation():
    initial_hayden_prompt = "Hello, how are you? My name is Hayden. What is your name?"
    simulate_conversation(initial_hayden_prompt)
    print('****************************************************************************************************')
        


if __name__ == "__main__":
    start_conversation()
