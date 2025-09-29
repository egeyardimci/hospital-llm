import logging

def get_logger():
    logger = logging.getLogger('hospital_llm')
    logger.setLevel(logging.DEBUG)

    # Only add handler if it doesn't exist (prevents duplicates)
    if not logger.handlers:
        handler = logging.StreamHandler()  # Just console for now
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%H:%M:%S'
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

