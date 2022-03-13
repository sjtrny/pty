from pty_expect import run

input_lines = ["Mr Anderson"]

output_lines = run("python3 ex.py", input_lines)
print(output_lines)
