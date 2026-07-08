import logging

def logger(name: str):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
