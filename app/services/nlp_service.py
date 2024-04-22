import openai

class CommandInterpreter:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        openai.api_key = self.api_key

    def interpret_command(self, input_text):
        try:
            response = openai.completions.create(
                engine='gpt-4-turbo',
                prompt=f"Translate the following prompt into an API action: '{input_text}'",
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
