import os
import shutil
import subprocess
from glob import glob
from pprint import pprint


def download_harvested_files(tmp_harvested_dir, dt_template_id="datenzee:horizon-europe-expanded-template:1.0.0"):
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'project-templates', 'doc', 'document_template')
    shutil.copytree(template_dir, tmp_harvested_dir, dirs_exist_ok=True)
    subprocess.check_call(f'dsw-tdk get {dt_template_id}', shell=True,
                          cwd=tmp_harvested_dir)


def harvest(harvest_dir, dt_template_id="datenzee:horizon-europe-expanded-template:1.0.0"):
    harvested_data = {}
    files = get_files(harvest_dir)
    parts_to_remove = [
        harvest_dir,
        '/src/components/gen/', '.html.jinja2',
        f'/{dt_template_id.replace(":", "_")}'
    ]
    for file in files:
        component = file
        for part_to_remove in parts_to_remove:
            component = component.replace(part_to_remove, '')
        before = extract_content(file, "before")
        if is_not_empty(before):
            harvested_data[component + "_before"] = before
        after = extract_content(file, "after")
        if is_not_empty(after):
            harvested_data[component + "_after"] = after
    print(" *** Harvested data (start) ***")
    pprint(harvested_data)
    print(" *** Harvested data (end) ***")
    return harvested_data


def is_not_empty(value):
    return value is not None and value != 'None' and value != [] and value != [''] and value != ''


def get_files(harvest_dir):
    skip_files = [
        'Heading.html.jinja2',
        'IterativeContainer.html.jinja2',
        'Rdf.html.jinja2',
    ]

    files = []
    pattern = "*.html.jinja2"
    for dir, _, _ in os.walk(harvest_dir):
        files.extend(glob(os.path.join(dir, pattern)))

    return list(filter(lambda f: f not in skip_files, files))


def extract_content(filename, stage):
    with open(filename, 'r') as file:
        data = file.read()

    # Define the start and end markers
    start_marker = "{#  Customization (" + stage + "): start  #}"
    end_marker = "{#  Customization (" + stage + "): end  #}"

    # Find all content between the markers
    start = 0
    while True:
        start = data.find(start_marker, start)
        if start == -1:
            break
        start += len(start_marker)
        end = data.find(end_marker, start)
        if end == -1:
            break
        return data[start:end].strip()
