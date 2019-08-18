import os
import csv

csvpath = os.path.join('03-Python_Homework_Instructions_PyBank_Resources_budget_data.csv')


PL = []

change = []



with open(csvpath, newline='') as csvfile:
    
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)  
    months = sum(1 for row in csvreader)
    print(f'Financial Analysis')
    print('---------------------------------------')
    print(f"Total Months: " + str(months))
    
    csvfile.seek(0) 
    next(csvreader)               
    csvreader = list(csvreader)  
    count = len(csvreader)        
    print(f'Total Months.. list count method: '+ str(count)+'. I had tp prove to myself that I could do it this way too...')

    total = round(sum(int(row[1]) for row in csvreader),0)
    print(f'Total profits/loss = $' + str(total))



for i in range(0 , len(csvreader)):
 
    
    PL.append(float(csvreader[i][1]))
  


for i in range(1,len(csvreader)):
    change.append((PL[i]-PL[i-1]))
    max_change = int(max(change))
    min_change = int(min(change))
    maxindex = change.index(max_change)+1
    minindex = change.index(min_change)+1

TTLchange = sum(change)

AVG_CHANGE = round(TTLchange/(len(csvreader)-1),2)
print('AVG CHANGE = $' + str(AVG_CHANGE))

print("Greatest Increase ['Month', 'Profit'] & Change in profit from previous month: " + str(csvreader[maxindex]) + ' $' + str(max_change))
print("Greatest Decrease ['Month', 'Profit'] & Change in profit from previous month: " + str(csvreader[minindex]) + ' $' + str(min_change))
print('I included all 3 data points because it was diffidult to get only the month from the csvreader list and then reference the index to bring the max/min change from that month...  \nI had already found the max/min and was able to use that index to pull month and total profit/loss from the original csvreader...   Thank you for the help.')

bashCommand = "python main.py > output/myfile.txt"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()