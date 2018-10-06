import os
from pathlib import Path
import json


def resume_summary(resume_path):

        # change path later..
    BASE_PATH = "/home/jigar/Desktop/EventManagement/ResumeParser/ResumeTransducer"

    os.chdir(BASE_PATH)

    os.system('export GATE_HOME="..\\GATEFiles"')

    parse_command = "java -cp 'bin/*:../GATEFiles/lib/*:../GATEFiles/bin/gate.jar:lib/*' code4goal.antony.resumeparser.ResumeParserProgram"

    os.system(parse_command + " " + resume_path + " tmp.json")

    json_string = Path('tmp.json').read_text()
    # os.system("rm tmp.json")

    return json_string


def recurse(dicx, dix):

    for key, value in dicx.items():
        if type(value) == type([]):
            for i in value:
                recurse(i, dix)
        elif type(value) == type("string"):
            dix[key] = value

    return dix


def summarize(resume_path):

    string = resume_summary(resume_path)
    dic = json.loads(Path("tmp.json").read_text())

    # print(dic)
    dix = dict()

    dix = recurse(dic, dict())

    # print("IDHAR")
    # print(dix)

    return dix


if __name__ == "__main__":
        # change path later..
    string = resume_summary("/home/jigar/Desktop/EventManagement/resume1.pdf")

    dic = json.loads(Path("tmp.json").read_text())

    print(dic)

    recurse(dic)
    print(dix)
    # print(dic["education_and_training"][0]['EDUCATION'].replace(r"\n\n", " "))
