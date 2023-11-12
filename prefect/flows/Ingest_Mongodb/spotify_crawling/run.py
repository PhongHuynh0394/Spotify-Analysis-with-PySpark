import subprocess

# Specify the path to the main.py file
command = 'python main.py -s 0 -e 4 -ts 1'

# Run the main.py script
result = subprocess.run(command, shell=True, capture_output=True, text=True)
output = result.stdout
print(output)
