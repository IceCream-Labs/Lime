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

    




