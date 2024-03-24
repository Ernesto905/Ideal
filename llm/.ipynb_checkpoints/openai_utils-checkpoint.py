from openai import OpenAI 
import dotenv
print("hello")

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

def test_backend(session):
    # Access session values
    current_weight = session.get("current_weight")
    ideal_weight = session.get("ideal_weight")
    body_composition = session.get("body_composition")
    archetype = session.get("archetype")
    age = session.get("age")
    sex = session.get("sex")
    allergies = session.get("allergies")
    diet = session.get("diet")
    religion = session.get("religion")
    anything_else_diet = session.get("anything_else_diet")
    physical_impediments = session.get("physical_impediments")

    session_values = f"Values are current weight: {current_weight}<br>" \
                     f"ideal weight: {ideal_weight}<br>" \
                     f"body composition: {body_composition}<br>" \
                     f"archetype: {archetype}<br>" \
                     f"age: {age}<br>" \
                     f"sex: {sex}<br>" \
                     f"allergies: {allergies}<br>" \
                     f"diet: {diet}<br>" \
                     f"religion: {religion}<br>" \
                     f"anything else diet: {anything_else_diet}<br>" \
                     f"physical impediments: {physical_impediments}"

    return session_values
