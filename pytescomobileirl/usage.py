import json

class Usage:

    def __init__(self, json_blob):
        self.usages = []
        self.oldest_record = ""
        