from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from .githubapi import gitHubProfileAnalyzer
import re


def get_links(text, url):
    match = [x[x.find(url):] for x in re.split('\n| |\)|\(|\{|\}|\[|\]|\'|\"', text) if url in x[x.find(url):]]
    print(match)
    return match


def get_github_username(github_links):
    for github_link in github_links:
        if github_link.endswith("/"):
            github_link = github_link[:-1]
        split_url = github_link.split('/')
        if len(split_url) == 2:
            github = gitHubProfileAnalyzer(split_url[1])
            if github.is_user():
                return split_url[1]
    return ""


def get_linkedin_username(linkedin_links):
    for linkedin_link in linkedin_links:
        if linkedin_link.endswith("/"):
            linkedin_link = linkedin_link[:-1]
        split_url = linkedin_link.split('/')
        if len(split_url) == 3 and split_url[1] == "in":
            return split_url[2]
    return ""


def get_codechef_username(codechef_links):
    for codechef_link in codechef_links:
        if codechef_link.endswith("/"):
            codechef_link = codechef_link[:-1]
        split_url = codechef_link.split('/')
        if len(split_url) == 3 and split_url[1] == "users":
            return split_url[2]
    return ""


def get_mobile_number(myContent):

    pattern = re.compile(r'((\+91)?\-?[0-9]{10})')

    results = pattern.findall(myContent)

    return (results[0][0])


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    text = ""

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
        annotationList = []
        try:
            annotationList = page.annots.resolve()
        except:
            annotationList = page.annots
        for annotation in annotationList:
            annotationDict = {}
            try:
                annotationDict = annotation.resolve()
            except:
                annotationDict = annotation
            if str(annotationDict["Subtype"]) != "/'Link'":
                # Skip over any annotations that are not links
                continue
            uriDict = annotationDict["A"]
            # This has always been true so far.
            if str(uriDict["S"]) != "/'URI'":
                continue
            # Some of my URI's have spaces.
            uri = (uriDict["URI"]).decode('ascii', 'ignore').replace(" ", "%20")
            text = text + " " + uri

    text = text + " " + retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


if __name__ == '__main__':

    myContent = str(convert_pdf_to_txt('resume5.pdf').encode('ascii', 'ignore')).replace(r"\n", " ")
    print("HELLOWORLD")
    print(myContent)
    print(get_mobile_number(myContent))
    print(get_github_username(get_links(myContent, "github.com")))
    # print(get_links(myContent, "github.com"))
    print(get_linkedin_username(get_links(myContent, "linkedin.com")))
    print(get_codechef_username(get_links(myContent, "codechef.com")))
