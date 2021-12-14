#!/usr/bin/env python
# encoding:utf-8

class Version(object):
    @staticmethod
    def compare(a, b):
        la = a.split('.')
        lb = b.split('.')

        if len(la) > len(lb):
            f = len(la)
        else:
            f = len(lb)

        for i in range(f):
            try:
                if int(la[i]) > int(lb[i]):
                    return ">"
                elif int(la[i]) == int(lb[i]):
                    continue
                else:
                    return "<"
            except IndexError as e:
                if len(la) > len(lb):
                    return ">"
                else:
                    return "<"
        return "="
