# practice_sim
Simulate a practice team contest

## How To Use
First you need to parse a rank list into a text file containing problem codes and teams with submissions (problem code, time in minutes, non accepted submision count)

    A B C D E F G H I J
    team_a ---- A 20 2
    team_b ---- B 100 0
    ...

For teams with no AC, you can write `team_c ----` only. Currently there is an yandex rank list parser that only works with ranklist copypasted from chrome.

name the submissions file `submissions.txt` and run `prac_sim.py` to simulate contest

- run `prac_sim.py start <name>` to start a virtual contest, a file named `local.txt` will be created with start time and team name
- run `prac_sim.py ac <prob_code> <non_ac_count>` to update local file with your ac submission time
- run `prac_sim.py rank` to generate a html file with snapshot of the virtual at that moment. The html file is created from codemarshal's ui.

## Issues
Due to ranklists generally not showing seconds, the penalty score shown in generated html might differ very little from the actual penalty