#! /usr/bin/env python
#-*- coding:utf-8 -*-

import sys

import urllib
import urllib2

from HTMLParser import HTMLParser

class RADEXHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_tr = 0

        self.lines = []
        self._l_count = 0

    def feed(self, html):
        HTMLParser.feed(self,html.replace("&nbsp;", " "))

    def handle_starttag(self, tag, attrs):
        if(tag == "tr"):
            self.in_tr += 1
            self._l_count = 0

    def handle_endtag(self, tag):
        if(tag == "tr"):
            self.in_tr -=1

    def handle_data(self, data):

        if self.in_tr == 2:
            i = len(self.lines)

            if self._l_count == 0:
                self.lines.append([])
                self.lines[i].append(data)

            if self._l_count != 0:
                self.lines[i-1].append(data)

            self._l_count += 1

class RADEXMoleculeParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_sel = False
        self.tmp_val = ""

        self.molecules = []

    def handle_starttag(self, tag, attrs):
        if(tag == "select" and attrs==[("name", "molfile")]):
            self.in_sel = True

        if self.in_sel:
            if(tag == "option"):
                self.tmp_val = attrs[0][1]

    def handle_endtag(self, tag):
        if(tag == "select"):
            self.in_sel = False

    def handle_data(self, data):
        if self.in_sel:
            self.molecules.append((data.strip(), self.tmp_val))


class RADEX:

    def __init__(self):
        self.base_url = "http://www.sron.rug.nl/~vdtak/radex/radex.php"

    def getMolecule(self):
        req = urllib2.Request(self.base_url)
        response = urllib2.urlopen(req)
        html = response.read()

        parser = RADEXMoleculeParser()
        parser.feed(html)

        return parser.molecules[1:]

    def _getHTML(self, molfile, fmin, fmax, tbg, tkin, nh2, cold, dv):
        values = { 
                "action" : "derive",
                "molfile" : str(molfile),
                "fmin" : str(fmin),
                "fmax" : str(fmax),
                "tbg" : str(tbg),
                "tkin" : str(tkin),
                "nh2" : str(nh2).replace("+",""),
                "cold" : str(cold).replace("+",""),
                "dv" : str(dv)
                }

        q = urllib.urlencode(values)
        req = urllib2.Request(self.base_url, q)
        response = urllib2.urlopen(req)

        return response.read()

    def get(self, molfile, fmin, fmax, tbg, tkin, nh2, cold, dv):
        html = self._getHTML(molfile, fmin, fmax, tbg, tkin, nh2, cold, dv)
        #sys.stderr.write("got response from radex.\n")
        #html = open("dummy.html").read()

        parser = RADEXHTMLParser()
        parser.feed(html)

        return parser.lines[:-1]


if __name__ == "__main__":

    if sys.argv[1] == "list":
        ret = RADEX().getMolecule()
        print "Mol\tKey"
        print "----------------"
        for key, val in ret:
            print key + "\t" + val
        sys.exit()


    if len(sys.argv) != 9:
        print "syntax error.\tradex.py mol fmix fmax t_bg t_k h2 column_d dv"
        print "  example:\tradex.py 13co 50 500 2.73 30 134 1e14 1.0"
        sys.exit()


    tmp = sys.argv
    ret = RADEX().get(tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8])

    print "Transition\tFrequency[GHz]\tT_ex[K]\ttau      \tT_r[K]"
    for l in ret:
        for v in l:
            print v+"\t",
        print


