class Config:
    ALLOWED_FILE_EXTENSION = ["csv", "xlsx"]
    BIENCODER_HF_PATH = "sentence-transformers/all-mpnet-base-v2"
    MAX_RETRIES = 5
    SLEEP_TIME = 30
    CA_PROMPT = '''\n"{context}"\n<question>:{question}\n<answer>:{answer}\n<expert>:'''
    CA_SYSTEM_PROMPT = """The following is a conversation between a human and an AI product expert. The human will provide you a context based on which a question is asked. The AI product expert will analyze, comprehend and understand the context and question. The question will be followed by an answer which the AI product expert has to score based on a scale from 1 to 100 and has to give a proper explanation about the scoring. The question will start from "<question>:", the answer will start from "<answer>:" and the AI product expert will start from "<expert>:". The AI product expert will provide the score and the explanation in a proper JSON format."""