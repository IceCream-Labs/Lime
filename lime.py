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





from argparse import ArgumentParser
from src.Tester.tester import Tester


if __name__ == "__main__":
    parser = ArgumentParser(
        description="LIMA for evaluating your LLM responses"
    )
    parser.add_argument(
        '--openai_key',
        type=str,
        help = "OpenAI Key for openai as language model in langauge model evaluation",
        default = ""
    )
    parser.add_argument(
        '--testset_path',
        type = str,
        help = "Test set path, it should include the model responses and the ground truth and have to be either in CSV or XLSX format",
        required = True
    )
    parser.add_argument(
        '--test_type',
        type = str,
        help = """
        Type of Test:
        be -> Binary Evaluation,
        lme -> Language Model Evaluation,
        bee -> BiEncoder Evaluation,
        all -> All Evalution tests will be run""",
        required = True
    )
    parser.add_argument(
        '--ground_truth_col',
        type = str,
        help = "Name of the column in the test set that contains the ground truth",
        required = True
    )
    parser.add_argument(
        '--model_response_col',
        type = str,
        help = "Name of the column in the test set that contains the model responses",
        required = True
    )
    parser.add_argument(
        '--query_col',
        type = str,
        help = "Name of the column in the test set that contains the queries or questions",
        required = True
    )
    parser.add_argument(
        '--context_col',
        type = str,
        help = "Name of the column in the test set that contains the contexts for the queries",
        required = True
    )
    parser.add_argument(
        '--test_name',
        type = str,
        help = "To write the results with this name",
        required = True
    )

    args_dict = vars(parser.parse_args())

    tester = Tester(**args_dict)
    tester()

    




