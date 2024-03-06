#####################################################################################################
## LIME is a framework to test and evaluate LLMs on custom datasets and tasks
## Copyright (C)2023 IceCreamlabs Inc
##
## This program is free software: you can redistribute it and/or modify it under the terms of the 
## GNU Affero General Public License as published by the Free Software Foundation, either version 3
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
## without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
## See the GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License along with this program.
## If not, see <https://www.gnu.org/licenses/>.
##
## If your software can interact with users remotely through a computer network, 
## you should also make sure that it provides a way for users to get its source. 
## For example, if your program is a web application, its interface could display a "Source" link 
## that leads users to an archive of the code. There are many ways you could offer source, 
## and different solutions will be better for different programs; 
## see section 13 for the specific requirements.
#####################################################################################################


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
        
