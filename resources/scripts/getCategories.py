# Import this script in the post-render of the _quarto.yml to get all the categories in the blog and add them in the divs of class categories-list
from bs4 import BeautifulSoup
import os

def process_html_file(file_path, data_categories):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all div elements with class "categories-list"
        divs = soup.find_all('div', class_='categories-list')
        
        for div in divs:
            # Create a new list element and add it to the div
            ul = soup.new_tag('ul')
            for item in data_categories:
                li = soup.new_tag('li')
                li.string = item
                ul.append(li)
            div.append(ul)
        
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(str(soup))

def get_categories_list(site_directory): 
    # Iterate through HTML files in the directory
    for filename in os.listdir(site_directory):
        if filename.endswith(".html"):
            with open(os.path.join(site_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all div elements with the specified class
                divs = soup.find_all('div', class_='quarto-listing-category category-default')

                for wrapper in divs:
                    for div in wrapper:
                        if div['data-category'] != "":
                            data_categories.append(div['data-category'])

    unique_set = set(data_categories)
    return sorted(list(unique_set))


site_directory = os.path.join(os.getcwd(), "_site")
data_categories = []
data_categories=get_categories_list(site_directory)
# Recursively process HTML files in the directory and its subdirectories
for root, dirs, files in os.walk(site_directory):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            process_html_file(file_path, data_categories)





