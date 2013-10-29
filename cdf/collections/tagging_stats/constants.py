from cdf.streams.mapping import CONTENT_TYPE_INDEX


CROSS_PROPERTIES_COLUMNS = ('suggest_combination', 'content_type', 'depth', 'http_code', 'index', 'follow')

COUNTERS_FIELDS = (
    'pages_nb',
    'total_delay_ms',
    'redirections_nb',
    'canonical_nb',
    'canonical_nb.filled',
    'canonical_nb.not_filled',
    'canonical_nb.equal',
    'canonical_nb.not_equal',
    'canonical_nb.incoming',

    'inlinks_internal_nb',
    'inlinks_internal_nb.total',
    'inlinks_internal_nb.follow',
    'inlinks_internal_nb.follow_unique',
    'inlinks_internal_nb.nofollow',
    'inlinks_internal_nb.nofollow_combinations',
    'inlinks_internal_nb.nofollow_combinations.link',
    'inlinks_internal_nb.nofollow_combinations.link_meta',
    'inlinks_internal_nb.nofollow_combinations.link_meta_robots',
    'inlinks_internal_nb.nofollow_combinations.link_robots',
    'inlinks_internal_nb.nofollow_combinations.meta',
    'inlinks_internal_nb.nofollow_combinations.meta_robots',

    'outlinks_internal_nb',
    'outlinks_internal_nb.total',
    'outlinks_internal_nb.follow',
    'outlinks_internal_nb.follow_unique',
    'outlinks_internal_nb.nofollow',
    'outlinks_internal_nb.nofollow_combinations',
    'outlinks_internal_nb.nofollow_combinations.link',
    'outlinks_internal_nb.nofollow_combinations.link_meta',
    'outlinks_internal_nb.nofollow_combinations.link_meta_robots',
    'outlinks_internal_nb.nofollow_combinations.link_robots',
    'outlinks_internal_nb.nofollow_combinations.meta',
    'outlinks_internal_nb.nofollow_combinations.meta_robots',
    'outlinks_internal_nb.nofollow_combinations.robots',

    'outlinks_external_nb',
    'outlinks_external_nb.total',
    'outlinks_external_nb.follow',
    'outlinks_external_nb.nofollow',
    'outlinks_external_nb.nofollow_combinations',
    'outlinks_external_nb.nofollow_combinations.link',
    'outlinks_external_nb.nofollow_combinations.link_meta',
    'outlinks_external_nb.nofollow_combinations.meta',

    'delay_gte_2s',
    'delay_from_1s_to_2s',
    'delay_from_500ms_to_1s',
    'delay_lt_500ms',
    'metadata_nb',
    'metadata_nb.not_enough'
)

for ct_txt in CONTENT_TYPE_INDEX.itervalues():
    COUNTERS_FIELDS += ('metadata_nb.%s.not_filled' % ct_txt, 'metadata_nb.%s.filled' % ct_txt, 'metadata_nb.%s.unique' % ct_txt)