from cdf.metadata.url.url_metadata import FLOAT_TYPE
from cdf.core.metadata.constants import RENDERING
from cdf.core.insights import Insight, PositiveTrend
from cdf.query.filter import (
    AndFilter, EqFilter, LtFilter,
    GteFilter, BetweenFilter, NotFilter
)
from cdf.query.aggregation import AvgAggregation
from cdf.query.sort import (
    AscendingSort, DescendingSort
)


def get_all_urls_insight():
    return [
        Insight(
            "all",
            "Crawled URLs",
            PositiveTrend.UNKNOWN
        )
    ]


def get_http_code_is_good_predicate():
    """Helper function that returns a filter that selects
    urls with good http code
    :returns: Filter
    """
    # TODO implement http_code_is_good
    return BetweenFilter("http_code", [200, 299])


def get_http_code_ok_ko_insights():
    return [
        Insight(
            "code_ok",
            "Good HTTP Status Code URLs",
            PositiveTrend.UP,
            get_http_code_is_good_predicate()
        ),
        Insight(
            "code_ko",
            "Bad HTTP Status Code URLs",
            PositiveTrend.DOWN,
            NotFilter(get_http_code_is_good_predicate())
        )
    ]


def get_http_code_ranges_insights():
    #insights by http ranges
    result = []
    ranges = [
        (200, PositiveTrend.UP),
        (300, PositiveTrend.DOWN),
        (400, PositiveTrend.DOWN),
        (500, PositiveTrend.DOWN)
    ]
    field = 'http_code'
    additional_fields = [field]

    for range_start, positive_trend in ranges:
        range_name = "{}xx".format(range_start / 100)
        insight = Insight(
            "code_{}".format(range_name),
            "{} URLs".format(range_name),
            positive_trend,
            BetweenFilter("http_code", [range_start, range_start + 99]),
            additional_fields=additional_fields,
            sort_by=AscendingSort(field)
        )
        result.append(insight)

    #special range for codes lower than 0
    result.append(
        Insight(
            "code_network_errors",
            "Network Errors",
            PositiveTrend.DOWN,
            LtFilter("http_code", 0),
            additional_fields=additional_fields,
            sort_by=AscendingSort(field)
        )
    )

    return result


def get_http_code_insights():
    #insights by http code
    result = []
    http_codes = [
        (200, PositiveTrend.UP),
        (301, PositiveTrend.DOWN),
        (302, PositiveTrend.DOWN),
        (304, PositiveTrend.DOWN),
        (403, PositiveTrend.DOWN),
        (404, PositiveTrend.DOWN),
        (410, PositiveTrend.DOWN),
    ]
    for code, positive_trend in http_codes:
        insight = Insight(
            "code_{}".format(code),
            "{} URLs".format(code),
            positive_trend,
            EqFilter("http_code", code)
        )
        result.append(insight)
    return result


def get_strategic_urls_insights():
    return [
        Insight(
            "strategic_1",
            "Strategic Urls",
            PositiveTrend.UP,
            EqFilter("strategic.is_strategic", True)
        ),
        Insight(
            "strategic_0",
            "Not Strategic URLs",
            PositiveTrend.DOWN,
            EqFilter("strategic.is_strategic", False)
        )
    ]


def get_content_type_insights():
    #insights for content types
    result = []
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    content_type_field = "content_type"
    for content_type in [TEXT_HTML, TEXT_CSS]:
        insight = Insight(
            "content_{}".format(content_type),
            "{} URLs".format(content_type[len("text/"):].upper()),
            PositiveTrend.UNKNOWN,
            EqFilter(content_type_field, content_type)
        )
        result.append(insight)

    result.append(
        Insight(
            "content_not_html",
            "Not HTML URLs",
            PositiveTrend.UNKNOWN,
            NotFilter(EqFilter(content_type_field, TEXT_HTML)),
            additional_fields=[content_type_field],
            sort_by=AscendingSort(content_type_field)
        )
    )
    return result


def get_protocol_insights():
    result = []
    for protocol in ["http", "https"]:
        insight = Insight(
            "protocol_{}".format(protocol),
            "{} URLs".format(protocol.upper()),
            PositiveTrend.UNKNOWN,
            EqFilter("protocol", protocol)
        )
        result.append(insight)
    return result


#speed insights
def get_speed_insights():
    field = "delay_last_byte"
    additional_fields = [field]
    return [
        Insight(
            "speed_fast",
            "Fast URLs (<500 ms)",
            PositiveTrend.UP,
            LtFilter(field, 500),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_medium",
            "Medium URLs (500 ms < 1 s)",
            PositiveTrend.DOWN,
            BetweenFilter(field, [500, 999]),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_slow",
            "Slow URLs (1 s < 2 s)",
            PositiveTrend.DOWN,
            BetweenFilter(field, [1000, 1999]),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_slowest",
            "Slowest URLs (>2 s)",
            PositiveTrend.DOWN,
            GteFilter(field, 2000),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_gt_1s",
            "Slow URLs (>1s)",
            PositiveTrend.DOWN,
            GteFilter(field, 1000),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        )
    ]


def get_strategic_urls_speed_insights():
    field = "delay_last_byte"
    additional_fields = [field]
    strategic_predicate = EqFilter("strategic.is_strategic", True)
    return [
        Insight(
            "speed_fast_strategic",
            "Fast Strategic URLs (<500 ms)",
            PositiveTrend.UP,
            AndFilter(
                [
                    strategic_predicate,
                    LtFilter(field, 500),
                ]
            ),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_medium_strategic",
            "Medium Strategic URLs (500 ms < 1 s)",
            PositiveTrend.DOWN,
            AndFilter(
                [
                    strategic_predicate,
                    BetweenFilter(field, [500, 999]),
                ]
            ),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_slow_strategic",
            "Slow Strategic URLs (1 s < 2 s)",
            PositiveTrend.DOWN,
            AndFilter(
                [
                    strategic_predicate,
                    BetweenFilter(field, [1000, 1999]),
                ]
            ),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
        Insight(
            "speed_slowest_strategic",
            "Slowest Strategic URLs (>2 s)",
            PositiveTrend.DOWN,
            AndFilter(
                [
                    strategic_predicate,
                    GteFilter(field, 2000),
                ]
            ),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields
        ),
    ]


#insights for domain/subdomains
def get_domain_insights():
    www_predicate = EqFilter("host", "www")
    return [
        Insight(
            "domain_www",
            "URLs from WWW",
            PositiveTrend.UNKNOWN,
            www_predicate
        ),
        Insight(
            "domain_not_www",
            "URLs from Subdomains",
            PositiveTrend.UNKNOWN,
            NotFilter(www_predicate)
        )
    ]


def get_average_speed_insights():
    field = "delay_last_byte"
    additional_fields = [field]
    return [
        Insight(
            "speed_avg",
            "Average Load Time (in ms)",
            PositiveTrend.DOWN,
            metric_agg=AvgAggregation(field),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields,
            unit=RENDERING.TIME_MILLISEC  # the param is a string so we need to use the enum value
        ),
        Insight(
            "speed_strategic_avg",
            "Average Load Time on Strategic URLs (in ms)",
            EqFilter("strategic.is_strategic", True),
            metric_agg=AvgAggregation(field),
            sort_by=DescendingSort(field),
            additional_fields=additional_fields,
            unit=RENDERING.TIME_MILLISEC  # the param is a string so we need to use the enum value
        ),
    ]


def get_average_depth_insights():
    field = "depth"
    additional_fields = [field]
    return [
        Insight(
            "depth_avg",
            "Average Depth",
            PositiveTrend.DOWN,
            metric_agg=AvgAggregation(field),
            additional_fields=additional_fields,
            sort_by=AscendingSort(field),
            type=FLOAT_TYPE,
            unit=RENDERING.DEPTH
        ),
        Insight(
            "depth_strategic_avg",
            "Average Depth on Strategic URLs",
            PositiveTrend.DOWN,
            EqFilter("strategic.is_strategic", True),
            metric_agg=AvgAggregation(field),
            additional_fields=additional_fields,
            sort_by=AscendingSort(field),
            type=FLOAT_TYPE,
            unit=RENDERING.DEPTH
        )
    ]


def get_index_insights():
    field = "metadata.robots.noindex"
    return [
        Insight(
            "index_ok",
            "Index URLs",
            PositiveTrend.UNKNOWN,
            EqFilter(field, False)
        ),
        Insight(
            "index_ko",
            "No-Index URLs",
            PositiveTrend.UNKNOWN,
            EqFilter(field, True)
        )
    ]


def get_gzipped_insights():
    field = "gzipped"
    return [
        Insight(
            "gzipped_ok",
            "GZIP URLs",
            PositiveTrend.UNKNOWN,
            EqFilter(field, True)
        ),
        Insight(
            "gzipped_ko",
            "Non GZIP URLs",
            PositiveTrend.UNKNOWN,
            EqFilter(field, False)
        )
    ]


def get_insights():
    insights = []
    insights.extend(get_all_urls_insight())
    insights.extend(get_http_code_ok_ko_insights())
    insights.extend(get_http_code_ranges_insights())
    insights.extend(get_http_code_insights())
    insights.extend(get_strategic_urls_insights())
    insights.extend(get_content_type_insights())
    insights.extend(get_protocol_insights())
    insights.extend(get_speed_insights())
    insights.extend(get_strategic_urls_speed_insights())
    insights.extend(get_domain_insights())
    insights.extend(get_average_speed_insights())
    insights.extend(get_average_depth_insights())
    insights.extend(get_index_insights())
    insights.extend(get_gzipped_insights())
    return insights

#actual insight definition
insights = get_insights()
