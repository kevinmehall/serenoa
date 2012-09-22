A Python framework for generating and deploying static websites.

Unlike other static site generators (Jekyll, etc.), Serenoa imposes no policy over directory structure or site type. Source directories contain a Python script (`.site`), which has complete control over the transformation to the output directory. You can include another source directory under a specified output URL, for instance a home page that contains subdirectories for multiple projects.

Supported outputs are a local filesystem directory, localhost server for interactive testing, Amazon S3, and SFTP.

Serenoa provides the script files tools for common tasks for manipulating the pages of a static site, and representing the target web site tree in an output-agnostic way. It has built-in support for processing markdown files with [YAML front matter](https://github.com/mojombo/jekyll/wiki/YAML-Front-Matter), and for [Mustache templates](http://mustache.github.com/mustache.5.html). However, the script files have the full power of Python, and you are free to use any other data source or template engine.

### Dependencies

    sudo pip install Markdown pystache PyYAML glob2
    
### Command Usage

    serenoa [-h] [-s PORT] [-l] [-o DIR] [-d DEST] [-n] PATH

    positional arguments:
	  PATH        Path to the root directory of the site

	optional arguments:
	  -h, --help  show this help message and exit
	  -s PORT     Run a server on the specified port
	  -l          List the files in the site
	  -o DIR      Render to output directory DIR
	  -d DEST     Write to a destination defined with a destination() call in the
	              .site file
	  -n          Dry run: When used with -d, print what would happen, but do not modify the remote


### Site Definition

The `.site` file in a site's root directory is a Python script that maps files and other data into pages of the site. See the `examples/` directory.

The following functions are available in `.site` files:

**add(node, path=None)**

Add a node object to the site at a specified URL path. If `path` is not specified, a reasonable default will be provided by the node object, such as the source filename.

**include(path, bind)**

Include another site in the relative filesystem `path`, whose contents will have URLs under the `bind` URL directory.

**destination(name, backend, \*\*kwds)**

Add a destination that can be used to upload the site (`-d name` command line option). Backend is one of `"file"`, `"sftp"`, or `"s3"`. Keyword arguments are passed to the backend. 

**glob(\*paths)**


### Resource Nodes

To be documented

### Destination Backends

To be documented

