from requests_toolbelt import MultipartEncoder
from lxml import html
from login import login
import requests
import argparse


def parseme():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'task',
        help='The number of this weeks problem set.',
        type=int,
        metavar='TASK')
    parser.add_argument(
        'letters',
        help='''The problem(s) you want to submit. For example: to submit
        problems C, D and E enter submit.py 02 CDE. (Default: A-E)''',
        default='ABCDE',
        metavar='LETTERS')

    args = parser.parse_args()
    return args.task, args.letters

# static data
host = "http://algo.tcs.informatik.uni-goettingen.de/"

def submit_problem(task, letter, session, probid):
    m = MultipartEncoder(fields={
        'code[]': (
            letter + '.cpp',
            open('{:02d}/{}.cpp'.format(task, letter), 'rb'),
            'application/octet-stream'
        ),
        'probid': probid[letter],
        'langid': 'cpp',
        'submit': 'submit',
    })

    r = session.post(host + "team/upload.php", data=m,
                     headers={'Content-Type': m.content_type})
    if r.status_code == 200:
        print(
            "[Success] Task {:02d} problem {} submitted".format(task, letter))
    else:
        print(
            "[Failed] Task {:02d} problem {} not submitted".format(task, letter))


def main():
    task, letters = parseme()

    # session create and login
    s = requests.Session()
    r = s.post(host + "public/login.php", data=login)

    # retrieving problem ids
    page = s.get(host + 'team/problems.php')
    tree = html.fromstring(page.content)
    r = tree.xpath('/html/body/ul/li/a')
    probid = {letter: li.attrib['href'].split(
        '=')[1] for li, letter in zip(r, 'ABCDEFGHIJ')}

    # submitting selected problems
    for letter in letters:
        submit_problem(task, letter, s, probid)

main()
