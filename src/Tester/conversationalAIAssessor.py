# class ConversationalAIAssessor:
#     pass

from argparse import ArgumentParser
import pandas as pd
from tqdm import tqdm
from typing import Dict, List
import requests
from colorama import Fore
import time
import json
from collections import Counter
import re
import math
import openai


class TestConfig:
    MAX_RETRIES = 5
    API_KEY = "1a4d6eae8fdfab609ee5e010a96f6ce0c1686618"
    SLEEP_TIME = 30
    TESTET_PATH = "./Testset/testset_40qs.xlsx"


class Scorer:
    def jaccardSimilarity(self, string_1: str, string_2: str) -> float:
        """
        
        Method to get the Jaccard similarity between 2 texts
        
        """
        intersection = len(list(set(string_1.split()).intersection(string_2.split())))
        union = len(string_1.split()) + len(string_2.split()) - intersection

        return intersection / union

    def text2Vec(self, text: str) -> List[float]:
        """
        
        Method to convert the string to vector representation
        
        """
        words = re.compile(r"\w+").findall(text)
        return Counter(words)


    def cosineSimmilarity(self, string_1: str, string_2: str) -> float:
        """
        
        Method to get cosine similarity between two texts
        
        """
        vec1, vec2 = self.text2Vec(string_1), self.text2Vec(string_2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator



class Tester(Scorer):
    def __init__(self, url: str, api_key: str, test_name: str):
        self.url = url
        self.api_key = api_key
        self.test_name = test_name
        self.save_file_path = f"./Results/{self.test_name}.xlsx"

    def getTestset(self):
        """
        
        Method to load the test set
        
        """
        test_df = pd.read_excel(TestConfig.TESTET_PATH)
        test_df.fillna("", inplace = True)
        json_set = []
        for _, row in test_df.iterrows():
            json_set.append({
                "qtype": row["Type"],
                "context": row["Text"],
                "question": row["Question"],
                "ground_truth": row["Ground Truth"]
            })
        return json_set


    def gptCaller(self, prompt):
        """
        
        Helper function to call openai Turbo
        
        """
        retries = 5
        response = ""
        for _ in range(retries):
            if response:
                break
            try:
                system_msg = "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."

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
                time.sleep(TestConfig.SLEEP_TIME)
                error = str(E)
                print(f"[ERROR] {error}")
                if 'bill' in error:
                    return response

    def apiCaller(self, payload: Dict):
        """
        
        Method to call the API
        
        """
        headers = {'Accept': 'application/json', 'api-key': self.api_key}
        status_code = 500
        answer = ""
        params = payload
        for _ in range(TestConfig.MAX_RETRIES):
            if status_code == 200:
                break

            response = requests.get(
                url = self.url, 
                params=params,
                headers = headers,
            )

            if response.status_code == 200:
                status_code = 200
                answer = response.json()
                answer = answer["result"]
            else:
                time.sleep(TestConfig.SLEEP_TIME)
        

        return "FAILED" if answer == "" else answer
    

    def getJsonOuput(self, text: str):
        """
        
        Method to extract the JSON output from the model response
        
        """
        start, end = text.index('{'), text.rindex('}') + 1
        json_text = text[start: end]
        json_data = json.loads(json_text)

        return json_data

    def checkCorrectNess(self, ground_truth: str, model_output: str, qType: str) -> bool:
        """
        
        Method to check the correctness of the Model
        
        """
        correct, score = True, 1
        if qType == "Understanding" or qType == "Reasoning":
            correct = True if ground_truth in model_output else False
            score = int(correct)

        elif qType == "Truthfulness":
            pass        

        elif qType == "Data Retrieval":
            ground_truth_json = {}
            for pair in ground_truth.split("\n"):
                key, value = pair.split(":")
                ground_truth_json[key] = value
            

            
        return correct, score

    def __call__(self):
        results = []
        try:
            testData = self.getTestset()
            N = len(testData)
            
            # Collecting the model responses
            pbar = tqdm(total=N, desc="Collecting model responses", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.GREEN, Fore.RESET), position=0, leave=True)
            for json_data in testData:
                start_time = time.time()
                if self.url == "gpt":
                    answer = self.gptCaller(
                        prompt = f"""{json_data["context"]}. {json_data["question"]}"""
                    )
                else:
                    answer = self.apiCaller(
                        payload={
                            "context": json_data["context"],
                            "question": json_data["question"]
                        }
                    )
                end_time = time.time()
                json_data["model_response"] = answer
                json_data["time(mins)"] = round((end_time - start_time)/60, 3)
                results.append(json_data)
                pbar.update(1)

            # Checking the correctness of the model
            # pbar = pbar = tqdm(total=N, desc="Checking correctness", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.GREEN, Fore.RESET), position=0, leave=True)
            # for json_data in results:
            #     json_data["checker"] = self.checkCorrectNess(
            #         ground_truth = json_data["ground_truth"],
            #         model_output = json_data["model_response"],
            #         qType = json_data["qtype"]
            #     )

            results_df = pd.DataFrame.from_dict(results)
            results_df.to_excel(self.save_file_path, index = False)

        except KeyboardInterrupt:
            print("[INFO Saving the file]")
            # Saving the results
            results_df = pd.DataFrame.from_dict(results)
            results_df.to_excel(self.save_file_path, index = False)
        
        return self.save_file_path

            
