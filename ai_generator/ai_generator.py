import google.generativeai as genai
import re

GEMINI_AI_SECRET_KEY = ''

genai.configure(api_key=GEMINI_AI_SECRET_KEY)

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

with open("app/ai_generator/data/prompt.txt", "r", encoding='utf-8') as file:
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

def get_post_data(user_keys):
  keys = _create_keys(user_keys + NOT_EDITABLE_KEYS)
  prompt = DEFAULT_PROMPT + keys
  
  conversation.send_message(prompt)

  return conversation.last.text

class Post():
  def __init__(self, struct, content, resource_keys, hashtags):
    self.struct = struct
    self.content = content
    self.resource_keys = resource_keys
    self.hashtags = hashtags
    
  def to_dict(self):
    self.hashtags.pop(0)
    
    return {
        'struct': self.struct,
        'content': self.content,
        'resource_keys': self.resource_keys,
        'hashtags': self.hashtags
    }

def parse_result_to_post(text):
  struct_re = re.compile(r"\*\*struct\:?\*\*\:?(.+)")
  content_re = re.compile(r"\*\*content\:?\*\*\:?(.+)")
  image_re = re.compile(r"\*\*resource_keys\:?\*\*\:?(.+)")
  hashtags_re = re.compile(r"\*\*hashtags\:?\*\*\:?(.+)")

  struct_match = struct_re.search(text)
  content_match = content_re.search(text)
  image_match = image_re.search(text)
  hashtags_match = hashtags_re.search(text)

  struct = struct_match.group(1).strip()
  content = content_match.group(1).strip()
  resource_keys = image_match.group(1).strip()
  hashtags = [hashtag.strip() for hashtag in hashtags_match.group(1).split('#') if hashtag]

  post = Post(struct, content, resource_keys, hashtags)

  return post