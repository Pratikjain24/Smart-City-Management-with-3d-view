"""Bundled Mumbai demonstration dataset — static fixtures, not a live feed.

Honesty labels are baked as literals at the source of truth: every record here is
SAMPLE_BUNDLED_DATA with freshness "Bundled sample — not a live feed". There is no
import-time normalization pass; what you read is what the API serves.
"""

MUMBAI_METADATA = {'city_id': 'mumbai_01',
 'name': 'Mumbai Metropolitan City',
 'state': 'Maharashtra',
 'country': 'India',
 'center': [72.8777, 19.076],
 'bounding_box': [72.75, 18.88, 73.05, 19.32],
 'elevation_datum': 'MSL (Mumbai Municipal Datum)',
 'admin_wards': [{'id': 'ward_a',
                  'name': 'A Ward (Colaba, Fort, Marine Drive)',
                  'center': [72.8311, 18.922]},
                 {'id': 'ward_d',
                  'name': 'D Ward (Malabar Hill, Grant Road)',
                  'center': [72.8126, 18.9634]},
                 {'id': 'ward_f_north',
                  'name': 'F/North Ward (Matunga, Sion, Wadala)',
                  'center': [72.8611, 19.0345]},
                 {'id': 'ward_g_south',
                  'name': 'G/South Ward (Worli, Lower Parel, Prabhadevi)',
                  'center': [72.8258, 19.002]},
                 {'id': 'ward_h_west',
                  'name': 'H/West Ward (Bandra West, Khar, Santacruz W)',
                  'center': [72.8362, 19.0596]},
                 {'id': 'ward_k_east',
                  'name': 'K/East Ward (Andheri East, SEEPZ, Marol)',
                  'center': [72.8697, 19.1136]},
                 {'id': 'ward_k_west',
                  'name': 'K/West Ward (Andheri West, Juhu, Versova)',
                  'center': [72.8267, 19.1197]},
                 {'id': 'ward_l',
                  'name': 'L Ward (Kurla, Sakinaka, Chandivali)',
                  'center': [72.889, 19.0726]},
                 {'id': 'ward_r_south',
                  'name': 'R/South Ward (Kandivali, Charkop)',
                  'center': [72.8436, 19.2064]},
                 {'id': 'ward_r_central',
                  'name': 'R/Central Ward (Borivali, Gorai)',
                  'center': [72.8567, 19.2307]}]}
