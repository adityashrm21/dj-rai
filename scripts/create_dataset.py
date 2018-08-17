import os
import csv
import re
from youtube_dl import YoutubeDL


SCRIPTS = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(SCRIPTS))
DATASETS = os.path.join(PROJECT_ROOT, 'datasets')
SOURCES = os.path.join(PROJECT_ROOT, 'sources')


YOUTUBE_OPTIONS = {
    'quiet': True,
    # 'simulate': True,
    'download_archive': os.path.join(DATASETS, 'download_archive'),
    'forcefilename': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        # 'preferredquality': '192',
    }]
}


def make_dataset_dir(dataset_name):
    dataset_name = os.path.splitext(source_csv)[0]
    dataset_dir = os.path.join(DATASETS, dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)
    return dataset_dir

def make_dataset_sample_dir(dataset_name, sample_title):
    dataset_name = os.path.splitext(source_csv)[0]
    dataset_dir = os.path.join(DATASETS, dataset_name, sample_title)
    os.makedirs(dataset_dir, exist_ok=True)
    return dataset_dir

def download_from_csv(source_csv):
    path_tail = os.path.split(source_csv)[1]
    dataset_name = os.path.splitext(path_tail)[0] # kizomba

    dataset_dir = make_dataset_dir(dataset_name)
    print(f'About to download audio for {dataset_name} dataset to {dataset_dir}')

    with open(source_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if '-' not in row:
                download_song(row, dataset_name, remix=False)
                download_song(row, dataset_name, remix=True)
            else:
                print('Skipping row due to missing URL')

def get_yt_options(dataset, sample_name, remix=False):
    if remix:
        outtmpl = os.path.join(dataset, sample_name, '%(title)s-remix.%(ext)s')
    else:
        outtmpl = os.path.join(dataset, sample_name, '%(title)s-original.%(ext)s')

    options = {'outtmpl': outtmpl}
    options.update(YOUTUBE_OPTIONS)
    return options


def download_song(row, dataset, remix):
    if remix:
        url, title = row[0], row[1]
    else:
        url, title = row[2], row[3]

    # use original as dir
    sample_name = make_dataset_sample_dir(dataset, row[3])
    print(f'Downloading {title} to {sample_name}')

    options = get_yt_options(dataset, sample_name, remix=remix)

    with YoutubeDL(options) as ydl:
        ydl.download([url])
        print('completed download')

if __name__ == '__main__':
    for source_csv in os.listdir(SOURCES):
        csv_file = os.path.join(SOURCES, source_csv)
        download_from_csv(csv_file)
