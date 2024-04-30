import os
import shutil
import psutil

# Function to add the script tag to an HTML file
def remove_script_tag_to_qmd(file_path):
    # if "2023-10-25-create-new-post" in file_path:
        with open(file_path, 'r') as file:
            qmd_content = file.read()

        sections = qmd_content.split('---')

        if len(sections)>1:
            if len(sections)>2 and '<script src="../../resources/scripts/actionButtons.js"></script>' in sections[2]:
                # Find the end of the existing HTML block
                end_of_block = sections[2].find('```', sections[2].find('```{=html}') + 1)
                # Remove the existing HTML block
                sections[2] = sections[2][end_of_block + 3:]
                
            qmd_content = '---'.join(sections)

            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(qmd_content)

# Function to recursively traverse the directory and add script tags
def remove_script_tags_to_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name == 'index.qmd':
                qmd_file_path = os.path.join(root, file_name)
                print(qmd_file_path)
                if "_template" not in qmd_file_path:
                    if os.path.getsize(qmd_file_path) == 0:
                        os.remove(qmd_file_path)
                    else:
                        remove_script_tag_to_qmd(qmd_file_path)

def add_prod_prefix(prod,dev):
    with open("./_quarto.yml", 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Update the YAML content by replacing file paths
    yaml_content = yaml_content.replace(prod, dev)

    # Write the modified YAML content back to the file
    with open("./_quarto.yml", 'w') as yaml_file:
        yaml_file.write(yaml_content)

def is_rendering():
    all_pids = psutil.pids()

    for pid in all_pids:
        try:
            process = psutil.Process(pid)
            if "quarto" in process.cmdline()[1] and "render" in process.cmdline():
                return True
        except:
            pass
    return False

if is_rendering():
    print("removing edit buttons")
    remove_script_tags_to_directory('./posts')
    add_prod_prefix("prod_add_actionButtons","add_actionButtons")