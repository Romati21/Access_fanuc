Machine Program Number Refactoring
This Python script is used to refactor the 'ProgNo' field in a DataFrame that contains CNC machine data. The script is specifically designed to handle data from three machines: 'VCENTR-102', 'VTM9', and 'VCENTR-70'.

Classes
Machine: This class represents a CNC machine. Each machine has a name and a program number. The replace_prog method is used to update the 'ProgNo' field of a DataFrame row based on the machine's name and the current program number.
Functions
apply_replace_prog(df, machines): This function applies the replace_prog method of each machine in the provided list to the DataFrame. It returns the updated DataFrame.
Usage
First, create a list of Machine objects for the machines you want to handle:

python
Copy code
machines = [Machine('VCENTR-102'), Machine('VTM9'), Machine('VCENTR-70')]
Then, filter your DataFrame to include only the rows where 'CycleRecord' is True and select the 'MachineName' and 'ProgNo' columns:

python
Copy code
work = fanuc_copy['CycleRecord'] == True
test = fanuc_copy[work].loc[:, ['MachineName', 'ProgNo']].copy()
Next, call the apply_replace_prog function with your DataFrame and the list of machines:

python
Copy code
test = apply_replace_prog(test, machines)
Finally, use the result to update the 'ProgNo' field of the rows in your original DataFrame where 'CycleRecord' is True:

python
Copy code
fanuc_copy.loc[work, 'ProgNo'] = test
