import chevron, os, io, json, shutil

ARTICLE_TEMPLATE_FILE = "templates/article-template.mustache"
ARTICLE_ENTRIES_TEMPLATE_FILE = "templates/article-entries.mustache"
INDEX_TEMPLATE_FILE = "templates/index.mustache"
STYLESHEET = "index.css"
METADATA_FILE_NAME = "metadata.json"
BODY_FILE_NAME = "body.html"
INDEX_HTML_FILE_NAME = "index.html"
COMPONENTS_DIR = "components"
OUTPUT_DIR = "public"
ARTICLES_DIR = "articles"

def read_file(path):
    """Read a file from the specified path and return the data

    Arguments:
        path {string} -- complete file path for file

    Returns:
        string -- data inside the file
    """
    f = io.open(path, mode="r", encoding="utf-8")
    data = f.read()
    f.close()
    return data


def write_file(path, data):
    """Writes specified data to a file. Overwrites existing files

    Arguments:
        path {string} -- path to newly created file
        data {string} -- data to write to file
    """
    f = open(path, "w")
    f.write(data)
    f.close()


def create_dir(path):
    """Creates a directory at the specified path

    Arguments:
        path {string} -- Full path of the directory
    """
    try:
        os.mkdir(path)
    except OSError:
        print ("Failed to create directory {0}".format(path))
        exit()
    else:
        print ("Successfully created the directory: {0}".format(path))


class BlogContentPublisher:
    def __init__(self, current_path, component_dir, article_dir, output_dir):
        self.current_path = current_path
        self.component_dir = component_dir
        self.article_dir = article_dir
        self.output_dir = output_dir

    def render_site(self):
        """The primary entry point of this class. 
        Orchestrates the creation of all the static files to be served

        Creates output directory specified in the output_directory param
        Renders articles from article data gathered in `self.get_articles()`
        and components in `self.get_components()`. 
        Renders index.html with article metadata
        Copies stylesheet over to output directory
        """

        components = self.get_components()
        articles = self.get_articles()

        #Create output directory
        output_dir_path = os.path.join(self.current_path, self.output_dir)
        if os.path.exists(output_dir_path) and os.path.isdir(output_dir_path):
            print("Deleting existing output directory")
            shutil.rmtree(output_dir_path)
        create_dir(self.output_dir)

        #Build article htmls and links
        article_template = read_file(ARTICLE_TEMPLATE_FILE)
        for article in articles:
            article_html = chevron.render(article_template, {**article, **components})
            article_file_path = os.path.join(output_dir_path, article["url"] + ".html")
            write_file(article_file_path, article_html)
            print("wrote article with title {0}".format(article["title"]))

        #Write index.html
        index = chevron.render(read_file(INDEX_TEMPLATE_FILE), {"articles": articles, **components})
        write_file(os.path.join(output_dir_path, INDEX_HTML_FILE_NAME), index)
        #Copy css
        shutil.copyfile(os.path.join(self.current_path, STYLESHEET), os.path.join(output_dir_path, STYLESHEET))
    
    def get_components(self):
        """Reads the web page components from html files defined in the components directory

        Returns:
            dict -- {component_name: component_body}
        """
        components_path = os.path.join(self.current_path, self.component_dir)
        component_files = os.listdir(components_path)
        print("Scanning components dir for files, found: " + str(component_files))
        components = {}
        for component_file_name in component_files:
            path = os.path.join(components_path, component_file_name)
            body = read_file(path)
            name = os.path.splitext(component_file_name)[0]
            components[name] = body 
        return components

    #read in article data
    def get_articles(self):
        """Reads metadata.json and body.html files specified in the articles directory

        Returns:
            dict -- {title: string, body: string, url: string, pub_date: string}
        """
        articles_dir_path = os.path.join(self.current_path, self.article_dir)
        article_dirs = [f.path for f in os.scandir(articles_dir_path) if f.is_dir()]
        print("Scanning components dir for files, found: " + str(article_dirs))
        all_articles = []

        for article_dir in article_dirs:
            metadata_file_path = os.path.join(article_dir, METADATA_FILE_NAME)
            article_body_file_path = os.path.join(article_dir, BODY_FILE_NAME)
            if not os.path.exists(metadata_file_path) or not os.path.exists(article_body_file_path):
                print("Skipped article {0} does not contain appropriate files".format(article_dir))
                continue

            metadata_file = open(metadata_file_path, "r")
            data = json.loads(metadata_file.read())
            metadata_file.close()
            print("Got metadata for article: " + str(data))
            body = read_file(article_body_file_path)
            data["body"] = body
            all_articles.append(data)
        return all_articles


def main():
    b = BlogContentPublisher(os.getcwd(), COMPONENTS_DIR, ARTICLES_DIR, OUTPUT_DIR)
    b.render_site()

main()