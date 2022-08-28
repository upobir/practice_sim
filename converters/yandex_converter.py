#!/usr/bin/env python3

#### NOTE: ONLY FOR CHROME/CHROMIUM BROWSER, go to standings page, copy the sandings from all pages and paste
#### copy the header row from first page only.
#### don't have to care about a row appearing multiple times

with open('input.txt', 'r', encoding="utf-8") as f:
    lines = f.readlines()

lines = [line if line[-1] != '\n' else line[:-1] for line in lines]

assert lines[0].split('\t') == ['#', 'ParticipantY', '']
line_num = 1

problems = []
solve_counts = {}

while True:
    if len(lines[line_num]) == 1:
        problem = lines[line_num]
        problems.append(problem)
        line_num += 1

        solve_counts[problem], _ = map(int, lines[line_num].split('/'))
        line_num += 1
    else:
        assert lines[line_num].split('\t') == ['Score', 'Penalty']
        line_num += 1
        break

file_out = open('output.txt', 'w', encoding='utf-8')

file_out.write(' '.join(problems)+'\n')

seen = set()

while line_num < len(lines):
    rank = lines[line_num]
    line_num += 1

    name = lines[line_num]
    line_num += 1

    first_time = name not in seen
    
    if first_time:
        print(rank, name)

    calculated_penalty = 0
    calculated_solved = 0
    
    for x in problems: 
        if lines[line_num][0] == '-':
            line_num += 2

        elif lines[line_num][0] == '—':
            line_num += 1

        elif lines[line_num][0] == '+':
            non_ac_count = int(lines[line_num][1:]) if len(lines[line_num]) > 1 else 0
            calculated_solved += 1
            line_num += 1
            
            h, m = map(int, lines[line_num].split(':'))
            solved_time = h*60+m
            calculated_penalty += solved_time + non_ac_count * 20
            line_num += 1

            if first_time:
                file_out.write(name + ' ---- ' + x + ' ' + str(solved_time) + ' ' + str(non_ac_count)+'\n')

        else:
            assert False

    solved, penalty = map(int, lines[line_num].split('\t'))
    line_num +=1

    if first_time:
        seen.add(name)

file_out.close()