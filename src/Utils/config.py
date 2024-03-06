#####################################################################################################
##LIME is a framework to test and evaluate LLMs on custom datasets and tasks
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

class Config:
    ALLOWED_FILE_EXTENSION = ["csv", "xlsx"]
    BIENCODER_HF_PATH = "sentence-transformers/all-mpnet-base-v2"
    MAX_RETRIES = 5
    SLEEP_TIME = 30
    CA_PROMPT = '''\n"{context}"\n<question>:{question}\n<answer>:{answer}\n<expert>:'''
    CA_SYSTEM_PROMPT = """The following is a conversation between a human and an AI product expert. The human will provide you a context based on which a question is asked. The AI product expert will analyze, comprehend and understand the context and question. The question will be followed by an answer which the AI product expert has to score based on a scale from 1 to 100 and has to give a proper explanation about the scoring. The question will start from "<question>:", the answer will start from "<answer>:" and the AI product expert will start from "<expert>:". The AI product expert will provide the score and the explanation in a proper JSON format."""
