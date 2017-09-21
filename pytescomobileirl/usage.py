#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from . import UsageRecord

class Usage:

    def __init__(self, json_blob):
        original_records = json.loads(json_blob)["usageHistory"]

        self.records = [UsageRecord(rec) for rec in original_records ]

    def size(self):
        return len(self.records)

    def filter_by_type(self, svc_type = None):
        for rec in self.records:
            if svc_type is None or (svc_type.lower() in rec.use_type.lower()):
                yield rec

    def data(self):
        return self.filter_by_type("data")

    def text(self):
        return self.filter_by_type("text")

    def voice(self):
        return self.filter_by_type("call")