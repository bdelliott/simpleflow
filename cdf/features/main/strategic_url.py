from cdf.core.streams.utils import group_left
from cdf.features.main.streams import InfosStreamDef
from .reasons import *

STRATEGIC_HTTP_CODE = 200
STRATEGIC_CONTENT_TYPE = 'text/html'


def is_strategic_url(url_id, infos_mask, http_code,
                     content_type, outlinks):
    """Logic to check if a url is SEO strategic

    It returns a tuple of form:
        (is_strategic, reason_mask)
    If a url is not SEO strategic, `reason_mask` will be non empty

    :param url_id: url id
    :type url_id: int
    :param infos_mask: `urlinfos`'s mask
    :type infos_mask: int
    :param http_code: http code
    :type http_code: int
    :param content_type: content type of the url
    :type content_type: str
    :param outlinks: all out-going links to the url
    :type outlinks: list
    :return: tuple indicating if the url is strategic plus its reason
    :rtype (bool, int)
    """
    reasons = set()

    # check `http_code`
    if http_code != STRATEGIC_HTTP_CODE:
        reasons.add(REASON_HTTP_CODE)

    # check `content_type`
    if content_type != STRATEGIC_CONTENT_TYPE:
        reasons.add(REASON_CONTENT_TYPE)

    # check no-index
    noindex = ((4 & infos_mask) == 4)
    if noindex == True:
        reasons.add(REASON_NOINDEX)

    # check `canonical`
    canonical_dest = None
    for _, link_type, _, dest, _ in outlinks:
        # takes the first canonical
        if link_type.startswith('c'):
            canonical_dest = dest
            break

    if canonical_dest is not None:
        if canonical_dest != url_id:
            reasons.add(REASON_CANONICAL)

    if len(reasons) > 0:
        return False, encode_reason_mask(*reasons)
    else:
        return True, 0


def generate_strategic_stream(infos_stream, outlinks_stream):
    """Generate a strategic url stream

    :param infos_stream: stream of dataset `urlinfos`
    :param outlinks_stream: stream of dataset `urloutlinks`
    :return: the strategic stream
    """
    http_idx = InfosStreamDef.field_idx('http_code')
    mask_idx = InfosStreamDef.field_idx('infos_mask')
    ctype_idx = InfosStreamDef.field_idx('content_type')

    grouped_stream = group_left(left=(infos_stream, 0),
                                outlinks_stream=(outlinks_stream, 0))

    for uid, info, outlink in grouped_stream:
        http_code = info[http_idx]
        outlinks = outlink['outlinks_stream']
        infos_mask = info[mask_idx]
        content_type = info[ctype_idx]

        is_strategic, reason_mask = is_strategic_url(
            uid,
            infos_mask,
            http_code,
            content_type,
            outlinks
        )

        yield uid, is_strategic, reason_mask