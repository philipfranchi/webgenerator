# Phil's website script
I use this script for generating the web pages on my website, and decided to put it on github for future reference in case I forget. 

These are the things it's expecting

    .
    ├── articles
    │   ├── article-name
    │   │   ├── body.html
    │   │   └── metadata.json
    ├── components
    │   └── component-name.html
    ├── index.css
    └── templates
        ├── article-template.mustache
        └── index.mustache

The script first scans the components directory for all the parts of the web page it'll be sticking into the mustache templates, and then it scans the article directory for the actual data of the articles it will generate.

Every time you run the script, `it deletes the output directory` so make sure there's nothing you want in there.