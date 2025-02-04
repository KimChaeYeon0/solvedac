import sys, os, sqlite3
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from hashlib import sha1

connect = sqlite3.connect("acmipc.db")
cursor = connect.cursor()

# def main(args="https://www.acmicpc.net/problem/1463"):
def main(args):
    link = f"https://www.acmicpc.net/problem/{args}" if args.isnumeric() else args
    id = int(link.split("/")[-1])
    cursor.execute("CREATE TABLE IF NOT EXISTS RAW_TABLE (id integer PRIMARY_KEY, content blob)")
    cursor.execute("SELECT id, content FROM RAW_TABLE WHERE id = ?", (id,))
    found = cursor.fetchone()
    if not found:
        # if id do not exist, read from bs4
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        req = Request(link, headers=headers)
        content = BeautifulSoup(urlopen(req), 'html.parser')
        cursor.execute("INSERT INTO RAW_TABLE VALUES (?, ?)", (id, str(content)))
        connect.commit()
    else:
        (id_found, content_found) = found
        content = BeautifulSoup(content_found, 'html.parser')
    title = " ".join(content.title.getText().split(" ")[1:])
    h = sha1()
    h.update(title.encode('utf-8'))
    print(h.hexdigest())
if __name__ == '__main__':
    # main()
    main(sys.argv[1])