from openai import OpenAI 
import os 
import dotenv

dotenv.load_dotenv()

client = OpenAI()

def get_completion(form_input):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant. You are concise and to the point."},
        {"role": "user", "content": form_input}
      ]
    )

    return completion.choices[0].message

