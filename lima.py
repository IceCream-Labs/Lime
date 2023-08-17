from argparse import ArgumentParser
from src.Tester.tester import Tester


if __name__ == "__main__":
    parser = ArgumentParser(
        description="LIMA Tester for testing LLM responses"
    )
    parser.add_argument(
        '--openai_key',
        type=str,
        help = "OpenAI Key to needed for Conv"
    )
    parser.add_argument(
        '--testset_path',
        type = str,
        help = "Test set path, it should include the model responses and the ground truth"
    )
    parser.add_argument(
        '--test_type',
        type = int,
        help = "Type of Test,\n0 -> Conversational AI Test\n1 -> BiEncoder Test\n2 -> Both"
    )
    parser.add_argument(
        '--ground_truth_field',
        type = str,
        help = "Name of the column in the test set that holds the ground truth",
    )
    parser.add_argument(
        '--model_responses',
        type = str,
        help = "Name of the column in the test set that holds the model responses"
    )

    args_dict = vars(parser.parse_args())

    tester = Tester(**args_dict)
    tester

    




