#!/usr/bin/env python3

#### NOTE: ONLY FOR ONE PAGE STANDINGS (FOR NOW), go to standings page, copy source code (html) to input.html

from bs4 import BeautifulSoup

page = open('input.html', 'r', encoding="utf-8").read()
file_out = open('output.txt', 'w', encoding='utf-8')

soup = BeautifulSoup(page, "html.parser")  # page is from request or from file

table = soup.find('table', class_ = 'table-standings')

# get child thead of table
thead = table.find('thead')

# get first row of thead
row = thead.find('tr')

# get fifth to remaining in row
headers = row.find_all('th')[4:]

problems = []
solve_counts = {}

for header in headers:
    problems.append(header.text)

file_out.write(' '.join(problems)+'\n')

# get tbody of table
tbody = table.find('tbody')

# get all rows of tbody
rows = tbody.find_all('tr')

for row in rows:
    # get second cell in row
    name = row.find_all('td')[1].text
    # convert contiguous whitespace to single space of name
    name = ' '.join(name.split())

    print(name)
    
    # get remaining cells of row
    cells = row.find_all('td')[4:]
    i = 0
    solved_any = False
    for i in range(len(problems)):
        cell = cells[i]
        child = cell.find('a')
        if child and child.text != '':
            div = child.find('div')
            if 'label-success' in div['class']:
                solved_any = True
                div = child.find_all('div')[2]
                attempt_count, solved_time = map(int, div.text[0:-1].split(' ('))
                non_ac_count = attempt_count - 1
                file_out.write(name + ' ---- ' + problems[i] + ' ' + str(solved_time) + ' ' + str(non_ac_count)+'\n')

        i += 1
        
    if not solved_any:
        file_out.write(name + ' ----\n')

file_out.close()