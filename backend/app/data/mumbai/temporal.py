"""Bundled Mumbai demonstration dataset — static fixtures, not a live feed.

Honesty labels are baked as literals at the source of truth: every record here is
SAMPLE_BUNDLED_DATA with freshness "Bundled sample — not a live feed". There is no
import-time normalization pass; what you read is what the API serves.
"""

TEMPORAL_STATES = {'historical_2020': {'year': 2020,
                     'title': 'Historical 2020: Baseline Pre-Coastal Road',
                     'description': 'Mumbai baseline prior to Coastal Road reclamation, Metro Line '
                                    '3 tunneling active underground, Metro 2A/7 in civil '
                                    'construction stage.',
                     'coastal_road_status': 'Reclamation & Seawall Construction (32% complete)',
                     'metro_line_3_status': 'TBM Tunneling Stage (17 TBMs active under South '
                                            'Mumbai)',
                     'avg_peak_commute_mins': 74,
                     'air_quality_avg_aqi': 185},
 'historical_2023': {'year': 2023,
                     'title': 'Historical 2023: Undersea Tunnel Breakthrough & Metro 2A/7 Launch',
                     'description': 'Girgaon twin undersea road tunnels excavated, Metro Line 2A & '
                                    '7 fully open to public, BWSL integration ramps progressing.',
                     'coastal_road_status': 'Twin Undersea Tunnels Completed (88% overall project)',
                     'metro_line_3_status': 'Track laying and sub-station electrification',
                     'avg_peak_commute_mins': 62,
                     'air_quality_avg_aqi': 158},
 'live_2026': {'year': 2026,
               'title': 'Current Demonstration State (SIMULATED)',
               'description': 'Current-time simulation using bundled Mumbai demonstration data; no '
                              'external live feed is configured.',
               'coastal_road_status': 'Fully Operational (8 lanes with SCADA monitoring)',
               'metro_line_3_status': 'Fully Operational carrying 450k daily commuters',
               'avg_peak_commute_mins': 44,
               'air_quality_avg_aqi': 142},
 'future_2028': {'year': 2028,
                 'title': 'Simulated Future 2028: Multi-Modal Metro Network & Bullet Train',
                 'description': 'Simulated scenario with Metro Lines 4, 6, and 11 fully '
                                'integrated, Mumbai-Ahmedabad High-Speed Rail underground BKC '
                                'terminal operational, Coastal Road North extension to Versova.',
                 'coastal_road_status': 'Phase 2 Versova Extension Operational',
                 'metro_line_3_status': 'Integrated with Metro 6 and Bullet Train Hub',
                 'avg_peak_commute_mins': 31,
                 'air_quality_avg_aqi': 110},
 'future_2030': {'year': 2030,
                 'title': 'Simulated Future 2030: Zero-Emission Transit & Climate Resilience',
                 'description': '100% electrified public transport bus fleet, BRIMSTOWAD 2.0 '
                                'automated tidal surge gates at Mithi and Love Grove, smart grid '
                                'micro-turbines along coastal seawall.',
                 'coastal_road_status': 'Autonomous EV dedicated lanes enabled',
                 'metro_line_3_status': 'Continuous AI-optimized signaling (CBTC 90s headway)',
                 'avg_peak_commute_mins': 24,
                 'air_quality_avg_aqi': 82}}
