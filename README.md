#### Examples using py-executable-checklist framework

###### Setting up python3 and dependencies with VirtualEnv

```
 make setup
```

### Scripts

<!-- START makefile-doc -->
[_hn_links.py_](https://namuan.github.io/bin-utils/hn_links.html)
```
usage: hn_links.py [-h] -l HN_LINK -b BLOG_DIRECTORY [-v]

Grab links from HN Post and generate Markdown post with image thumbnails
It also creates a Hugo blog post from Markdown and images generated

SUPPORT: To regenerate thumbnail, just delete the image file under thumbnails folder inside the post directory.
SUPPORT: To remove any link from the blog post, delete the entry after the post is created **in the blog directory**
Note down all the links somewhere then run the following command from blog directory to delete them
E.g. Image links will be like

![](/images/2021/12/21/httpsunixstackexchangecoma88682.png)
![](/images/2021/12/21/httpscleaveapp.png)

$ pbpaste | awk -F\/ '{print $6}' | tr -d ')' | while read img; do find . -name $img -delete; done # noqa: W605

Usage:
$ python hn-links.py -l https://news.ycombinator.com/item?id=25381191 -b <blog_directory> --open-in-editor

options:
  -h, --help            show this help message and exit
  -l HN_LINK, --hn-link HN_LINK
                        Link to HN Post
  -b BLOG_DIRECTORY, --blog-directory BLOG_DIRECTORY
                        Full path to blog directory
  -v, --verbose         Display context variables at each step

```
[_listen_to.py_](https://namuan.github.io/bin-utils/listen_to.html)
```
usage: listen_to.py [-h] [-p ROOT_PATH] [-v]

Downloads music from r/listentothis and saves them to a folder

options:
  -h, --help            show this help message and exit
  -p ROOT_PATH, --root-path ROOT_PATH
                        Path to the directory where the file will be created
  -v, --verbose         Increase verbosity of logging output

```
[_links_to_hugo.py_](https://namuan.github.io/bin-utils/links_to_hugo.html)
```
usage: links_to_hugo.py [-h] -l LINKS_FILE -t POST_TITLE -b BLOG_DIRECTORY
                        [-e] [-v]

Read a list of links from a file (Each line should contain a single link to a webpage)
Check if the link is still valid
Grab title of the webpage
Grab screenshot/thumbnail of the webpage
Create a blog post with list of links along with the thumbnail

Usage:
$ python3 links_to_hugo.py -l links.txt -t "<blog title>" -b <blog_directory> --open-in-editor

Process:
1. Use curl to download the webpage
$ curl -s <page-url> > .temp/<filename>.html

2. Use pup to extract links and output to a file
$ cat <filename>.html | pup 'a attr{href}' >> links.txt

3. Run this script
$ EDITOR=/usr/local/bin/idea ./links_to_hugo.py --links-file .temp/links.txt --post-title "Post title"     --blog-directory "<full-path-to-blog-directory"  --open-in-editor

4. Review blog post in the editor and remove any links if necessary

5. Run this script to clean up any images that are left behind due to deleted links
$ ./unused_files.py -s <blog-root>/static/images -t <blog-root>/content -d

6. make deploy from blog directory
7. make commit-all from blog directory

options:
  -h, --help            show this help message and exit
  -l LINKS_FILE, --links-file LINKS_FILE
                        Path to links file
  -t POST_TITLE, --post-title POST_TITLE
                        Blog post title
  -b BLOG_DIRECTORY, --blog-directory BLOG_DIRECTORY
                        Full path to blog directory
  -e, --open-in-editor  Open blog site in editor
  -v, --verbose         Display context variables at each step

```
[_publish_vnote_to_hugo.py_](https://namuan.github.io/bin-utils/publish_vnote_to_hugo.html)
```
usage: publish_vnote_to_hugo.py [-h] [-b BLOG_DIRECTORY] -n VNOTE_FILE_PATH
                                [-e]

Publish vNote to Hugo blog post
$ python publish_vnote_to_hugo.py <<blog-root>> <<vnote-location>>

options:
  -h, --help            show this help message and exit
  -b BLOG_DIRECTORY, --blog-directory BLOG_DIRECTORY
                        Blog directory
  -n VNOTE_FILE_PATH, --vnote-file-path VNOTE_FILE_PATH
                        vNote file path
  -e, --open-in-editor  Open blog site in editor

```
[_hn-vader-sentiment.py_](https://namuan.github.io/bin-utils/hn-vader-sentiment.html)
```
usage: hn-vader-sentiment.py [-h] -s STORY_ID [-v]

Analyse a HackerNews post by looking at the comments and calculating the sentiment

options:
  -h, --help            show this help message and exit
  -s STORY_ID, --story-id STORY_ID
                        Hacker News Story ID
  -v, --verbose         Display context variables at each step

```
[_phpbb_thread.py_](https://namuan.github.io/bin-utils/phpbb_thread.html)
```

```
<!-- END makefile-doc -->

## License

[MIT](https://choosealicense.com/licenses/mit/)
