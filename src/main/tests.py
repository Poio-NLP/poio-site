# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import unittest
import main
import os
import sqlite3

class MainTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up the app"""
        self.app = main.app.test_client()

    def test_main(self):
        """Test rendered index page."""
        rv = self.app.get('/')
        assert 'Language Diversity' in rv.data

    def test_get_semantic_map(self):
        """Test get_semantic_map."""
        rv = self.app.get('/api/semantics?iso=bar&term=brezn')
        assert 'fettn' in rv.data
        assert 'brezn' in rv.data

    def test_prediction(self):
        """Test prediction.""" 
        rv = self.app.get('/api/prediction?iso=bar&text=De')
        assert 'Des' in rv.data

    def test_languages(self):
        """Test supported languages.""" 
        rv = self.app.get('/api/languages')
        assert 'bar' in rv.data

    def test_corpus(self):
        """Test corpus files.""" 
        rv = self.app.get('/api/corpus?iso=bar')
        assert 'barwiki.zip' in rv.data

    def test_api_limits(self):
        """Test API request limits"""
        dic = {"languages":1000, "corpus":1000, "prediction":10000, "semantics":100}

        con = sqlite3.connect(os.path.abspath(os.path.join(main.app.static_folder, "limits.sqlite")), check_same_thread=False)
        cur = con.cursor()

        for function in dic:
            cur.execute("DELETE FROM {0} WHERE ip='None'".format(function))
            con.commit()

            if function == "languages":
                for count in xrange(0, dic[function]):
                    rv = self.app.get('/api/languages')
                    assert 'bar' in rv.data
                rv = self.app.get('/api/languages')
                assert 'bar' in rv.data

            elif function == "corpus":
                for count in xrange(0, dic[function]):
                    rv = self.app.get('/api/corpus?iso=bar')
                    assert 'barwiki.zip' in rv.data
                rv = self.app.get('/api/corpus?iso=bar')
                assert 'barwiki.zip' in rv.data



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()