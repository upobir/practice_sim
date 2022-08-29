#!/usr/bin/env python3

import sys
import time
import datetime
import math

# submissions.txt has problem codes in first line separated by space
# then each line has 'team name ---- problem solve_time(in minutes) non_ac_count'
# if a team has no ac, then the part after ---- is empty

def parse_submissions(lines):
    problems = lines[0].split(' ')

    results = {}

    for line in lines[1:]:
        name, submission = [word.strip() for word in line.split('----')]
        
        if name not in results:
            results[name] = [None] * len(problems)

        if not results:
            continue
        
        problem, solve_time, non_ac_count = submission.split(' ')
        solve_time = int(solve_time)
        non_ac_count = int(non_ac_count)

        results[name][problems.index(problem)] = (solve_time, non_ac_count)

    return problems, results

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('usage:')
        print('\tprac_sim.py start <team_name>')
        print('\t\tcreates local.txt with start time and team name, default team name is YOU')
        print('\tprac_sim.py ac <problem> <non_ac_count')
        print('\t\tupdates local.txt ac submission of problem with non_ac_count')
        print('\tprac_sim.py rank <time_in_minutes>')
        print('\t\tgenerates rank list, time is optional, start time and current time used by default')
        print('')
        print('\tIn all cases, keep submissions.txt in working directory')


    else:
        with open('submissions.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        lines = [line if line[-1] != '\n' else line[:-1] for line in lines]
        problems, results = parse_submissions(lines)

        
        if sys.argv[1] == 'start':
        
            start_time = time.time()
            start_time_str = time.ctime(start_time)
            team_name = sys.argv[2] if len(sys.argv) > 2 else 'YOU'

            assert team_name not in results

            file_out = open('local.txt','w', encoding='utf-8')

            # print(start_time)
            # print(time.ctime(start_time))
            # print(datetime.datetime.strptime(time.ctime(start_time), "%a %b %d %H:%M:%S %Y").timestamp())

            file_out.write(start_time_str + '\n')
            file_out.write(team_name + '\n')

            file_out.close()

        elif sys.argv[1] == 'ac':

            problem = sys.argv[2]
            non_ac_count = sys.argv[3]

            cur_time = time.time()

            with open('local.txt', 'r', encoding='utf-8') as f:
                start_time = datetime.datetime.strptime(f.readline().strip(), "%a %b %d %H:%M:%S %Y").timestamp()
                team_name = f.readline().strip()
            
            assert problem in problems

            solve_time = math.floor((cur_time - start_time)/60)

            with open('local.txt', 'a', encoding='utf-8') as f:
                f.write(problem + ' ' + str(solve_time) + ' ' + str(non_ac_count) + '\n')
        
        elif sys.argv[1] == 'rank':

            cur_time = time.time()

            with open('local.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            lines = [line if line[-1] != '\n' else line[:-1] for line in lines]

            start_time = start_time = datetime.datetime.strptime(lines[0], "%a %b %d %H:%M:%S %Y").timestamp()
            team_name = lines[1]

            elapsed_time = (cur_time - start_time)/60

            if len(sys.argv) > 2:
                elapsed_time = int(sys.argv[2])

            results[team_name] = [None] * len(problems)

            for line in lines[2:]:
                problem, solve_time, non_ac_count = line.split(' ')
                solve_time = int(solve_time)
                non_ac_count = int(non_ac_count)

                results[team_name][problems.index(problem)] = (solve_time, non_ac_count)

            scores = []

            for name, submissions in results.items():
                solve_count = 0
                penalty = 0

                for i in range(len(problems)):
                    if submissions[i] is not None and submissions[i][0] > elapsed_time:
                        submissions[i] = None

                    if submissions[i] is not None:
                        solve_count += 1
                        penalty += submissions[i][0] + 20 * submissions[i][1]

                scores.append((-solve_count, penalty, name))

            
            scores.sort()

            with open('ranks.txt', 'w', encoding='utf-8') as f:
                f.write(str(elapsed_time)+'\n')

                f.write('-\t-\t'+'\t'.join(problems)+'\tsolve\tpenalty\n')

                rank = 0
                for solve_count, penalty, name in scores:
                    solve_count = -solve_count

                    rank += 1

                    f.write(str(rank)+'\t')

                    f.write(name+'\t')

                    for x in results[name]:
                        if x is None:
                            f.write('-\t')
                        else:
                            f.write(str(x[0])+'('+ str(x[1]) +')\t')
                    
                    f.write(str(solve_count)+'\t' + str(penalty) + '\n')



        
