from argparse import ArgumentParser
from .llm import chain
from .reader import read_files
import json
import os


def main():
    parser = ArgumentParser()
    parser.add_argument("essay_path", nargs='?',
                        help="The essay document", default="")
    parser.add_argument("-i", "--instruction", help="The instruction text")

    # Parse the arguments
    args = parser.parse_args()

    if args.instruction != None:
        instruction = args.instruction
    else:
        instruction = "請就這篇文章的文章內容、文章結構和英文文法，給一個60-100字的台灣繁體中文評語，並給出分數。"

    # Read the essay content from the file
    essay_collection = read_files(args.essay_path)
    for id in essay_collection:
        essay_content = essay_collection[id]

    # Read existing data from JSON file if it exists
    output_file = 'answer.json'

    # read output_file to dict
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []

    print("results", type(results))

    for id, essay_content in essay_collection.items():
        answer = chain.invoke(
            {"input": essay_content, "instruction": instruction})

        answer_dict = {
            "id": id,
            "content": answer.content,
        }

        results.append(answer_dict)

    # Write updated data back to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # mail = Mail(to="r12227113@ntu.edu.tw", subject="評語",
    #             content="評語：" + answer.content)
    # res = send_mail(mail)
    # print(res)

def save_results(new_results, output_file = 'answer.json'):
    # read output_file to dict
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []

    results.extend(new_results)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def grade_batch(essays_path: str, instruction: str) -> list:
    essay_collection = read_files(essays_path)

    results = []
    for id, essay_content in essay_collection.items():
        answer = chain.invoke(
            {"input": essay_content, "instruction": instruction})

        answer_dict = {
            "id": id,
            "grade_content": answer.content,
        }

        results.append(answer_dict)

    print(results)
    return results


if __name__ == "__main__":
    main()
