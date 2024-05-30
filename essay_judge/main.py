from argparse import ArgumentParser 
from llm import chain
from mail import Mail, send_mail
from reader import read_file

parser = ArgumentParser()
parser.add_argument("essay_path", nargs='?',  help="The essay document", default="")
args = parser.parse_args()

essay_content = read_file(args.essay_path)

answer = chain.invoke({"input": essay_content})
print(answer)

mail = Mail(to="r12227113@ntu.edu.tw", subject="評語", content="評語：" + answer.content)
res = send_mail(mail)
print(res)

