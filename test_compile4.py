import subprocess
result = subprocess.run(["gradle", "assembleDebug"], capture_output=True, text=True)
if result.returncode != 0:
    print("Error compiling")
    print(result.stdout)
    print(result.stderr)
else:
    print("Compiled successfully")
