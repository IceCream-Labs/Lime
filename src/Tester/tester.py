from Testers.conversationalAIAssessor import ConversationalAIAssessor
from Testers.biEncoderAssesor import BiEncoderAssessor
import time
from tqdm import tqdm
from colorama import Fore
import pandas as pd

class Tester(ConversationalAIAssessor, BiEncoderAssessor):
    def __init__(self):
        super(ConversationalAIAssessor).__init_()
        super(BiEncoderAssessor).__init_()
    
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