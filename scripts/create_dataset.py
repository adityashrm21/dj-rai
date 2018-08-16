import os
import csv
import re
from youtube_dl import YoutubeDL
import logging

SCRIPTS = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(SCRIPTS))
DATASETS = os.path.join(PROJECT_ROOT, 'datasets')
SOURCES = os.path.join(PROJECT_ROOT, 'sources')




SAMPLES = {}



class MyLogger(object):
    def debug(self, msg):
        logging.debug(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)


def my_hook(d):
    if d['status'] == 'finished':
        logging.info('Done downloading, now converting ...')

YOUTUBE_OPTIONS = {
    # 'quiet': True,
    # 'simulate': True,
    # 'format': 'bestaudio/best',
    'forcefilename': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        # 'preferredquality': '192',
    }],
    # 'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


def make_dataset_dir(dataset_name):
    dataset_name = os.path.splitext(source_csv)[0]
    dataset_dir = os.path.join(DATASETS, dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)
    return dataset_dir

def make_dataset_sample_dir(dataset_name, song_title):
    dataset_name = os.path.splitext(source_csv)[0]
    dataset_dir = os.path.join(DATASETS, dataset_name, song_title)
    os.makedirs(dataset_dir, exist_ok=True)
    return dataset_dir

def download_from_csv(source_csv):
    path_tail = os.path.split(source_csv)[1]
    dataset_name = os.path.splitext(path_tail)[0] # kizomba

    og_title_col = "Original Title"
    og_url_col = "Original URL"
    remix_title_col = f"{dataset_name.title()} Title"
    remix_url_col = f"{dataset_name.title()} URL"

    dataset_dir = make_dataset_dir(dataset_name)
    logging.info(f'About to download audio for {dataset_name} dataset to {dataset_dir}')



    with open(source_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:

            song_title = row[og_title_col]
            sample_dir = make_dataset_sample_dir(dataset_name, song_title)

            logging.info(f'Downloading {song_title} to {sample_dir}')
            og_out = os.path.join(dataset_dir, sample_dir, '%(title)s-original.%(ext)s')

            options = {'outtmpl': og_out}
            options.update(YOUTUBE_OPTIONS)
            with YoutubeDL(options) as ydl:
                ydl.download([row[og_url_col]])
                logging.info('completed original download')

            remix_out = os.path.join(dataset_dir, sample_dir, '%(title)s-remix.%(ext)s')
            options = {'outtmpl': remix_out}
            options.update(YOUTUBE_OPTIONS)
            with YoutubeDL(options) as ydl:
                ydl.download([row[remix_url_col]])
                logging.info('completed remix download')



if __name__ == '__main__':
    for source_csv in os.listdir(SOURCES):
        csv_file = os.path.join(SOURCES, source_csv)
        download_from_csv(csv_file)
