class DataCollection:
    def __init__(self):
        self.data = {}

        self.request = {}
        self.request["TotalRequest"] = 0
        self.request["NumCompleted"] = 0
        self.request["NumRejected"] = 0
        self.request["WaitingTime"] = []
        self.request["ResponseTime"] = []