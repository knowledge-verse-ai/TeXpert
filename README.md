# TeXpert

## Abstract

LaTeX's precision and flexibility in typesetting have made it the gold standard for the preparation of scientific documentation. Large Language Models (LLMs) present a promising opportunity for researchers to produce publication-ready material using LaTeX with natural language instructions, yet current benchmarks completely lack evaluation of this ability. By introducing TeXpert, our benchmark dataset with natural language prompts for generating LaTeX code focused on components of scientific documents across multiple difficulty levels, we conduct an in-depth analysis of LLM performance in this regard and identify frequent error types. Our evaluation across open and closed-source LLMs highlights multiple key findings: LLMs excelling on standard benchmarks perform poorly in LaTeX generation with a significant accuracy drop-off as the complexity of tasks increases; open-source models like DeepSeek v3 and DeepSeek Coder strongly rival closed-source counterparts in LaTeX tasks; and formatting and package errors are unexpectedly prevalent, suggesting a lack of diverse LaTeX examples in the training datasets of most LLMs.

<img width=800pt  src="https://github.com/user-attachments/assets/11777bfb-cc89-436d-b8bc-931590aaeb47">
<br>
<p align=center><em>Process used to create the TeXpert dataset along with the schema description </em></p>


## Installation

1. Clone the repository
2. Optional: Create a Python virtual environment
3. Run:
   
```
pip install -r requirements.txt
```
4. Create a .env file with LLM API keys as required

## Usage

Set the test parameters in main_test.py.
```
model = <model-name>
difficulty_class = <Simple/Average/Hard>
dataset_path = <path-to-dataset>
```
Then run main_eval.py, results will be stored as an Excel file in the results folder with the file name as {model}_{difficulty_class}_results.xlsx.

## Contributing

We appreciate any additional requests and/or contributions to TeXpert. The issues tracker is used to keep a list of features and bugs to be worked on. Please contact the authors for contributions.
