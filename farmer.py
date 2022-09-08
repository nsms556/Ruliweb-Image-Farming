import sys
import urllib.request as request

from bs4 import BeautifulSoup

def get_img_src(img_tags) :
    return list(map(lambda x : x['src'], img_tags))

def convert_orginal_size_url(img_urls) :
    return list(map(lambda x : x.replace('img', 'ori'), img_urls))

def convert_video_to_gif(vid_urls) :
    return list(map(lambda x : x.replace('mp4?', ''), vid_urls))

def is_gif_webp(img_url) :
    gif = img_url[-7:]
    webp = img_url[-8:]

    if gif == 'mp4?gif' or webp == 'mp4?webp' :
        return True

    return False

def get_vid_src(gif_tags) :
    srcs = list(map(lambda x : x['src'], gif_tags))
    srcs = [x for x in srcs if is_gif_webp(x)]

    return convert_video_to_gif(srcs)
    
def parsing_image_urls(read_url, original_size) :
    req = request.Request(read_url)
    res = request.urlopen(req).read()

    original_doc = BeautifulSoup(res, 'html.parser')
    main_view = original_doc.find('div', class_='board_main_view')
    img_urls = get_img_src(main_view.find_all('img'))
    gif_urls = get_vid_src(main_view.find_all('video'))

    if original_size :
        return convert_orginal_size_url(img_urls) + gif_urls
    
    return img_urls + gif_urls

def download_image(url, folder) :
    file_name = url.split('/')[-1]
    target_dir = '{}/{}'.format(folder, file_name)

    request.urlretrieve(url, target_dir)

def download_images(img_urls, folder) :
    for url in img_urls :
        file_name = url.split('/')[-1]
        target_dir = '{}/{}'.format(folder, file_name)

        request.urlretrieve(url, target_dir)

def run(url, target_folder, original_size=True) :
    img_urls = parsing_image_urls(url, original_size)

    download_images(img_urls, target_folder)

if __name__ == '__main__' :
    args = len(sys.argv)

    url = sys.argv[1]
    target = './'

    if args > 1 :
        target = sys.argv[2]

    run(url, target)