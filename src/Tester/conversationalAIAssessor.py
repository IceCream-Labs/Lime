import pandas as pd
from tqdm import tqdm
from colorama import Fore
import openai
from src.Utils.config import Config
import time
import pandas as pd


class ConversationalAIAssessor:
    def __init__(self, openai_key: str, testset_df: pd.DataFrame, ground_truth_col: str, model_response_col: str):
        self.openai_key = openai_key, 
        self.testset_df = testset_df, 
        self.ground_truth_col = ground_truth_col, 
        self.model_response_col = model_response_col
   

    @staticmethod
    def gptCaller(prompt: str):
        """

        Helper function to call openai Turbo

        """
        retries = 5
        response = ""
        for _ in range(retries):
            if response:
                break
            try:
                system_msg = Config.CA_SYSTEM_PROMPT
                system_msg = system_msg.strip()
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages = [
                        {"role": "system", "content" : system_msg},
                        {"role": "user", "content" : prompt},
                    ]
                )
                if response['choices']:
                    return response['choices'][0]["message"]['content']
            except Exception as E:
                retries += 1
                time.sleep(30)
                error = str(E)
                print(f"[ERROR] {error}")
                if 'bill' in error:
                    return response

    def run_ca_eval(self):
        """
        
        Method to run the conversational AI Evaluation
        
        """
        pbar = tqdm(total=len(self.testset_df), desc="Conversation AI Evaluation", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.CYAN, Fore.RESET), position=0, leave=True)
        for idx, row in self.testset_df.iterrows():
            context = row["context"]
            question = row["question"]
            answer = row[self.model_response_col]
            prompt = Config.CA_PROMPT.format(context = context, question = question, answer = answer).strip()
            score_explanation = ConversationalAIAssessor.gptCaller(prompt)
            self.testset_df.loc[idx, "ca_score"] = score_explanation
            pbar.update(1)

            
