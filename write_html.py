import ebooklib
from ebooklib import epub
import sys
import os
from distutils.dir_util import copy_tree
from PIL import Image
from io import BytesIO


def write_html_file(book, folder):
    """
    This function will remove the value attribute from the given epub
    Params:
    book : book name (mandatory)
    """
    try:
        book_data = epub.read_epub(book)
        html_list = []
        
        #getting the table of contents
        toc = book_data.toc
        
        #Copying the template for customize with ebook content
        if not os.path.isdir(os.path.join(os.getcwd(), folder)):
            from_dir = os.path.join(os.getcwd(), "Template01")
            to_dir = os.path.join(os.getcwd(), folder)
            try:
                copy_tree(from_dir, to_dir)
            except:
                print("Error copying the template")
                return
                
        #Saving all the book contents including images
        for item in book_data.get_items():
            file_name = item.file_name
            file_name_parts = file_name.split("/")
            if file_name_parts[0] == 'text':
                with open(os.path.join(os.getcwd(), folder, "www", file_name_parts[1]), "w") as f:
                    f.write(item.content.decode("utf-8"))
            if file_name_parts[0] == 'media':
                im = Image.open(BytesIO(item.content))
                im.save(os.path.join(os.getcwd(), folder, file_name))
        with open(os.path.join(os.getcwd(), folder, "www", "index.html")) as idx:
            index_content = idx.read()         
        with open(os.path.join(os.getcwd(), folder, "www", "index.html"), "w") as idx:
            side_panel = '<ul class="list-unstyled components mb-5">\n{title_links}</ul>\n'
            title_links = ""
            for t in toc:
                if type(t) is tuple:
                    print(type(t))
                    section_links = ''
                    section = t[0]
                    section_list = t[1]
                    section_href = section.href
                    section_href = section_href.split("/")[1]
                    section_id = section_href.split(".")[0]
                    section_title = section.title
                    print(section_title)
                    a = '<li><a href="#{section_id}" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">{section_title}</a>'.format(section_id=section_id, section_title=section_title)
                    section_links += a + '<ul class="collapse list-unstyled" id="{section_id}">\n'.format(section_id=section_id)
                    for s in section_list:
                        shref = s.href
                        shref = shref.split("/")[1]
                        stitle = s.title
                        print(stitle)
                        section_links += '''<li>
                            <a href="#" onclick="changeContent('{href}')">{link_title}</a>
                        </li>'''.format(href=shref, link_title=stitle)
                    section_links += "</ul>\n</li>"
                    print(section_links)
                    title_links += section_links
                    continue
                href = t.href
                href = href.split("/")[1]
                title = t.title
                title = '''<li>
                            <a href="#" onclick="changeContent('{href}')">{link_title}</a>
                        </li>'''.format(href=href, link_title=title)
                title_links += title+"\n"
            index_content = index_content.replace("{{{toc}}}", side_panel.format(title_links=title_links))
            index_content = index_content.replace("{{{title}}}", book_data.title)
            idx.write(index_content)
        print("done..")
    except:
        print("Unknown error occured")
        print(traceback.format_exc())
        
        
#getting file name
book = sys.argv[1]

#getting the folder name on which the html should get in
folder_name = sys.argv[2]

#function to read and remove the value attribute
write_html_file(book, folder_name)
