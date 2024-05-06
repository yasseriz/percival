from openai import OpenAI
import logging
from app.utils.env_loader import get_config_value
client = OpenAI(
    api_key= get_config_value('OPEN_API_KEY')
)

class CommandInterpreter:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        client.api_key = self.api_key

    def interpret_command(self, input_text):
        logging.info(f"Interpreting command: {input_text}")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system", "content":"You are an API developer. You have been given the following prompt to translate into an API action."},
                    {"role":"user", "content":f"Translate the following prompt into an API action: '{input_text}'"}],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5
            )
            command_action = response.choices[0].text.strip()
            return command_action
        except Exception as e:
            print(f"Error in intepreting command: {e}")
            return None
