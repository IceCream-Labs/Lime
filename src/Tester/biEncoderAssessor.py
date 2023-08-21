import pandas as pd
from tqdm import tqdm 
from colorama import Fore
from sentence_transformers import SentenceTransformer, util
from src.Utils.config import Config

class BiEncoderAssessor:
    def __init__(self, testset_df: pd.DataFrame, ground_truth_col: str, model_response_col: str):
        self.encoder = SentenceTransformer(Config.BIENCODER_HF_PATH)
        self.ground_truth_col = ground_truth_col
        self.model_response_col = model_response_col
        self.testset_df = testset_df
    
    def run_biencoder_eval(self):
        """
        Method to run Bi Encoder evaluation

        """        
        N = len(self.testset_df)
        pbar = tqdm(total=N, desc="BiEncoder Evaluation", bar_format="{l_bar}%s{bar:50}%s{r_bar}" % (Fore.CYAN, Fore.RESET), position=0, leave=True)
        for idx, row in self.testset_df.iterrows():
            ground_truth = row[self.ground_truth_col]
            model_response = row[self.model_response_col]
            answer_embedding = self.encoder.encode(ground_truth, convert_to_tensor=True)
            model_answer_embedding = self.encoder.encode(model_response, convert_to_tensor=True)
            cosine_score = util.cos_sim(answer_embedding, model_answer_embedding)
            self.testset_df.loc[idx, f"biencoder_score"] = float(cosine_score[0][0])*100
            pbar.update(1)
        
