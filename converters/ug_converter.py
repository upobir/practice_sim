#!/usr/bin/env python3

#### NOTE: run this script with all the html files as arguments

from bs4 import BeautifulSoup
import sys

file_out = open('output.txt', 'w', encoding='utf-8')

problems = []
solve_counts = {}

for i in range(1, len(sys.argv)):
    page = open(sys.argv[i], 'r', encoding="utf-8").read()
    soup = BeautifulSoup(page, "html.parser")  # page is from request or from file

    table = soup.find('table', class_ = 'table table-bordered table-striped table-text-center table-vertical-middle table-condensed')
    thead = table.find('thead')
    row = thead.find('tr')
    headers = row.find_all('th')[3:]

    if len(problems) == 0:
        for header in headers:
            problems.append(header.find('a').text)
        file_out.write(' '.join(problems)+'\n')

    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    for row in rows:
        name = row.find_all('td')[1].text
        name = ' '.join(name.split())
        i = name.find(')')
        if i != -1 and i+1 < len(name) and name[i+1] != ' ':
            name = name[:i+1] + ' ' + name[i+1:]

        print(name)

        cells = row.find_all('td')[3:]
        i = 0
        solved_any = False
        for i in range(len(problems)):
            cell = cells[i]
            if cell.text == '':
                continue

            divs = cell.find_all('div')
            result = divs[0].text
            if result[0] == '-':
                continue
            
            solved_any = True

            non_ac_count = 0
            if len(result) > 1:
                non_ac_count = int(result)
            
            hour, minute = divs[1].text.split(':')
            solved_time = int(hour) * 60 + int(minute)

            file_out.write(name + ' ---- ' + problems[i] + ' ' + str(solved_time) + ' ' + str(non_ac_count)+'\n')

        if not solved_any:
            file_out.write(name + ' ----\n')
    print('-'*100)



file_out.close()