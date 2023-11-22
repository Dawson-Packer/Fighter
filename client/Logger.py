import os as os

class Logger:
    """
    A simple CSV Logger which logs on a line-by-line basis.
    """
    def __init__(self, headers: list):
        data_entries = ", ".join(headers)
        data_entries = data_entries + '\n'
        if os.path.exists("client/log.csv"):
            os.remove("client/log.csv")
        self.log_file = open("client/log.csv", 'w')
        self.log_file.write(data_entries)
        self.log_file.flush()

    def enter_data(self, data: list):
        """
        Enters data into a single line of the output log.
        
        :param data: A list of entries to add. Does not have to be the same number of entries as
                     headers on initial creation.
        """
        if len(data) > 1:
            for index, entry in enumerate(data):
                data[index] = str(entry)
            data_entries = ", ".join(data)
        else:
            data_entries = str(data[0])
        data_entries = data_entries + '\n'
        self.log_file.write(data_entries)
        self.log_file.flush()

    def terminate(self):
        self.enter_data(["------END OF FILE------"])
        self.log_file.close()