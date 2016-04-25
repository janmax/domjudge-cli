from requests_toolbelt import MultipartEncoder
from lxml import html
from login import login
import requests
import argparse


# static data
host = "http://algo.tcs.informatik.uni-goettingen.de/"


def parseme():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--score',
        help='Display the current score for all problems and exit',
        action='store_true')
    parser.add_argument(
        'task',
        help='The number of this weeks problem set. (default: %(default)s)',
        choices=range(1,13),
        type=int,
        nargs='?',
        default=1,
        metavar='TASK')
    parser.add_argument(
        'letters',
        help='''The problem(s) you want to submit. For example: to submit
        problems C, D and E enter submit.py 02 CDE. (default: %(default)s)''',
        nargs='?',
        default='ABCDE',
        metavar='LETTERS')

    args = parser.parse_args()
    return args.score, args.task, args.letters


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
        res = ('Success', task, letter, '')
    else:
        res = ('Failed',  task, letter, ' not')
    print("[{}] Task {:02d} problem {}{} submitted".format(*res))


def get_xpath(session, url, xpath):
    page = session.get(url)
    tree = html.fromstring(page.content)
    return tree.xpath(xpath)


def display_score(session):
    td_list = get_xpath(
        session, host + 'team', '//*[@id="teamscoresummary"]/table/tbody/tr/td')
    print("\nRANK\tSOLVED\tTIME\tA\tB\tC\tD\tE")
    print("{rank}\t{solved}\t{time}\t{A}\t{B}\t{C}\t{D}\t{E}".format(
        rank=td_list[0].text,
        solved=td_list[3].text,
        time=td_list[4].text,
        **{letter : score for letter, score in zip("ABCDEFGHIJ",
            [td.text for td in td_list if td.attrib['class'].startswith('score_')])}
    ))


def main():
    score, task, letters = parseme()

    # session create and login
    s = requests.Session()
    r = s.post(host + "public/login.php", data=login)

    # display score
    if score:
        display_score(s)
        return

    # retrieving problem ids
    li_list = get_xpath(s, host + 'team/problems.php', '/html/body/ul/li/a')
    probid = {letter: li.attrib['href'].split(
        '=')[1] for li, letter in zip(li_list, 'ABCDEFGHIJ')}

    # submitting selected problems
    for letter in letters:
        submit_problem(task, letter, s, probid)

main()
