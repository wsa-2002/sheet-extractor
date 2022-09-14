import urllib.request
from urllib.request import urlopen, FancyURLopener
from urllib.parse import urlparse, parse_qs, unquote


class UndercoverURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.9 Safari/533.2" # noqa E501


urllib.request._urlopener = UndercoverURLopener()


def youtube_download(video_url: str) -> str:
    video_id = parse_qs(urlparse(video_url).query)['v'][0]

    url_data = urlopen('http://www.youtube.com/get_video_info?&video_id=' + video_id).read() # noqa
    url_info = parse_qs(unquote(url_data.decode('utf-8')))
    token_value = url_info['token'][0]

    download_url = "http://www.youtube.com/get_video?video_id={0}&t={1}&fmt=18".format( # noqa
        video_id, token_value)

    video_title = url_info['title'][0] if 'title' in url_info else ''
    # Unicode filenames are more trouble than they're worth
    filename = video_title.encode('ascii', 'ignore').decode('ascii').replace("/", "-") + '.mp4'

    print("\t Downloading '{}' to '{}'...".format(video_title, filename))

    try:
        download = urlopen(download_url).read()
        with open(filename, 'wb') as file:
            file.write(download)
    except Exception as e:
        raise Exception(e)
    else:
        return filename
