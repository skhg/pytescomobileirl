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