start_time = JSON.parse([START])
problems = JSON.parse([PROBLEMS])
results = JSON.parse([RESULTS])

counts = []
scores = []
for(var i = 0; i<problems.length; i++){
    counts.push(0)
}

cur_time = Date.now()/1000

var remaining
if (cur_time - start_time > 5 * 60 * 60) {
    remaining = "Finished"
}
else{
    elapsed_time = cur_time - start_time
    hours = Math.floor((5 * 60 * 60 - elapsed_time)/60/60)
    minutes = Math.floor((5 * 60 * 60 - elapsed_time)/60)  % 60
    seconds = Math.floor((5 * 60 * 60 - elapsed_time))  % 60
    remaining = `Remaining: ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`
}

elapsed_time = (cur_time - start_time)/60

for(var team in results){
    var solve_count = 0
    var penalty = 0

    for(var i = 0; i<results[team].length; i++){
        if(results[team][i] !== null &&  results[team][i][0] > elapsed_time)
            results[team][i] = null

        if(results[team][i] !== null){
            solve_count += 1
            penalty += results[team][i][0] + 20 * results[team][i][1]
            counts[i]++
        }
    }

    scores.push([solve_count, penalty, team])
}

scores = scores.sort((a, b) => {
    if(a[0] == b[0])
        return a[1] - b[1]
    else
        return b[0] - a[0]
})


function pad(x){
    y = x.toString()
    if (y.length < 2)
        return '0' + y
    else
        return y
}

function update(){
    document.querySelector('.h3').innerText = remaining

    table = document.querySelector('.table-standings')

    problem_row = table.children.item(0).children.item(0)
    problems.forEach((x) => {
        problem_row.innerHTML += `<th style="width: 24px;"><a href="">${x}</a></th>`
    })

    count_row = table.children.item(0).children.item(1)
    counts.forEach((x) => {
        count_row.innerHTML += `<th class="text-center">${x}</th>`
    })

    ranks = table.children.item(1)

    content = ''
    for(var i = 0 ; i<scores.length; i++){
        row_head = `<td>${i+1}</td><td><a href="">${scores[i][2]}</td><td><a href=""><div class="label label-info">${scores[i][0]}</div><div class="label label-default">${scores[i][1]}</div></a><td style="width: 24px;"></td></td>`
        row_tail = ''
        team = scores[i][2]

        for(var j = 0; j<results[team].length; j++){
            if(results[team][j] === null){
                row_tail += `<td><a href=""></a></td>`
            }
            else{
                row_tail += `<td><a href=""><div class="label label-success">&nbsp;</div><div class="label label-default">${results[team][j][1]+1} (${results[team][j][0]})</div></a></td>`
            }
        }

        content += `<tr data-id="undefined">${row_head}${row_tail}</tr>`
    }

    ranks.innerHTML += content
}