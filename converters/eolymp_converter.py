#!/usr/bin/env python3

#### NOTE: run this script with all the html files as arguments, create the html files by copying from dev tools.

from bs4 import BeautifulSoup
import sys

file_out = open('output.txt', 'w', encoding='utf-8')

problems = []
solve_counts = {}

for i in range(1, len(sys.argv)):
    page = open(sys.argv[i], 'r', encoding="utf-8").read()
    soup = BeautifulSoup(page, "html.parser")  # page is from request or from file

    table = soup.find('table', class_ = 'MuiTable-root')
    thead = table.find('thead')
    row = thead.find('tr')
    headers = row.find_all('th')[5:-1]

    if len(problems) == 0:
        for header in headers:
            problems.append(header.text)
        file_out.write(' '.join(problems)+'\n')


    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    team_count = 0
    for row in rows:
        cells = row.find_all('td')
        name = cells[3].text + ' (' + ' '.join(cells[1].text.split()) + ')'
        name = ' '.join(name.split())

        print(name)

        cells = cells[5:-1]
        solved_any = False
        for i in range(len(problems)):
            cell = cells[i]
            if cell.text == '-':
                continue

            divs = cell.find_all('div')
            result = divs[0]
            childs = result.findChildren()
            
            if len(childs) == 0:
                continue
            
            solved_any = True

            non_ac_count = int(childs[1].text.split(' ')[0]) - 1
            
            hour, minute = childs[0].text.split(':')
            solved_time = int(hour) * 60 + int(minute)

            file_out.write(name + ' ---- ' + problems[i] + ' ' + str(solved_time) + ' ' + str(non_ac_count)+'\n')

        if not solved_any:
            file_out.write(name + ' ----\n')

        team_count += 1
        
    print('-'*100)



file_out.close()