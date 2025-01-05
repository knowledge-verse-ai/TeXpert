from core.llm_interface import create_and_send_prompt, Prompt

class LatexGenerationPromptRunner:
    def __init__(self, prompt_id: str, model: str, user_prompt: str):
        self.prompt_id:str = prompt_id
        self.model:str = model
        self.system_prompt:str = r'''You are a helpful latex code assistant. 
Your main job is to produce syntactically correct and logically accurate LaTeX code based on instructions given as TASK INSTRUCTIONS. 
Make sure to follow each and every small instruction given in the task instructions. 
The LaTeX code need not always be for an entire document if not specified, you can give code only according to the parts required. 
Your output should be enclosed within ```latex and ``` only. Do not give any other output other than the Latex code please!"'''
        self.user_prompt:str = user_prompt
        self.response:str = ""

    @create_and_send_prompt
    def _send_prompt(self):
        self.user_prompt = "TASK INSTRUCTIONS: " + self.user_prompt
        return Prompt(system_prompt=self.system_prompt, user_prompt=self.user_prompt, model=self.model)

    def get_response(self):
        self.response = self._send_prompt()

