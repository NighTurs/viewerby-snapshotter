# Viewer.BY Snapshotter

Viewer.by is Belarusian service to manage IP cameras. Some clients like
street cameras, hockey arenas open their cameras to public with this
service. On site one is able to get new camera snapshots each minute.
You can also view historical snapshots, but only on hour basis. Purpose
of this application is to get and aggregate minute snapshots for clients
of interest.

## Requirements

* Python 3
* Virtualenv

## Setup

Create virtual environment called env in root application folder,
something like 'virtualenv -p python3 env'. Then source it
'source env/bin/activate', and install requirements
'pip install -r requirements.txt'. Then you are ready to run it by
launching [run.sh](run.sh). You can specify list of clients by altering
[run.sh](run.sh) chunk --clients {client_id} {client_id}

## How to get client id?

When opening some camera view on Viewer.by in address bar you can see
something like https://viewer.by/view?obj=117. 117 here is client id.

