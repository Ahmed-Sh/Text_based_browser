import requests
from bs4 import BeautifulSoup
import os
import sys
from collections import deque
from colorama import Fore


argv = sys.argv
dirName = argv[1]
try:
    # Create target Directory
    os.mkdir(dirName)
    # or we can use the following avoiding try except
    # os.makedirs(dirName, exist_ok=True)
except FileExistsError:
    pass
x = os.getcwd()
my_path = x + "\\" + dirName


def create_file(path, content):
    with open(path, 'w+') as f:
        print(content, file=f, end='\n')


def read_file(path):
    with open(path, "r") as f:
        print(f.read())


def peek_stack(st):
    if st:
        return st[-1]    # this will get the last element of stack


def get_url_req(address):
    r = requests.get(address)
    r.encoding = "utf-8"
    return r.content


def making_soup(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()


'''
# another way of making_soup()
def making_soup(content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.find_all(["p", "a", "ul", "ol", "li"])
    print(text)
    output = ""
    for line in text:
        output += line.text + "\n"
    return output
'''


files = set()
stack = deque()

while True:
    url = input()
    if url == "exit":
        break
    elif "." in url or url in files:
        if url in files:
            existing_file_path = my_path + "\\" + url
            read_file(existing_file_path)
        else:
            file_name = url[:-4]
            file_path = my_path + "\\" + file_name
            files.add(file_name)
            stack.append(file_name)
            complete_address = "https://" + url
            r_content = get_url_req(complete_address)
            soup_out = making_soup(r_content)
            print(Fore.BLUE + soup_out)
            create_file(file_path, soup_out)
    elif url == "back":
        if len(stack) > 0:
            stack.pop()
            last_page = peek_stack(stack)
            if last_page:
                last_page_path = my_path + "\\" + last_page
                read_file(last_page_path)

    else:
        print("error")
