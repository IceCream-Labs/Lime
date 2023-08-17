import pandas as pd
import json
import re
from typing import Dict, List
import openai
from tqdm import tqdm 
from colorama import Fore
import time
from sentence_transformers import SentenceTransformer, CrossEncoder, util
class BiEncoderAssessor:
    def __init__(self):
        self.encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    
    def run_biencoder_eval(self, df):
        pbar = tqdm(total=len(df), desc="Scoring", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.CYAN, Fore.RESET), position=0, leave=True)
        for idx, row in df.iterrows():
            answer_embedding = self.encoder.encode(row["ground_truth"], convert_to_tensor=True)
            model_answer_embedding = self.encoder.encode("model_response", convert_to_tensor=True)
            cosine_score = util.cos_sim(answer_embedding, model_answer_embedding)
            df.loc[idx, f"biencoder_score"] = float(cosine_score[0][0])*100
            pbar.update(1)