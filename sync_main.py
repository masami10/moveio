import yaml
from app import docker_huey
from huey import crontab
from tasks import create_sync_blue_print, sync_image

import logging.config
logging.config.fileConfig('logger.ini')
LOG = logging.getLogger('logger01')


with open('image_list.yml', 'rt') as f:
    image_list = yaml.load(f)


@docker_huey.periodic_task(crontab(hour='*/24'))
def sync_all_images():
    for image_name in image_list['images']:
        try:
            blue_print = create_sync_blue_print(image_name)
            sync_image(blue_print)
        except Exception as e:
            LOG.error(e)

sync_all_images()

