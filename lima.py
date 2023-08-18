from argparse import ArgumentParser
from src.Tester.tester import Tester


if __name__ == "__main__":
    parser = ArgumentParser(
        description="LIMA Tester for testing LLM responses"
    )
    parser.add_argument(
        '--openai_key',
        type=str,
        help = "OpenAI Key to needed for Conversational AI Test",
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
        type = int,
        help = "Type of Test,\ncat -> Conversational AI Test\nbet -> BiEncoder Test\nboth -> Both",
        required = True
    )
    parser.add_argument(
        '--ground_truth_col',
        type = str,
        help = "Name of the column in the test set that holds the ground truth",
        required = True
    )
    parser.add_argument(
        '--model_response_col',
        type = str,
        help = "Name of the column in the test set that holds the model responses",
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

    




