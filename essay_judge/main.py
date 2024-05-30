from argparse import ArgumentParser
from llm import chain
from mail import Mail, send_mail
from reader import read_file


def main():
    parser = ArgumentParser()
    parser.add_argument("essay_path", nargs='?',
                        help="The essay document", default="")
    parser.add_argument("-i", "--instruction", help="The instruction text")

    args = parser.parse_args()

    essay_content = read_file(args.essay_path)
    if len(args.instruction) != 0:
        instruction = args.instruction
    else:
        instruction = "請就這篇文章的文章內容、文章結構和英文文法，給一個60-100字的台灣繁體中文評語，並給出分數。"

    answer = chain.invoke(
        {"input": essay_content, "instruction": instruction})
    print("=================\n", answer)

    # mail = Mail(to="r12227113@ntu.edu.tw", subject="評語",
    #             content="評語：" + answer.content)
    # res = send_mail(mail)
    # print(res)


def process_essay(to: str, subject: str, essay_path: str, instruction: str):
    essay_content = read_file(essay_path)
    answer = chain.invoke({"input": essay_content, "instruction": instruction})
    mail = Mail(to=to, subject=subject, content="評語：\n" + answer.content)
    res = send_mail(mail)
    print(res)


if __name__ == "__main__":
    main()
