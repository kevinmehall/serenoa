A Python framework for generating and deploying static websites.

Unlike other static site generators (Jekyll, etc.), Serenoa imposes no policy over directory structure or site type. Source directories contain a python script (.site), which has complete control over the transformation to the output directory. You can include another source directory under a specified output URL, for instance a home page that contains subdirectories for multiple projects.

Supported outputs are a local filesystem directory, localhost server for interactive testing, Amazon S3*, and SFTP*. (* = not yet implemented).

Serenoa provides the script files tools for common tasks for manipulating the pages of a static site, and representing the target web site tree in an output-agnostic way. It has built-in support for processing markdown files with YAML front matter, and for Mustache templates. However, the script files have the full power of Python, and you are free to use any other data source or template engine.

### Dependencies

    sudo pip install Markdown pystache PyYAML