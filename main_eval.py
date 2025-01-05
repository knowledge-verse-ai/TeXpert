import pandas as pd, xlsxwriter
from core.prompt_runner import LatexGenerationPromptRunner
from core.result_parser import LatexResponseAnalyser

if __name__ == "__main__":
    model = '' # select from ['gpt-4o-mini','gpt-4o','gemini-1.5-flash','claude-3-5-sonnet-latest','mistral-large-lastest','grok-2-1212','codestral-latest','deepseek-chat','deepseek-coder']
    difficulty_class = '' # select from ['Simple','Average','Hard']
    dataset_path = ''
    df = pd.read_excel(dataset_path,sheet_name=difficulty_class) # add the path to the TeXpert excel file 
    if 'Result' not in df.columns:
        df['Result'] = None
    if 'Error Type' not in df.columns:
        df['Error Type'] = None
    if 'Error Description' not in df.columns:
        df['Error Description'] = None
    for index, row in df.iterrows():
        try:
            prompt_id = row['ID']
            user_prompt = row['Task Instructions']
            prompt_runner = LatexGenerationPromptRunner(prompt_id=prompt_id,model=model,user_prompt=user_prompt)
            prompt_runner.get_response()
            response_analyser = LatexResponseAnalyser(task_prompt=prompt_runner.user_prompt, difficulty_class=difficulty_class, response=prompt_runner.response, response_from_model=model)
            if difficulty_class.lower() == "hard":
                sample_code = row['LaTeX Code']
                result = response_analyser.analyse_response(sample_code)
                if response_analyser.extracted_code:
                    df.at[index, 'LLM LaTeX Code'] = response_analyser.extracted_code
                else:
                    df.at[index, 'LLM LaTeX Code'] = ""
            else:
                result = response_analyser.analyse_response()
                if response_analyser.extracted_code:
                    df.at[index, 'LaTeX Code'] = response_analyser.extracted_code
                else:
                    df.at[index, 'LaTeX Code'] = ""
            df.at[index, 'Result'] = "Success" if result else "Fail"
            if result == False:
                df.at[index, 'Error Type'] = response_analyser.error_type
                df.at[index, 'Error Description'] = response_analyser.error_description
            print(f"Processed {index+1} of {len(df)}")
        except Exception as e:
            print(f"Error processing {index+1} of {len(df)}")
            df.at[index, 'Result'] = "Fail"
            df.at[index, 'Error Type'] = "Capability Error"
            
    df.to_excel(f'results/{model}_{difficulty_class.lower()}_results.xlsx', index=False,engine='xlsxwriter')
    print(f"Results saved to results/{model}_{difficulty_class.lower()}_results.xlsx")