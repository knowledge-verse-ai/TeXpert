import re,ast
from typing import Optional
from core.llm_interface import create_and_send_prompt, Prompt

class LatexResponseAnalyser:
    def __init__(self, task_prompt:str, difficulty_class: str, response: str, response_from_model: str):
        self.task_prompt : str = task_prompt  
        self.difficulty_class : str = difficulty_class
        self.response : str = response
        self.response_from_model : str = response_from_model
        self.extracted_code : str = ""
        self.result : bool
        self.error_type : Optional[str] = None
        self.error_description : Optional[str] = None

    def _extract_latex_code(self):
        pattern = r'(```latex.*?```)'
        matches = re.search(pattern, self.response, re.DOTALL)

        if matches:
            self.extracted_code = matches.group(1).strip()
            if self.extracted_code.startswith(r"```latex") and self.extracted_code.endswith(r"```"):
                self.result = True
        else:
            self.result = False

    @create_and_send_prompt
    def _judge_hard_response(self, sample_code):
        system_prompt = r'''You are a judge tasked with evaluating the given GENERATED LATEX CODE against the TASK INSTRUCTIONS. 
You are also provided a SAMPLE LATEX CODE that has been verified to meet each and every requirement from TASK INSTRUCTIONS for your reference.
Analyze the GENERATED LATEX CODE thoroughly to determine if it satisfies the instructions completely and without errors. Use the SAMPLE LATEX CODE only as a reference to identify any discrepancies, as there can be multiple ways to achieve TASK INSTRUCTIONS.
Check each and every line and command with utmost care for the following types of errors:
1. Capability Error: The LLM fails or denies to provide a valid response or says the task is out of its capability.
Examples:
LLM responds with: "Sorry, I cannot…"
LLM does not include any code in response at all.

2. Syntax Error: The code does not follow valid LaTeX syntax.
Examples:
Missing closing braces.
Unescaped special characters.

3. Logical Error: The code does not fulfill all requirements as given in the task instructions.
Examples:
Table headers omitted when explicitly requested.
Missing components or incorrect logic in the code.

4. Package Error: Necessary LaTeX packages for the code are missing, or commands used are incompatible with the document type.
Examples:
Using \includegraphics without importing the graphicx package.
Using \chapter in a document class that does not support chapters.

5. Formatting Errors: Errors in layout, alignment, spacing, or referencing. But, make sure to ignore errors where the LaTeX code is missing the 'references.bib' file, it is not needed anywhere!
Examples:
Misaligned tables with inconsistent column widths.
Using custom references like \ref{sec:1} without defining \label{sec:1}.

YOUR TASK:
Evaluate the GENERATED LATEX CODE for errors of the above types. If no errors are present, return 'error' as 'No' in below format.
Provide your evaluation only and only in the following Python dictionary format:
```
{
    "error": "Yes" or "No",
    "error_types": list of error types if error is 'Yes', else empty list,
    "description": "description of error(s) encountered if error is 'Yes', else empty string"
}
```
Return only this dictionary as the output. Make sure the output is parseable using Python's ast.literal_eval function.
'''
        user_prompt = self.task_prompt + "\SAMPLE LATEX CODE: \n" + sample_code + "\nGENERATED LATEX CODE: \n" + self.extracted_code
        return Prompt(system_prompt=system_prompt, user_prompt=user_prompt, model="gpt-4o")

        
    @create_and_send_prompt
    def _judge_simple_avg_response(self):
        system_prompt = r'''You are a judge tasked with evaluating the given LATEX CODE against the TASK INSTRUCTIONS. 
Analyze the LaTeX code thoroughly to determine if it satisfies the instructions completely and without errors. 
Check each and every line and command with utmost care for the following types of errors:
1. Capability Error: The LLM fails or denies to provide a valid response or says the task is out of its capability.
Examples:
LLM responds with: "Sorry, I cannot…"
LLM does not include any code in response at all.

2. Syntax Error: The code does not follow valid LaTeX syntax.
Examples:
Missing closing braces.
Unescaped special characters.

3. Logical Error: The code does not fulfill all requirements as given in the task instructions.
Examples:
Table headers omitted when explicitly requested.
Missing components or incorrect logic in the code.

4. Package Error: Necessary LaTeX packages for the code are missing, or commands used are incompatible with the document type.
Examples:
Using \includegraphics without importing the graphicx package.
Using \chapter in a document class that does not support chapters.

5. Formatting Errors: Errors in layout, alignment, spacing, or referencing. But, make sure to ignore errors where the LaTeX code is missing the 'references.bib' file, it is not needed anywhere!
Examples:
Misaligned tables with inconsistent column widths.
Using custom references like \ref{sec:1} without defining \label{sec:1}.

YOUR TASK:
Evaluate the LATEX CODE for errors of the above types. If no errors are present, return 'error' as 'No' in below format.
Provide your evaluation only and only in the following Python dictionary format:
```
{
    "error": "Yes" or "No",
    "error_types": list of error types if error is 'Yes', else empty list,
    "description": "description of error(s) encountered if error is 'Yes', else empty string"
}
```
Return only this dictionary as the output. Make sure the output is parseable using Python's ast.literal_eval function.
'''
        user_prompt = self.task_prompt + "\nLATEX CODE: \n" + self.extracted_code
        return Prompt(system_prompt=system_prompt, user_prompt=user_prompt, model="gpt-4o")

    def analyse_response(self, sample_code = None):
        self._extract_latex_code()
        if not self.result:
            self.error_type = "Capability Error"
            return self.result
        if self.difficulty_class.lower() == "hard":
            eval = self._judge_hard_response(sample_code)
        else:
            eval = self._judge_simple_avg_response()
        if eval.startswith("```python"):
            eval = eval.replace('```python', '').replace('```', '').strip()
        eval = ast.literal_eval(eval)
        self.result = eval['error']
        if self.result == "Yes":
            self.result = False
            self.error_type = ", ".join(eval['error_types'])
            self.error_description = eval['description']
        else:
            self.result = True
        return self.result