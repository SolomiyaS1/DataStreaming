import pandas as pd
from DataStreaming.utils import load_config, create_logger

logger = create_logger(__name__)


class SourceDataHandler(object):

    def __init__(self):
        config = load_config()
        self.start = 0
        self.end = 0
        self.messages_num = 1
        self.data = pd.read_csv(config["file_path"], sep='\t')

    def prepare_dataset(self):
        self.data = self.data[["Tweet"]]
        self.data["Id"] = [i for i in range(1, len(self.data) + 1)]

    def get_next_message(self):
        self.start = self.end + 1
        self.end += self.messages_num
        filtered_df = self.data.loc[(self.start <= self.data.Id) & (self.data.Id <= self.end)]
        message = filtered_df["Tweet"].astype(str)
        return message
