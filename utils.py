import logging
import os
import coloredlogs
import yaml

COLOREDLOGS_FIELD_STYLES = coloredlogs.DEFAULT_FIELD_STYLES
COLOREDLOGS_FIELD_STYLES.update(
    {
        "asctime": {"color": "green"},
        "filename": {"color": "green"},
        "fileno": {"color": "green"},
    }
)


def create_logger(
        name: str,
        msg_format: str = "",
) -> logging.Logger:
    msg_format = msg_format or "%(asctime)s %(hostname)s %(name)s %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
    logger = logging.Logger(name)
    console_handler = logging.StreamHandler()
    level = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    coloredlogs.install(
        level=level,
        logger=logger,
        field_styles=COLOREDLOGS_FIELD_STYLES,
        fmt=msg_format,
    )

    return logger


def get_relative_path(path: str, rel_to: str) -> str:
    return os.path.join(os.path.dirname(rel_to), path)


def load_yaml(path: str):
    with open(path) as fd:
        config = yaml.load(fd, yaml.FullLoader)
        config["yaml_path"] = path
        return config


def load_config():
    return load_yaml(get_relative_path("config.yaml", __file__))
