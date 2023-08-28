from src.Tester.languageModelAssessor import LanguageModelAssessor
from src.Tester.biEncoderAssessor import BiEncoderAssessor
import pandas as pd
import os
from src.Utils.config import Config

class Tester(LanguageModelAssessor, BiEncoderAssessor):
    def __init__(self,
        openai_key: str,
        testset_path: str,
        test_type: str,
        ground_truth_col: str,
        model_response_col: str, 
        query_col: str,
        context_col: str,
        test_name: str
    ):
        self.test_type = test_type
        self.test_name = test_name
        self.file_extension = testset_path.split(".")[-1].lower()

        # Checking file extension
        if self.file_extension in Config.ALLOWED_FILE_EXTENSION:
            if self.file_extension == "csv":
                self.testset_df = pd.read_csv(testset_path)
            else:
                self.testset_df = pd.read_excel(testset_path)
        else:
            raise "File should either be XLSX and CSV format."
        
        LanguageModelAssessor.__init__(
            self,
            openai_key=openai_key,
            testset_df=self.testset_df,
            ground_truth_col=ground_truth_col,
            model_response_col=model_response_col,
            query_col=query_col,
            context_col=context_col
        )
        BiEncoderAssessor.__init__(
            self,
            testset_df=self.testset_df,
            ground_truth_col=ground_truth_col,
            model_response_col=model_response_col
        )

    def __call__(self):
        """
        
        Perform testing based on test_type
        
        """
        if self.test_type == "be":
            pass
        if self.test_type == "lme":
            self.run_lma_eval()
        elif self.test_type == "bee":
            self.run_biencoder_eval()
        else:
            self.run_lma_eval()
            self.run_biencoder_eval()

        # Saving the results in results directory
        if not os.path.exists("./results"):
            os.mkdir("./results")

        filepath = f"./results/{self.test_name}.{self.file_extension}"
        self.testset_df.to_excel(filepath, index = False)
        print(f"Saving results to {filepath}")


        # Printing results
        ca_score, biencoder_score = "NA", "NA"
        if "ca_score" in self.testset_df.columns:
            ca_score = sum(self.testset_df["ca_score"])/len(self.testset_df)
        if "biencoder_score" in self.testset_df.columns:
            biencoder_score = sum(self.testset_df["biencoder_score"])/len(self.testset_df)
        
        ca_score = "NA" if ca_score == "NA" else round(ca_score, 3)
        biencoder_score = "NA" if biencoder_score == "NA" else round(biencoder_score, 3)
        print(f"""
        -----------------------------------------------------
        |   Language Model Score  |    BiEncoder Score      |
        -----------------------------------------------------
        |           {ca_score}    |         {biencoder_score}              |      
        -----------------------------------------------------
                    
        """)