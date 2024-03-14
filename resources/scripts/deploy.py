import os
import re
import shutil
import subprocess
import sys
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

def exclude_dev_posts(directory_path):
    menuempty=True
    # for every folder
    for root, _, files in os.walk(directory_path):
        # for every file found
        for file_name in files:
            # if its an index.qmd
            if file_name.endswith('index.qmd'):
                # if it's not already a hidden folder and file exists
                file_path = os.path.join(root, file_name)
                if not file_path.replace(directory_path+"/", "").startswith("_") and os.path.exists(file_path):
                        with open(file_path, 'r') as file:
                            qmd_content = file.read()

                        sections = qmd_content.split('---')
                        if len(sections)>1 and "prod: true" not in sections[1]:
                            new_file_path = directory_path+"/_"+file_path.replace(directory_path+"/", "")
                            new_file_path = new_file_path.replace("/"+file_name, "")
                            file_path=file_path.replace("/"+file_name, "")
                            print(file_path,new_file_path)
                            shutil.move(file_path,new_file_path)
                        else:
                            menuempty=False
    if menuempty:
        with open(os.path.join(directory_path, "index.qmd"), 'w') as f:
            f.write("")


def add_prod_prefix(file_path):
    with open("./_quarto.yml", 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Update the YAML content by replacing file paths
    directory, file_name = os.path.split(file_path)
    new_file_path = os.path.join(directory, "prod_"+file_name)
    yaml_content = yaml_content.replace(file_path, new_file_path)

    # Write the modified YAML content back to the file
    with open("./_quarto.yml", 'w') as yaml_file:
        yaml_file.write(yaml_content)

def exclude_dev_parts():
    print("Excluding unready posts")
    exclude_dev_posts('./posts')
    add_prod_prefix("./resources/scripts/add_actionButtons.py")

if len(sys.argv)>1 and sys.argv[1]=="production":
    exclude_dev_parts()

trydeploy()
