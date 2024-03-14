import os
import shutil
import psutil

# Function to add the script tag to an HTML file
def add_script_tag_to_qmd(file_path):
    # if "2023-10-25-create-new-post" in file_path:
        with open(file_path, 'r') as file:
            qmd_content = file.read()

        sections = qmd_content.split('---')

        if len(sections)>1:
            if len(sections)>2 and '```{=html}' in sections[2]:
                # Find the end of the existing HTML block
                end_of_block = sections[2].find('```', sections[2].find('```{=html}') + 1)
                # Remove the existing HTML block
                sections[2] = sections[2][end_of_block + 3:]
                
            script = "\n```{=html}\n<script src=\"../../resources/scripts/prod_actionButtons.js\"></script>\n"

            script= script + "\n```"

            sections[2]=script+sections[2]

            qmd_content = '---'.join(sections)

            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(qmd_content)

# Function to copy chatbot.js to the _site directory
def copy_script_to_site_directory(site_directory,filename):
    script_source_path = './resources/scripts/'+filename
    script_dest_path = os.path.join(site_directory, 'resources', 'scripts', filename)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(script_dest_path), exist_ok=True)

    if os.path.exists(script_source_path):
        shutil.copy(script_source_path, script_dest_path)
    else:
        print(f'{filename} not found at {script_source_path}')

# Function to recursively traverse the directory and add script tags
def add_script_tags_to_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.qmd'):
                qmd_file_path = os.path.join(root, file_name)
                add_script_tag_to_qmd(qmd_file_path)

def is_rendering():
    all_pids = psutil.pids()

    for pid in all_pids:
        try:
            process = psutil.Process(pid)
            if "quarto" in process.cmdline()[1] and process.cmdline()[2]=="render":
                return True
        except:
            pass
    return False

# if is_rendering():
    # add_script_tags_to_directory('./posts')
    # copy_script_to_site_directory('./_site', "prod_actionButtons.js")
