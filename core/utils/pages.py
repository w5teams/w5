#!/usr/bin/env python
# encoding:utf-8

class Page(object):
    def __init__(self, model):
        self.model = model

    def to(self):
        return {
            "page": self.model.current_page,
            "page_count": self.model.per_page,
            "total_page": self.model.last_page,
            "total_count": self.model.total,
            "list": self.model.serialize()
        }
