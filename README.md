# pty expect

A minimal [Pexpect](https://pexpect.readthedocs.io/en/stable/) reimplementation.

## Usage Example

```
from pty_expect import run

input_lines = ["Mr Anderson"]

output_lines = run("python3 ex.py", input_lines)
print(output_lines)
```
