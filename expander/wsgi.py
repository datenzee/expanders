import glob
import mimetypes
import tempfile
from os import path, getenv
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from minio import Minio

from expander.doc.expander import DocExpander
from expander.doc.harvester import harvest, download_harvested_files
from expander.vue.expander import VueExpander

load_dotenv()

app = Flask(__name__)

s3_public_url = getenv('S3_PUBLIC_URL')
s3_server = getenv('S3_SERVER')
s3_bucket = getenv('S3_BUCKET')
s3_access_key = getenv('S3_ACCESS_KEY')
s3_secret_key = getenv('S3_SECRET_KEY')


def get_endpoint(url):
    parts = url.split('://', maxsplit=1)
    return parts[0] if len(parts) == 1 else parts[1]


@app.route('/expand', methods=['POST'])
def expand():
    data = request.json
    root_component = data['root_component']
    template_editor_id = data['template_editor_id']
    expander_type = data['expander_type']

    with tempfile.TemporaryDirectory() as tmpdirname:
        if expander_type == 'vue':
            expander = VueExpander(root_component, tmpdirname, input_data=data['content'])
            expander.expand()
            expander.post_expand()
        elif expander_type == 'doc':
            with tempfile.TemporaryDirectory() as tmp_harvested_dir:
                download_harvested_files(tmp_harvested_dir)
                harvested_data = harvest(tmp_harvested_dir)
            expander = DocExpander(root_component, tmpdirname, harvested_data, input_data=data['content'])
            expander.expand()
            expander.post_expand()
        else:
            abort(400, 'Not a valid expander type. Allowed types are: vue, doc')

        client = Minio(
            get_endpoint(s3_server),
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            secure=s3_server.startswith('https://')
        )

        for file in glob.iglob(path.join(tmpdirname, 'dist', '**'), recursive=True):
            if path.isfile(file):
                content_type = get_content_type(file)
                client.fput_object(s3_bucket, f"{template_editor_id}/{Path(file).name}", file,
                                   content_type=content_type)

    response = {'url': f'{s3_public_url}/{s3_bucket}/{template_editor_id}/index.html'}
    return jsonify(response)


def get_content_type(file):
    mt = mimetypes.guess_type(file)
    if mt:
        return mt[0]
    return 'application/octet-stream'
