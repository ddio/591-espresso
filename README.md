# 591 Espresso

One time 591 crawler that keep flexibility and peace in mind.

Major features:

1. Crawl any rental list, including 住家、店面、辦公.
2. Accept incomplete data, such as 404 not found.
3. Aggregate all results and export union of attributes.
4. Crawl target website with politeness, at most 1 request/sec.

This crawler is NOT designed for:

1. Parallel execution or anything related to efficiency
2. Aggregate data across multiple time period

## System Requirement

1. Docker environment - [Docker 18+](https://docs.docker.com/install/) and [docker-compose 1.18.0+](https://docs.docker.com/compose/install/)

## Setup

Build development image and update python package

```bash
docker-compose build espresso
```

## Execution

This tool provide a simple CLI `manage.py`, which support:

1. `list` - list all existing crawler job
2. `crawl` - create a new crawler job
3. `resume` - resume a previously stopped job
4. `delete` - delete specified job and its data
5. `export` - export data in specified job

For detail usage, please see help message:

```bash
docker-compose run expresso python manage.py -h
```

### Create One Time Crawler

```bash
docker-compose run espresso python manage.py crawl 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1'
```
