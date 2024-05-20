import google.generativeai as genai

genai.configure(api_key="AIzaSyDF7EvI8Oo2BCDtnFNw8IdHg1mXWym60d0")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

conversation = model.start_chat(history=[])

#Read files
DEFAULT_PROMPT = None

with open("app/posts_ai/data/prompt.txt", "r", encoding='utf-8') as file:
  DEFAULT_PROMPT = file.read()

def _create_keys(user_keys):
  result = "\n"
  for index, key in enumerate(user_keys, start=1):
      result += f"{index}. {key}\n"
  return result

NOT_EDITABLE_KEYS = [
   "Liderazgo",
    "Inteligencia emocional",
    "Manejo de equipos de trabajo",
    "Solución de problemas",
    "Desarrollo de trabajo remoto"
]

def get_result(user_keys):
  keys = _create_keys(user_keys + NOT_EDITABLE_KEYS)
  prompt = DEFAULT_PROMPT + keys
  
  conversation.send_message(prompt)
  print(conversation.last.text)

  return conversation.last.text

get_result(user_keys=[
            "gerente de proyectos fotovoltaicos",
            "generación de energía, transmisión de energía eléctrica",
            "Proyectos EPC, Construcción de proyectos solares, construcción de líneas de transmisión, grandes proyectos de generación",
            "Diseño de líneas de transmisión, selección de conductor, plscadd, pvsyst",
            "comunicación asertiva, templanza, escucha activa"])