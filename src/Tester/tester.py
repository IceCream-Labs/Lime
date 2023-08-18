from src.Tester.conversationalAIAssessor import ConversationalAIAssessor
from src.Tester.biEncoderAssessor import BiEncoderAssessor
import pandas as pd
import os
from src.Utils.config import Config

class Tester(ConversationalAIAssessor, BiEncoderAssessor):
    def __init__(self, openai_key: str, testset_path: str, test_type: str, ground_truth_col: str, model_response_col: str, test_name: str):
        # Checking file extension
        self.file_extension = testset_path.split(".")[-1].lower()
        if self.file_extension in Config.ALLOWED_FILE_EXTENSION:
            if self.file_extension == "csv":
                testset_df = pd.read_csv(self.testset_path)
            else:
                testset_df = pd.read_excel(self.testset_path)
        else:
            raise "File should either be XLSX and CSV format."
        super(ConversationalAIAssessor).__init_(openai_key = openai_key, testset_df = testset_df, ground_truth_col = ground_truth_col, model_response_col = model_response_col)
        super(BiEncoderAssessor).__init_(testset_df = testset_df, ground_truth_col = ground_truth_col, model_response_col = model_response_col)
        self.test_type = test_type
        self.test_name = test_name
    
    def __call__(self):
        """
        
        Perform testing based on test_type
        
        """
        if self.test_type == "cat":
            self.run_ca_eval()
        elif self.test_type == "bet":
            self.run_biencoder_eval()
        else:
            self.run_ca_eval()
            self.run_biencoder_eval()

        # Saving the results in results directory
        if not os.path.exists("./results"):
            os.mkdir("./results")

        filepath = f"./results/{self.test_name}.{self.file_extension}"
        print(f"Saving results to {filepath}")