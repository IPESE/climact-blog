const categories = document.getElementsByClassName('quarto-title-meta')[0].innerHTML;

const currentUrl = window.location.href;

// for pdf url
// Get the current URL
let pdfUrl = ""

if (currentUrl.endsWith('/')) {
    pdfUrl = currentUrl+'index.pdf';
} else if (currentUrl.endsWith('.html')) {
    pdfUrl = currentUrl.replace('.html', '.pdf');
}

let newDomain = "https://github.com/IPESE/climact-blog/edit/main/";

if (!currentUrl.includes("climact-blog")) {
  console.log("adding the ipese-blog")
  newDomain += "climact-blog";
}

let modifiedUrl = currentUrl.replace(/^https?:\/\/[^/]+/, newDomain);

if (modifiedUrl.endsWith(".html")) {
  modifiedUrl = modifiedUrl.replace(/\.html$/, ".qmd");
} else {
  modifiedUrl = modifiedUrl + "index.qmd";
}

document.getElementsByClassName('quarto-title-meta')[0].innerHTML =
  categories + `
  <div style="display:flex;justify-content: space-between;">
    <a href=${modifiedUrl} target="_blank" id="edit-button" class="action-button">Edit</a>
    <a href=${pdfUrl} target="_blank" id="pdf-button" class="action-button"><i class="bi bi-file-pdf-fill" role="img"></i></a>
  </div>
  `;