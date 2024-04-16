import logging
import logging.config

logging.config.fileConfig('logging.conf')


from hdx_hwa.main import process  # noqa


if __name__ == '__main__':
    process()
