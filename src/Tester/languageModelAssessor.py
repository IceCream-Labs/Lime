import pandas as pd
from tqdm import tqdm
from colorama import Fore
import openai
from src.Utils.config import Config
import time
import pandas as pd
import json


class LanguageModelAssessor:
    def __init__(self, 
        openai_key: str, 
        testset_df: pd.core.frame.DataFrame, 
        ground_truth_col: str, 
        model_response_col: str,
        query_col: str,
        context_col: str
    ):
        self.openai_key = openai_key
        self.testset_df = testset_df
        self.ground_truth_col = ground_truth_col
        self.model_response_col = model_response_col
        openai.api_key = openai_key
        self.query_col = query_col
        self.context_col = context_col
                    

    @staticmethod
    def gptCaller(prompt: str):
        """

        Method to call openai Turbo

        """
        retries = 5
        response = ""
        for _ in range(retries):
            if response:
                break
            try:
                system_msg = ""
                response = openai.ChatCompletion.create(
                    model="gpt-4", 
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


    @staticmethod
    def getScore(prompt: str):
        """
        
        Method to parse the Language Model response
        
        """
        score = float(0)
        prompt = Config.CA_SYSTEM_PROMPT + "\n" + prompt
        model_response = LanguageModelAssessor.gptCaller(prompt)
        try:
            json_response = json.loads(model_response)
            if 'score' in json_response.keys():
                score = float(json_response["score"])
            elif 'expert' in json_response.keys():
                score = float(json_response['expert']["score"])
        except Exception as E:
            pass
            
        return score if 0 <= score and score <= 100 else 0.0

    def run_lma_eval(self):
        """
        
        Method to run the conversational AI Evaluation
        
        """
        N = len(self.testset_df)
        pbar = tqdm(total=N, desc="Language Model Evaluation", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.CYAN, Fore.RESET), position=0, leave=True)
        for idx, row in self.testset_df.iterrows():
            context = row[self.context_col]
            question = row[self.query_col]
            answer = row[self.model_response_col]
            prompt = Config.CA_PROMPT.format(context = context, question = question, answer = answer).strip()
            score_ = LanguageModelAssessor.getScore(prompt)
            self.testset_df.loc[idx, "ca_score"] = score_
            pbar.update(1)

            
