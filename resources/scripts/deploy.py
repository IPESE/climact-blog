import os
import re
import shutil
import subprocess
import time

log_file_path = "quarto_logs.log" 
quarto_command = "quarto render > "+log_file_path+" 2>&1"

def trydeploy():
    subprocess.run(quarto_command, shell=True)
    try:
        last_line = None

        # Wait for last_line to be not None
        while last_line is None:
            time.sleep(1)  # Adjust the sleep duration if needed

            with open(log_file_path, "a+") as log_file:
                log_file.seek(0)
                lines = log_file.readlines()
                last_line = next((line.strip() for line in reversed(lines) if line.strip()), None)

        if last_line == "Output created: _site/index.html":
            print("Quarto render successful!")
        else:
            pattern = re.compile(r'\[\d+/\d+\] .+\.qmd')
            error_path = re.sub(r'\[\d+/\d+\]\s*', '', next((line.strip() for line in reversed(lines) if pattern.match(line)), None))

            if error_path:
                error_folder = os.path.dirname(error_path.split(".qmd")[0])
                underscored_path = os.path.join(os.path.dirname(error_folder), "_" + os.path.basename(error_folder))
                shutil.move(error_folder, underscored_path)
                print(f"Error: {error_folder}")
                print("Trying again")
                trydeploy()
            else:
                print("Quarto render failed. Check logs for details.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

trydeploy()
