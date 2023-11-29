# Run locally
First, you need to have the repository in your computer:

1. git clone the repository
You can use the http version or the ssh version. 
```
SSH 
git@github.com:IPESE/climact-blog.git
```

    ```
    http method
    git clone https://github.com/IPESE/climact-blog.git
    cd ipese-blog-v2
    ```
#### Setup local environment
2. Make sure you have the following installed:
    * quarto
    * R
    * python (you might also need to run `pip install beautifulsoup4 pandas`)
    * GDAL
3. Run the following to preview the website:
    ```
    quarto preview
    ```
    the first run will install all the R packages necessary and will take a while but everytime you rebuild, the process will be faster

# Deploy
- To deploy to production, simply commit your changes to the main branch
- Make sure you only commit to the main branch if your code works
- If you want to save your work in progress in github, feel free to create a branch with your name

# Other information
### Add edit and pdf button to your post
to add an edit button to a post you can import editButton.js
```
<script src="../../resources/scripts/editButton.js"></script>
```
### Improve build process
- The build process uses a personalized image that has multiple packages and libraries pre-installed to accelarate the process.
    - If the build porcess takes to long because of the installation of new packages, contact the IT service to add new packages to the image


### Write a post
For instructions on how to write a post go to the IT Tutorials menu and there is a post dedicated to creating new posts
Refer to the _template folder to create posts inside the different menus
