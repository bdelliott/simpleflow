# -*- coding:utf-8 -*-
import unittest
import logging
from pandas import DataFrame

from cdf.log import logger
from cdf.collections.tagging_stats.request import MetricsRequest

logger.setLevel(logging.DEBUG)


class TestPropertiesStats(unittest.TestCase):

    def setUp(self):
        self.data = [
            {'host': 'www.site.com',
             'content_type': 'text/html',
             'resource_type': 'article',
             'depth': 1,
             'follow': True,
             'index': True,
             'http_code': 200,
             'pages_nb': 10,
             'outlinks_nofollow_link__nofollow_meta_nb': 5
             },
            {'host': 'subdomain.site.com',
             'content_type': 'text/html',
             'resource_type': 'photo',
             'depth': 5,
             'follow': True,
             'index': True,
             'http_code': 200,
             'pages_nb': 20,
             'outlinks_nofollow_link__nofollow_meta_nb': 4,
             'outlinks_nofollow_link__nofollow_robots_nb': 8
             }
        ]

    def tearDown(self):
        pass

    def test_simple(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        settings = {
            'fields': ['pages_nb', 'outlinks_nb']
        }

        self.assertItemsEqual(request.query(settings)['counters'],
                              {
                                  'pages_nb': 10,
                                  'outlinks_nb': {
                                      'total': 17,
                                      'nofollow_link__nofollow_meta': 9,
                                      'nofollow_link__nofollow_robots': 8
                                  }
                              })

        settings = {
            'fields': ['pages_nb', 'outlinks_nb', 'inlinks_nb'],
            'filters': [
                {'field': 'host', 'value': 'www.site.com'}
            ]
        }

        self.assertEquals(request.query(settings)['counters'],
                          {
                              'pages_nb': 10,
                              'outlinks_nb': {
                                  'total': 5,
                                  'nofollow_link__nofollow_meta': 5,
                              },
                              'inlinks_nb': {
                                  'total': 0
                              }
                          })

        # Implicit OR
        settings = {
            'fields': ['pages_nb', 'outlinks_nb'],
            'filters': [
                {'field': 'host', 'value': 'www.site.com'},
                {'field': 'host', 'value': 'subdomain.site.com'}
            ]
        }
        expected_result = {
            'pages_nb': 10,
            'outlinks_nb': {
                'total': 17,
                'nofollow_link__nofollow_meta': 9,
                'nofollow_link__nofollow_robots': 8
            }
        }
        self.assertItemsEqual(request.query(settings)['counters'], expected_result)

        # explicit OR condition
        settings['filters'] = {
            'or': [
                {'field': 'host', 'value': 'www.site.com'},
                {'field': 'host', 'value': 'subdomain.site.com'}
            ]
        }
        self.assertItemsEqual(request.query(settings)['counters'], expected_result)

        # AND condition
        settings['filters'] = {
            'and': [
                {'field': 'host', 'predicate': 'ends', 'value': '.site.com'},
                {'field': 'resource_type', 'value': 'article'}
            ]
        }
        self.assertEquals(request.query(settings)['counters'],
                          {
                              'pages_nb': 10,
                              'outlinks_nb': {
                                  'total': 5,
                                  'nofollow_link__nofollow_meta': 5,
                              }
                          })

    def test_predicates(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)
        settings = {
            'fields': ['pages_nb'],
            'filters': [
            ]
        }

        # eq explicit
        settings['filters'] = [
            {'field': 'host', 'predicate': 'eq', 'value': 'www.site.com'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 10})

        # eq implicit
        settings['filters'] = [
            {'field': 'host', 'value': 'www.site.com'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 10})

        # in implicit
        settings['filters'] = [
            {'field': 'host', 'value': ['www.site.com', 'subdomain.site.com']}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

        # in explicit
        settings['filters'] = [
            {'field': 'host', 'predicate': 'in', 'value': ['www.site.com', 'subdomain.site.com']}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

        # starts
        settings['filters'] = [
            {'field': 'host', 'predicate': 'starts', 'value': 'www'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 10})

        # ends
        settings['filters'] = [
            {'field': 'host', 'predicate': 'ends', 'value': '.site.com'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

        # contains
        settings['filters'] = [
            {'field': 'host', 'predicate': 'contains', 'value': '.site.'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

        # re
        settings['filters'] = [
            {'field': 'host', 'predicate': 're', 'value': '(www|subdomain).site.com'}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

    def test_nested_filter(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        settings = {
            'fields': ['pages_nb']
        }

        # nested OR + AND conditions
        settings['filters'] = {
            'or': [
                {'and': [
                    {'field': 'host', 'value': 'www.site.com'},
                    {'field': 'resource_type', 'value': 'article'}
                ]},
                {'and': [
                    {'field': 'host', 'value': 'subdomain.site.com'},
                    {'field': 'resource_type', 'value': 'photo'}
                ]}
            ]
        }
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

    def test_filter_in(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        settings = {
            'fields': ['pages_nb']
        }

        # nested OR + AND conditions
        settings['filters'] = [
            {'field': 'host', 'value': ['www.site.com', 'subdomain.site.com']}
        ]
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 30})

    def test_sum_by_property_1dim(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        expected_results = [
            {
                "properties": {
                    "host": "www.site.com"
                },
                "counters": {
                    "pages_nb": 10
                }
            },
            {
                "properties": {
                    "host": "subdomain.site.com"
                },
                "counters": {
                    "pages_nb": 20
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

    def test_sum_by_property_2dim(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        expected_results = [
            {
                "properties": {
                    "host": "www.site.com",
                    "content_type": "text/html"
                },
                "counters": {
                    "pages_nb": 10,
                }
            },
            {
                "properties": {
                    "host": "subdomain.site.com",
                    "content_type": "text/html"
                },
                "counters": {
                    "pages_nb": 20
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host', 'content_type']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

    def test_sum_domains(self):
        self.data = [
            {'host': 'www.site.com',
             'content_type': 'text/html',
             'resource_type': 'article',
             'depth': 1,
             'follow': True,
             'index': True,
             'pages_nb': 10,
             },
            {'host': 'my.subdomain.site.com',
             'content_type': 'text/html',
             'resource_type': 'photo',
             'depth': 5,
             'follow': True,
             'index': True,
             'pages_nb': 20,
             },
            {'host': 'www.site.fr',
             'content_type': 'text/html',
             'resource_type': 'product',
             'depth': 1,
             'follow': True,
             'index': True,
             'pages_nb': 40,
             }
        ]

        df = DataFrame(self.data)
        request = MetricsRequest(df)

        # Level 1, TLDs
        expected_results = [
            {
                "properties": {
                    "host": "*.com",
                },
                "counters": {
                    "pages_nb": 30,
                }
            },
            {
                "properties": {
                    "host": "*.fr",
                },
                "counters": {
                    "pages_nb": 40
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host__level1']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        # Level 2, main domains
        expected_results = [
            {
                "properties": {
                    "host": "*.site.com",
                },
                "counters": {
                    "pages_nb": 30,
                }
            },
            {
                "properties": {
                    "host": "*.site.fr",
                },
                "counters": {
                    "pages_nb": 40
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host__level2']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        # Level 3, subdomains
        expected_results = [
            {
                "properties": {
                    "host": "www.site.com",
                },
                "counters": {
                    "pages_nb": 10,
                }
            },
            {
                "properties": {
                    "host": "*.subdomain.site.com",
                },
                "counters": {
                    "pages_nb": 20,
                }
            },
            {
                "properties": {
                    "host": "www.site.fr",
                },
                "counters": {
                    "pages_nb": 40
                }
            }
        ]

        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host__level3']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        # Level 4, my.subdomain.site.com
        expected_results = [
            {
                "properties": {
                    "host": "www.site.com",
                },
                "counters": {
                    "pages_nb": 10,
                }
            },
            {
                "properties": {
                    "host": "my.subdomain.site.com",
                },
                "counters": {
                    "pages_nb": 20,
                }
            },
            {
                "properties": {
                    "host": "www.site.fr",
                },
                "counters": {
                    "pages_nb": 40
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['host__level4']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

    def test_resource_type_levels(self):
        self.data = [
            {'host': 'www.site.com',
             'content_type': 'text/html',
             'resource_type': 'article/comments/p1',
             'depth': 1,
             'follow': True,
             'index': True,
             'pages_nb': 10,
             },
            {'host': 'www.site.com',
             'content_type': 'text/html',
             'resource_type': 'article/comments/px',
             'depth': 5,
             'follow': True,
             'index': True,
             'pages_nb': 20,
             },
            {'host': 'www.site.fr',
             'content_type': 'text/html',
             'resource_type': 'article/permalink',
             'depth': 1,
             'follow': True,
             'index': True,
             'pages_nb': 40,
             }
        ]

        df = DataFrame(self.data)
        request = MetricsRequest(df)

        # Level 1
        expected_results = [
            {
                "properties": {
                    "resource_type": "article/*",
                },
                "counters": {
                    "pages_nb": 70,
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['resource_type__level1']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        # Level 2
        expected_results = [
            {
                "properties": {
                    "resource_type": "article/comments/*",
                },
                "counters": {
                    "pages_nb": 30,
                }
            },
            {
                "properties": {
                    "resource_type": "article/permalink",
                },
                "counters": {
                    "pages_nb": 40,
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['resource_type__level2']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        # Level 3
        expected_results = [
            {
                "properties": {
                    "resource_type": "article/comments/p1",
                },
                "counters": {
                    "pages_nb": 10,
                }
            },
            {
                "properties": {
                    "resource_type": "article/comments/px",
                },
                "counters": {
                    "pages_nb": 20,
                }
            },
            {
                "properties": {
                    "resource_type": "article/permalink",
                },
                "counters": {
                    "pages_nb": 40,
                }
            }
        ]
        settings = {
            'fields': ['pages_nb'],
            'group_by': ['resource_type__level3']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

        settings = {
            'fields': ['pages_nb'],
            'group_by': ['resource_type__level4']
        }
        self.assertItemsEqual(request.query(settings), expected_results)

    def test_not(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        settings = {
            'fields': ['pages_nb'],
            'filters': [
                {'field': 'host', 'value': 'www.site.com', 'not': True}
            ]
        }
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 20})

        settings = {
            'fields': ['pages_nb'],
            'filters': [
                {'field': 'host', 'predicate':'ends', 'value': '.site.com', 'not': True}
            ]
        }
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 0})

        settings = {
            'fields': ['pages_nb'],
            'filters': [
                {'field': 'host', 'value': ['www.site.com', 'music.site.com'], 'not': True}
            ]
        }
        self.assertEquals(request.query(settings)['counters'], {'pages_nb': 20})

    def test_bad_field(self):
        df = DataFrame(self.data)
        request = MetricsRequest(df)

        settings = {
            'fields': ['pages_nb', 'bad_field']
        }

        with self.assertRaises(MetricsRequest.BadRequestException):
            request.query(settings)
