"""
MahaTwin Mumbai - Comprehensive Authoritative & Calibrated Spatial Dataset
Covers Mumbai City with high-precision GIS coordinates, connected graph topology,
underground utility networks, multi-modal transit corridors, and temporal states.
"""

from typing import Dict, Any, List
import time

MUMBAI_METADATA = {
    "city_id": "mumbai_01",
    "name": "Mumbai Metropolitan City",
    "state": "Maharashtra",
    "country": "India",
    "center": [72.8777, 19.0760],
    "bounding_box": [72.7500, 18.8800, 73.0500, 19.3200],
    "elevation_datum": "MSL (Mumbai Municipal Datum)",
    "admin_wards": [
        {"id": "ward_a", "name": "A Ward (Colaba, Fort, Marine Drive)", "center": [72.8311, 18.9220]},
        {"id": "ward_d", "name": "D Ward (Malabar Hill, Grant Road)", "center": [72.8126, 18.9634]},
        {"id": "ward_f_north", "name": "F/North Ward (Matunga, Sion, Wadala)", "center": [72.8611, 19.0345]},
        {"id": "ward_g_south", "name": "G/South Ward (Worli, Lower Parel, Prabhadevi)", "center": [72.8258, 19.0020]},
        {"id": "ward_h_west", "name": "H/West Ward (Bandra West, Khar, Santacruz W)", "center": [72.8362, 19.0596]},
        {"id": "ward_k_east", "name": "K/East Ward (Andheri East, SEEPZ, Marol)", "center": [72.8697, 19.1136]},
        {"id": "ward_k_west", "name": "K/West Ward (Andheri West, Juhu, Versova)", "center": [72.8267, 19.1197]},
        {"id": "ward_l", "name": "L Ward (Kurla, Sakinaka, Chandivali)", "center": [72.8890, 19.0726]},
        {"id": "ward_r_south", "name": "R/South Ward (Kandivali, Charkop)", "center": [72.8436, 19.2064]},
        {"id": "ward_r_central", "name": "R/Central Ward (Borivali, Gorai)", "center": [72.8567, 19.2307]}
    ]
}

# --- 1. CONNECTED ROAD NETWORK ---
# Formats roads with connected road IDs, lane data, traffic status, condition, and nearby infrastructure
ROADS_DATA: List[Dict[str, Any]] = [
    {
        "id": "road_weh_01",
        "name": "Western Express Highway (WEH) - Bandra to Andheri",
        "type": "Expressway",
        "category": "High-Speed Arterial",
        "lanes": 8,
        "speed_limit_kmh": 80,
        "avg_speed_kmh": 34,
        "traffic_status": "Heavy",
        "traffic_level": "ORANGE",
        "road_condition": "Good",
        "construction_status": "Operational (Flyover repair near Kalanagar)",
        "maintenance_status": "Regular Maintenance (BMC/MMRDA)",
        "known_incidents": 2,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (15s ago)",
        "coordinates": [
            [72.8465, 19.0558], # Kalanagar Bandra E
            [72.8498, 19.0689], # Bandra Kurla Flyover
            [72.8512, 19.0834], # Santacruz Airport Flyover
            [72.8530, 19.0970], # Vile Parle E
            [72.8560, 19.1155], # Andheri Flyover / Western Express Hwy Metro
            [72.8580, 19.1350]  # Jogeshwari Flyover
        ],
        "connected_road_ids": ["road_bwsl_01", "road_sclr_01", "road_jvlr_01", "road_bkc_01"],
        "nearby_intersections": ["Kalanagar Junction", "Vakola Junction", "Centaur Hotel Junction", "Gundavali Junction"],
        "signals": ["Kalanagar Smart Signal", "Vakola Bridge North Signal", "Airport Flyover South Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["Kalanagar", "Vakola Police Station", "Domestic Airport", "Gundavali"],
            "railway_stations": ["Bandra Station (1.2 km)", "Santacruz Station (0.9 km)", "Andheri Station (1.1 km)"],
            "metro": ["Line 7 Gundavali", "Line 1 WEH Metro Station", "Line 2B under construction"],
            "hospitals": ["Nanavati Max Super Speciality", "Guru Nanak Hospital", "Holy Spirit Hospital"],
            "utilities": ["Bhandup Trunk Water Main (4m offset)", "Tata 220kV Conduits", "BRIMSTOWAD SWD Vakola Nullha"]
        }
    },
    {
        "id": "road_bwsl_01",
        "name": "Bandra-Worli Sea Link (Rajiv Gandhi Sea Link)",
        "type": "Cable-Stayed Bridge / Expressway",
        "category": "Sea Bridge",
        "lanes": 8,
        "speed_limit_kmh": 80,
        "avg_speed_kmh": 72,
        "traffic_status": "Normal",
        "traffic_level": "GREEN",
        "road_condition": "Excellent",
        "construction_status": "Fully Operational (Integrated with Coastal Road South)",
        "maintenance_status": "MSRDC Monitored Structural Health",
        "known_incidents": 0,
        "data_provenance": "LIVE_SENSORS",
        "freshness": "Realtime (8s ago)",
        "coordinates": [
            [72.8360, 19.0430], # Bandra Toll Plaza
            [72.8250, 19.0340], # Cable Stayed Main Span
            [72.8160, 19.0200], # Mahim Bay Mid Span
            [72.8135, 19.0080], # Worli Sea Face Connector
            [72.8150, 18.9990]  # Worli Interchange
        ],
        "connected_road_ids": ["road_weh_01", "road_coastal_01", "road_worli_01"],
        "nearby_intersections": ["Bandra Toll Plaza", "Worli Sea Face Connector", "Bindumadhav Thackeray Chowk"],
        "signals": ["Toll Electronic Gantry", "Worli Exit Dynamic Messaging Sign"],
        "nearby_infrastructure": {
            "bus_stops": ["Bandra Reclamation Bus Depot", "Worli Sea Face North"],
            "railway_stations": ["Bandra Station (2.5 km)", "Prabhadevi Station (2.1 km)"],
            "metro": ["Line 3 Worli (1.5 km)"],
            "hospitals": ["Lilavati Hospital & Research Centre", "Podar Hospital Worli"],
            "utilities": ["Deep Sea Marine Outfall Subsea Pipeline (12m depth)"]
        }
    },
    {
        "id": "road_coastal_01",
        "name": "Dharmveer Swarajya Rakshak CSM Coastal Road",
        "type": "Freeway & Undersea Tunnel",
        "category": "Coastal Expressway",
        "lanes": 8,
        "speed_limit_kmh": 80,
        "avg_speed_kmh": 68,
        "traffic_status": "Normal",
        "traffic_level": "GREEN",
        "road_condition": "Brand New / State of the Art",
        "construction_status": "Phase 1 Operational / Phase 2 Interconnection",
        "maintenance_status": "BMC Coastal Road Department",
        "known_incidents": 0,
        "data_provenance": "LIVE_OPERATIONAL",
        "freshness": "Realtime (20s ago)",
        "coordinates": [
            [72.8150, 18.9990], # Worli Interchange
            [72.8080, 18.9850], # Haji Ali Sea Promenade
            [72.8020, 18.9680], # Breach Candy Promenade
            [72.7980, 18.9550], # Undersea Twin Tunnel (Girgaon/Malabar)
            [72.8180, 18.9440], # Marine Drive Princess Street Flyover exit
            [72.8240, 18.9380]  # Marine Drive Promenade
        ],
        "connected_road_ids": ["road_bwsl_01", "road_marine_drive_01", "road_pedder_01"],
        "nearby_intersections": ["Worli Bindumadhav Chowk", "Haji Ali Interchange", "Amarson Garden Junction", "Princess Street Flyover"],
        "signals": ["Coastal SCADA Automated Speed Enforcement", "Tunnel Emergency Extraction Signals"],
        "nearby_infrastructure": {
            "bus_stops": ["Haji Ali Juice Centre", "Breach Candy Hospital", "Princess Street"],
            "railway_stations": ["Grant Road (1.4 km)", "Charni Road (0.6 km)", "Marine Lines (0.5 km)"],
            "metro": ["Line 3 Girgaon & Grant Road Underground Stations"],
            "hospitals": ["Breach Candy Hospital", "Jaslok Hospital", "Saifee Hospital"],
            "utilities": ["Coastal Storm Sea Surge Defense Culverts", "Tunnel Fire Suppression Mains"]
        }
    },
    {
        "id": "road_marine_drive_01",
        "name": "Netaji Subhash Chandra Bose Road (Marine Drive Promenade)",
        "type": "Arterial Boulevard",
        "category": "Heritage Coastal Boulevard",
        "lanes": 6,
        "speed_limit_kmh": 60,
        "avg_speed_kmh": 42,
        "traffic_status": "Normal",
        "traffic_level": "GREEN",
        "road_condition": "Good",
        "construction_status": "Operational",
        "maintenance_status": "Heritage Zone Maintained (BMC A & C Ward)",
        "known_incidents": 0,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (12s ago)",
        "coordinates": [
            [72.8240, 18.9380], # Princess Street North
            [72.8235, 18.9300], # Marine Lines Flyover / Marine Plaza
            [72.8228, 18.9240], # Churchgate Station Forecourt
            [72.8210, 18.9180], # Air India Building / Trident
            [72.8185, 18.9140]  # Nariman Point NCPA
        ],
        "connected_road_ids": ["road_coastal_01", "road_madame_cama_01", "road_pedder_01"],
        "nearby_intersections": ["Mafatlal Bath Chowk", "Veer Nariman Road Chowk", "Madame Cama Junction", "NCPA Terminal"],
        "signals": ["Marine Drive / Veer Nariman Signal", "Air India Building Junction Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["NCPA Nariman Point", "Air India", "Marine Hotel", "Charni Road Station"],
            "railway_stations": ["Churchgate Railway Terminus (0.3 km)", "Marine Lines (0.2 km)"],
            "metro": ["Line 3 Vidhan Bhavan Station (0.4 km)", "Line 3 Churchgate (0.3 km)"],
            "hospitals": ["Bombay Hospital & Medical Research Centre (1.1 km)", "GT Hospital"],
            "utilities": ["South Mumbai Heritage Sewer Collectors", "Sea-wall drainage sluice gates"]
        }
    },
    {
        "id": "road_eeh_01",
        "name": "Eastern Express Highway (EEH) - Sion to Thane",
        "type": "Expressway",
        "category": "High-Speed Arterial",
        "lanes": 8,
        "speed_limit_kmh": 80,
        "avg_speed_kmh": 48,
        "traffic_status": "Moderate",
        "traffic_level": "YELLOW",
        "road_condition": "Good",
        "construction_status": "Metro Line 4 Construction along corridor",
        "maintenance_status": "Regular MMRDA Maintenance",
        "known_incidents": 1,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (30s ago)",
        "coordinates": [
            [72.8630, 19.0400], # Sion Circle / Priyadarshini Park
            [72.8790, 19.0620], # Chembur Amar Mahal Junction
            [72.9050, 19.0880], # Ghatkopar Chheda Nagar
            [72.9260, 19.1120], # Vikhroli Godrej Flyover
            [72.9420, 19.1410], # Kanjurmarg / Bhandup Junction
            [72.9600, 19.1760]  # Mulund Check Naka
        ],
        "connected_road_ids": ["road_sclr_01", "road_jvlr_01", "road_freeway_01"],
        "nearby_intersections": ["Amar Mahal Junction", "Chheda Nagar Junction", "Vikhroli Depot Chowk", "Mulund Airoli Bridge Chowk"],
        "signals": ["Chheda Nagar Smart Gantry", "Vikhroli East Signal", "Mulund Flyover Entry"],
        "nearby_infrastructure": {
            "bus_stops": ["Sion Chunabhatti", "Amar Mahal", "Chheda Nagar", "Godrej Vikhroli"],
            "railway_stations": ["Vikhroli Station (0.8 km)", "Ghatkopar Station (1.2 km)", "Kanjurmarg (0.6 km)"],
            "metro": ["Line 4 Green Line (underway)", "Line 1 Ghatkopar Interchange (1.2 km)"],
            "hospitals": ["Godrej Memorial Hospital", "Fortis Hospital Mulund", "Sion Municipal Hospital"],
            "utilities": ["Tansa & Vihar Mega Water Trunk Mains", "MSETCL 400kV High Voltage Corridor"]
        }
    },
    {
        "id": "road_jvlr_01",
        "name": "Jogeshwari-Vikhroli Link Road (JVLR)",
        "type": "Arterial Connector",
        "category": "East-West Crosstown Corridor",
        "lanes": 6,
        "speed_limit_kmh": 60,
        "avg_speed_kmh": 22,
        "traffic_status": "Severe",
        "traffic_level": "RED",
        "road_condition": "Fair (Pothole repairs near SEEPZ)",
        "construction_status": "Metro Line 6 viaduct work in progress",
        "maintenance_status": "MMRDA Active Work Zone",
        "known_incidents": 3,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (5s ago)",
        "coordinates": [
            [72.8580, 19.1350], # WEH Jogeshwari Junction
            [72.8750, 19.1320], # Majas Depot / Western Railway Cross
            [72.8910, 19.1280], # SEEPZ / Powai Lake West
            [72.9060, 19.1230], # IIT Bombay Main Gate
            [72.9180, 19.1200], # Gandhi Nagar / Kanjurmarg West
            [72.9260, 19.1120]  # EEH Vikhroli Junction
        ],
        "connected_road_ids": ["road_weh_01", "road_eeh_01", "road_sv_road_01", "road_lbs_01"],
        "nearby_intersections": ["Jogeshwari WEH Junction", "SEEPZ Gate 1 Chowk", "IIT Powai Main Gate", "Gandhi Nagar Kanjurmarg Chowk"],
        "signals": ["JVLR SEEPZ Signal", "IIT Powai Gate Signal", "Gandhi Nagar Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["Majas Depot", "SEEPZ Village", "IIT Main Gate", "Powai Plaza"],
            "railway_stations": ["Jogeshwari (1.4 km)", "Kanjurmarg (0.9 km)"],
            "metro": ["Line 6 JVLR (under construction)", "Line 3 SEEPZ Station"],
            "hospitals": ["Dr L H Hiranandani Hospital", "SevenHills Hospital Marol"],
            "utilities": ["Powai Lake Overflow Spillway Drain", "Bhandup Water Pumping Secondary Main"]
        }
    },
    {
        "id": "road_sclr_01",
        "name": "Santacruz-Chembur Link Road (SCLR) & Extension",
        "type": "Elevated Expressway",
        "category": "East-West Crosstown Corridor",
        "lanes": 6,
        "speed_limit_kmh": 60,
        "avg_speed_kmh": 40,
        "traffic_status": "Moderate",
        "traffic_level": "YELLOW",
        "road_condition": "Good",
        "construction_status": "Operational",
        "maintenance_status": "MMRDA Monitored",
        "known_incidents": 1,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (18s ago)",
        "coordinates": [
            [72.8512, 19.0834], # WEH Santacruz East
            [72.8680, 19.0760], # BKC Connector / Vakola Nullah
            [72.8800, 19.0710], # Kurla Station Double Decker Flyover
            [72.8920, 19.0660], # Tilak Nagar / Lokmanya Tilak Terminus
            [72.8790, 19.0620]  # Amar Mahal EEH Junction
        ],
        "connected_road_ids": ["road_weh_01", "road_eeh_01", "road_bkc_01", "road_lbs_01"],
        "nearby_intersections": ["Vakola SCLR Entry", "Kurla CST Road Chowk", "Tilak Nagar Station Cut", "Amar Mahal Interchange"],
        "signals": ["SCLR Kurla East Signal", "CST Road Junction Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["Kurla Depot", "Tilak Nagar", "CST Road Kalina"],
            "railway_stations": ["Kurla Railway Station (0.3 km)", "Lokmanya Tilak Terminus LTT (0.5 km)"],
            "metro": ["Line 2B under construction", "Line 3 BKC (1.5 km)"],
            "hospitals": ["Bhabha Hospital Kurla", "Asian Heart Institute BKC"],
            "utilities": ["Mithi River Bridge Crossing Culverts", "Adani Power 110kV Cable Tray"]
        }
    },
    {
        "id": "road_bkc_01",
        "name": "Bandra Kurla Complex (BKC) Avenue & Financial Corridor",
        "type": "Smart Boulevard",
        "category": "Central Business District Hub",
        "lanes": 8,
        "speed_limit_kmh": 50,
        "avg_speed_kmh": 38,
        "traffic_status": "Normal",
        "traffic_level": "GREEN",
        "road_condition": "Excellent",
        "construction_status": "Bullet Train BKC Underground Station Works",
        "maintenance_status": "MMRDA Smart City Infrastructure",
        "known_incidents": 0,
        "data_provenance": "LIVE_IOT_SENSORS",
        "freshness": "Realtime (2s ago)",
        "coordinates": [
            [72.8498, 19.0689], # Kalanagar Entry
            [72.8600, 19.0665], # MMRDA Grounds / Jio World Centre
            [72.8680, 19.0640], # ICICI / NSE Headquarters
            [72.8730, 19.0655], # Diamond Bourse / US Consulate
            [72.8680, 19.0760]  # SCLR Connector
        ],
        "connected_road_ids": ["road_weh_01", "road_sclr_01"],
        "nearby_intersections": ["Kalanagar BKC Gate", "Jio World Drive Roundabout", "NSE Roundabout", "MTNL Junction"],
        "signals": ["BKC Smart Adaptive Traffic Control (SCATS)", "Jio Centre Pedestrian Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["MMRDA Building", "Diamond Bourse", "ICICI Bank BKC", "BKC Telephone Exchange"],
            "railway_stations": ["Bandra Station (1.8 km)", "Kurla Station (1.5 km)"],
            "metro": ["Line 3 BKC Underground Station", "Line 2B Income Tax Station (underway)"],
            "hospitals": ["Asian Heart Institute", "Lilavati (2.4 km)"],
            "utilities": ["Smart Gas Distribution Grid (Mahanagar Gas)", "Underground Fiber Ring", "Dual-feed 220kV Substation"]
        }
    },
    {
        "id": "road_lbs_01",
        "name": "Lal Bahadur Shastri (LBS) Marg - Sion to Mulund",
        "type": "Major Arterial",
        "category": "Central Suburbs Arterial",
        "lanes": 4,
        "speed_limit_kmh": 50,
        "avg_speed_kmh": 18,
        "traffic_status": "Severe",
        "traffic_level": "RED",
        "road_condition": "Moderate",
        "construction_status": "Metro Line 4 Pier erection",
        "maintenance_status": "BMC L & S Ward",
        "known_incidents": 2,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (10s ago)",
        "coordinates": [
            [72.8640, 19.0430], # Sion Hospital Circle
            [72.8750, 19.0680], # Kurla Kalpana Cinema Chowk
            [72.8980, 19.0910], # Ghatkopar Phoenix Marketcity
            [72.9180, 19.1170], # Vikhroli West Surya Nagar
            [72.9350, 19.1450], # Bhandup West Dream Mall
            [72.9510, 19.1720]  # Mulund Check Naka
        ],
        "connected_road_ids": ["road_sclr_01", "road_jvlr_01", "road_eeh_01"],
        "nearby_intersections": ["Kurla Depot Chowk", "Phoenix Marketcity Junction", "Gandhi Nagar LBS Junction", "Bhandup Sonapur Chowk"],
        "signals": ["Kalpana Cinema Signal", "Marketcity Gate 1 Signal", "Bhandup Sonapur Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["Kurla Depot", "Phoenix Marketcity", "Vikhroli Station West", "Bhandup Police Station"],
            "railway_stations": ["Kurla (0.5 km)", "Vidyavihar (0.7 km)", "Ghatkopar (0.8 km)", "Bhandup (0.6 km)"],
            "metro": ["Line 4 LBS Marg corridor", "Line 1 Ghatkopar Interchange"],
            "hospitals": ["Fauziya Hospital Kurla", "Sarvodaya Hospital Ghatkopar"],
            "utilities": ["Old Cast Iron Water Mains", "Deep Storm Sewer Channels", "MGL City Gas Pipelines"]
        }
    },
    {
        "id": "road_sv_road_01",
        "name": "Swami Vivekanand (SV) Road - Bandra to Borivali",
        "type": "Major Arterial",
        "category": "Western Suburbs Arterial",
        "lanes": 4,
        "speed_limit_kmh": 50,
        "avg_speed_kmh": 20,
        "traffic_status": "Heavy",
        "traffic_level": "ORANGE",
        "road_condition": "Moderate",
        "construction_status": "Ongoing utility underground ducting",
        "maintenance_status": "BMC H/W & K/W Wards",
        "known_incidents": 2,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (25s ago)",
        "coordinates": [
            [72.8390, 19.0570], # Bandra Lucky Restaurant Chowk
            [72.8395, 19.0770], # Khar & Santacruz West
            [72.8420, 19.1020], # Vile Parle Irla Bridge
            [72.8440, 19.1190], # Andheri Station West / SV Rd Market
            [72.8460, 19.1430], # Jogeshwari West
            [72.8480, 19.1750], # Malad West
            [72.8530, 19.2290]  # Borivali West
        ],
        "connected_road_ids": ["road_jvlr_01", "road_weh_01"],
        "nearby_intersections": ["Lucky Hotel Bandra", "Milan Subway Junction", "Andheri Market Chowk", "SV Road Jogeshwari Gate"],
        "signals": ["Bandra Jama Masjid Signal", "Milan Subway Signal", "Andheri Fire Brigade Signal"],
        "nearby_infrastructure": {
            "bus_stops": ["Bandra Talkies", "Santacruz Depot", "Andheri Bazar", "Borivali SV Road"],
            "railway_stations": ["Bandra (0.4 km)", "Khar Road (0.3 km)", "Santacruz (0.4 km)", "Andheri (0.2 km)"],
            "metro": ["Line 2A (parallel along Link Road 1km west)", "Line 1 Andheri"],
            "hospitals": ["Bhabha Hospital Bandra", "Kokilaben Dhirubhai Ambani Hospital (1.5 km)"],
            "utilities": ["Western Suburbs Sewer Trunk", "BSES/Adani 33kV Distribution Lines"]
        }
    },
    {
        "id": "road_freeway_01",
        "name": "Eastern Freeway - Orange Gate CSMT to Chembur",
        "type": "Elevated Freeway",
        "category": "High-Speed Corridor",
        "lanes": 6,
        "speed_limit_kmh": 80,
        "avg_speed_kmh": 65,
        "traffic_status": "Normal",
        "traffic_level": "GREEN",
        "road_condition": "Good",
        "construction_status": "Operational (Thane extension planned)",
        "maintenance_status": "MMRDA Dedicated Toll & Freeway Ops",
        "known_incidents": 0,
        "data_provenance": "LIVE_CALIBRATED",
        "freshness": "Realtime (14s ago)",
        "coordinates": [
            [72.8440, 18.9400], # Orange Gate CSMT / P D'Mello Road
            [72.8520, 18.9750], # Mazgaon Dock Elevated Spans
            [72.8620, 19.0050], # Wadala Truck Terminal
            [72.8750, 19.0350], # Bhakti Park Elevated Flyover
            [72.8880, 19.0550]  # Chembur Panjarpol Junction
        ],
        "connected_road_ids": ["road_eeh_01", "road_sclr_01"],
        "nearby_intersections": ["Orange Gate Entry", "Wadala Monorail Crossing", "Panjarpol Chembur Junction"],
        "signals": ["Orange Gate Entry Gantry", "Panjarpol Exit Gantry"],
        "nearby_infrastructure": {
            "bus_stops": ["Wadala Depot", "Panjarpol Chembur"],
            "railway_stations": ["CSMT (1.0 km)", "Wadala Road (0.8 km)", "Govandi (1.2 km)"],
            "metro": ["Mumbai Monorail Wadala Hub"],
            "hospitals": ["KEM Hospital (2.0 km)", "Surana Sethia Hospital Chembur"],
            "utilities": ["Mumbai Port Trust Underground Bunkering Pipelines"]
        }
    }
]

# --- 2. UNDERGROUND UTILITIES ---
UTILITIES_DATA: Dict[str, List[Dict[str, Any]]] = {
    "water": [
        {
            "id": "util_wat_trunk_01",
            "name": "Bhandup Master Water Trunk Main (3000mm Tansa Pipeline)",
            "type": "Trunk Pipeline",
            "utility_type": "WATER",
            "depth_meters": -8.5,
            "diameter_mm": 3000,
            "material": "Mild Steel Polyurethane Coated",
            "pressure_bar": 6.8,
            "flow_rate_m3h": 42000,
            "status": "Optimal Operational",
            "upstream_source": "Bhandup Water Treatment Plant (Largest in Asia)",
            "downstream_zones": ["Worli Reservoir", "Malabar Hill Reservoir", "Parel Master Balancing Reservoir"],
            "coordinates": [
                [72.9380, 19.1550, -6.0], # Bhandup Complex
                [72.9250, 19.1200, -8.0], # Vikhroli Conduit
                [72.9020, 19.0850, -9.5], # Ghatkopar Balancing Node
                [72.8780, 19.0550, -8.5], # Chembur Junction
                [72.8550, 19.0200, -10.0], # Parel Reservoir feed
                [72.8120, 18.9600, -12.0]  # Malabar Hill Reservoir
            ],
            "connected_assets": ["Bhandup Chlorination Plant", "Ghatkopar Valve Chamber 4", "Malabar High Level Tank"],
            "data_provenance": "BMC_SCADA_LIVE",
            "freshness": "Realtime (3s ago)"
        },
        {
            "id": "util_wat_dist_02",
            "name": "Western Suburbs Distribution Feeder (1800mm)",
            "type": "Primary Feeder",
            "utility_type": "WATER",
            "depth_meters": -4.2,
            "diameter_mm": 1800,
            "material": "Ductile Iron",
            "pressure_bar": 4.2,
            "flow_rate_m3h": 18500,
            "status": "Optimal Operational",
            "upstream_source": "Veravali Reservoir Complex",
            "downstream_zones": ["Andheri West", "Juhu", "Bandra West", "Khar"],
            "coordinates": [
                [72.8680, 19.1280, -4.0], # Veravali Reservoir
                [72.8460, 19.1180, -4.5], # Andheri Metro crossing
                [72.8350, 19.0850, -4.2], # Santacruz West
                [72.8360, 19.0580, -4.0]  # Bandra Water Zone Tank
            ],
            "connected_assets": ["Veravali Pumping Station", "Andheri SV Road Valve Node 12", "Pali Hill Booster"],
            "data_provenance": "BMC_SCADA_LIVE",
            "freshness": "Realtime (5s ago)"
        },
        {
            "id": "util_wat_facility_01",
            "name": "Bhandup Water Treatment Complex",
            "type": "Treatment Facility",
            "utility_type": "WATER",
            "depth_meters": 0.0,
            "capacity_mld": 2810,
            "status": "Operational 100% capacity",
            "coordinates": [[72.9380, 19.1550, 0.0]],
            "connected_assets": ["util_wat_trunk_01", "Tansa Lake Inflow", "Bhatsa Dam Line"],
            "data_provenance": "BMC_AUTHORITATIVE",
            "freshness": "Realtime (1m ago)"
        },
        {
            "id": "util_wat_facility_02",
            "name": "Malabar Hill Hanging Gardens Reservoir",
            "type": "Balancing Reservoir",
            "utility_type": "WATER",
            "depth_meters": -5.0,
            "capacity_mld": 150,
            "status": "Operational - Structural Repair Scheduled",
            "coordinates": [[72.8120, 18.9600, -5.0]],
            "connected_assets": ["util_wat_trunk_01", "South Mumbai Gravity Lines"],
            "data_provenance": "BMC_AUTHORITATIVE",
            "freshness": "Realtime (1m ago)"
        }
    ],
    "sewer": [
        {
            "id": "util_sew_trunk_01",
            "name": "Worli-Dharavi Deep Sewerage Tunnel (MSDP Phase 2)",
            "type": "Deep Sewer Tunnel",
            "utility_type": "SEWER",
            "depth_meters": -24.0,
            "diameter_mm": 3200,
            "material": "Segmental Precast Concrete Lining",
            "flow_rate_m3h": 31000,
            "status": "Active Flow (72% load)",
            "upstream_source": "Dharavi Sewage Pumping Station",
            "downstream_zones": ["Worli Sewage Treatment Plant & Marine Outfall (3.5 km offshore)"],
            "coordinates": [
                [72.8550, 19.0400, -18.0], # Dharavi Pumping Station
                [72.8420, 19.0150, -22.0], # Dadar Prabhadevi Shaft
                [72.8250, 18.9980, -26.0], # Worli STP Inlet Shaft
                [72.7950, 18.9950, -32.0]  # Arabian Sea Deep Outfall Diffusers
            ],
            "connected_assets": ["Dharavi Wet Well", "Prabhadevi Drop Shaft 3", "Worli Water Reclamation Facility"],
            "data_provenance": "BMC_MSDP_SCADA",
            "freshness": "Realtime (10s ago)"
        },
        {
            "id": "util_sew_bandra_02",
            "name": "Bandra Reclamation Sewerage Tunnel",
            "type": "Gravity Sewer Collector",
            "utility_type": "SEWER",
            "depth_meters": -14.0,
            "diameter_mm": 2400,
            "material": "Reinforced Concrete Pipe",
            "flow_rate_m3h": 16500,
            "status": "Active Flow",
            "upstream_source": "Khar/Bandra West Trunk Network",
            "downstream_zones": ["Bandra Waste Water Treatment Facility & Subsea Outfall"],
            "coordinates": [
                [72.8360, 19.0700, -10.0], # Khar West
                [72.8350, 19.0550, -12.5], # Bandra Bazaar
                [72.8280, 19.0420, -15.0], # Bandra Reclamation STP
                [72.8050, 19.0400, -22.0]  # Mahim Bay Diffusers
            ],
            "connected_assets": ["Bandra West Manhole Cluster 14", "Bandra Outfall Pump Unit"],
            "data_provenance": "BMC_MSDP_SCADA",
            "freshness": "Realtime (15s ago)"
        }
    ],
    "drainage": [
        {
            "id": "util_drn_swd_01",
            "name": "BRIMSTOWAD Storm Water Trunk Drain - Love Grove Basin",
            "type": "Storm Water Drainage Network",
            "utility_type": "DRAINAGE",
            "depth_meters": -4.5,
            "dimensions": "4.5m x 3.0m Box Culvert",
            "discharge_capacity_cumecs": 140,
            "current_water_level_m": 0.45,
            "flood_risk_state": "GREEN (Low Tide Drainage Clear)",
            "coordinates": [
                [72.8420, 19.0100, -3.0], # Lower Parel Mill Area
                [72.8280, 19.0020, -4.0], # Gandhi Nagar Worli
                [72.8180, 18.9960, -5.0]  # Love Grove Pumping Station Sluice
            ],
            "connected_assets": ["Love Grove Storm Water Pumping Station (6 x 6000 LPS Pumps)", "Worli Nullah Sluice Gates"],
            "data_provenance": "BMC_SWD_SCADA",
            "freshness": "Realtime (2s ago)"
        },
        {
            "id": "util_drn_mithi_02",
            "name": "Mithi River Regulated Training Channel & Outfall",
            "type": "Major Flood Mitigation Channel",
            "utility_type": "DRAINAGE",
            "depth_meters": -2.0,
            "dimensions": "Open Regulated Channel 25m - 60m width",
            "discharge_capacity_cumecs": 450,
            "current_water_level_m": 1.2,
            "flood_risk_state": "GREEN",
            "coordinates": [
                [72.9050, 19.1250, 10.0], # Powai Lake Spillway discharge
                [72.8850, 19.0900, 4.0],  # Marol / Saki Naka
                [72.8680, 19.0680, 1.5],  # BKC Bridge & Mangrove Sanctuary
                [72.8450, 19.0480, 0.0]   # Mahim Creek / Bay Outfall
            ],
            "connected_assets": ["BKC Flood Retention Pond", "Mahim Causeway Tidal Regulators"],
            "data_provenance": "BMC_DISASTER_MGMT",
            "freshness": "Realtime (5s ago)"
        },
        {
            "id": "util_drn_milan_03",
            "name": "Milan Subway Flood Protection Deep Sump & Holding Tank",
            "type": "Underground Storm Holding Reservoir",
            "utility_type": "DRAINAGE",
            "depth_meters": -9.0,
            "capacity_liters": 20000000,
            "current_volume_liters": 1500000,
            "flood_risk_state": "GREEN",
            "coordinates": [
                [72.8420, 19.0880, -9.0]
            ],
            "connected_assets": ["Milan Subway High Capacity Dewatering Pumps (5 units)"],
            "data_provenance": "BMC_SWD_MONITORING",
            "freshness": "Realtime (1s ago)"
        }
    ],
    "electricity": [
        {
            "id": "util_elec_grid_01",
            "name": "Tata Power 220kV Underground Transmission Conduit",
            "type": "High Voltage Transmission",
            "utility_type": "ELECTRICITY",
            "depth_meters": -3.5,
            "voltage_kv": 220,
            "current_load_mva": 185,
            "capacity_mva": 250,
            "status": "Energized / Optimal",
            "substations": ["Trombay Thermal Receiving Station", "Dharavi 220kV Grid Substation", "Backbay 220kV Gas-Insulated Substation"],
            "coordinates": [
                [72.8980, 19.0050, -3.0], # Trombay
                [72.8600, 19.0450, -3.5], # Dharavi Substation
                [72.8350, 18.9950, -4.0], # Mahalaxmi Substation
                [72.8220, 18.9220, -3.5]  # Backbay GIS Substation
            ],
            "connected_assets": ["Dharavi GIS", "Backbay GIS", "Mahalaxmi Receiving Station"],
            "data_provenance": "SLDC_MAHARASHTRA_LIVE",
            "freshness": "Realtime (1s ago)"
        },
        {
            "id": "util_elec_bkc_02",
            "name": "Adani Electricity BKC Underground Smart Ring Main",
            "type": "Medium Voltage Distribution",
            "utility_type": "ELECTRICITY",
            "depth_meters": -2.8,
            "voltage_kv": 33,
            "current_load_mva": 62,
            "capacity_mva": 90,
            "status": "Energized / 100% Redundancy",
            "coordinates": [
                [72.8550, 19.0700, -2.8],
                [72.8650, 19.0660, -2.8],
                [72.8720, 19.0630, -2.8],
                [72.8620, 19.0580, -2.8],
                [72.8550, 19.0700, -2.8]
            ],
            "connected_assets": ["BKC Substation 1", "BKC Substation 2", "Jio Convention Centre Substation"],
            "data_provenance": "ADANI_SMART_GRID_LIVE",
            "freshness": "Realtime (2s ago)"
        }
    ],
    "telecom": [
        {
            "id": "util_tel_fiber_01",
            "name": "Mumbai Subsea Cable Landing Core Dark Fiber Loop",
            "type": "Core Optical Fiber Backbone",
            "utility_type": "TELECOM",
            "depth_meters": -2.2,
            "fiber_count": 576,
            "bandwidth_capacity_tbps": 400,
            "utilization_pct": 68.4,
            "status": "Active 99.999% SLA",
            "coordinates": [
                [72.8240, 19.0150, -2.0], # Prabhadevi Tata Comm Subsea Landing
                [72.8320, 18.9250, -2.2], # Nariman Point Gateway
                [72.8620, 19.0650, -2.5], # BKC Data Center Hub (Equinix/CtrlS)
                [72.8750, 19.1200, -2.2], # Chandivali / SEEPZ IT Zone
                [72.8240, 19.0150, -2.0]
            ],
            "connected_assets": ["Prabhadevi International Gateway", "BKC Carrier Meet-Me Room", "Chandivali Cloud Data Campus"],
            "data_provenance": "NLD_TELECOM_OPERATORS",
            "freshness": "Realtime (10s ago)"
        }
    ]
}

# --- 3. PUBLIC TRANSPORTATION ---
TRANSIT_DATA: Dict[str, Any] = {
    "metro_lines": [
        {
            "id": "metro_line_3",
            "name": "Metro Line 3 (Aqua Line) - Underground Corridor",
            "status": "Operational / Commissioned",
            "color": "#00A896",
            "type": "Underground Metro",
            "depth_meters": -22.0,
            "length_km": 33.5,
            "daily_ridership": 450000,
            "frequency_mins": 3.5,
            "stations": [
                {"name": "Cuffe Parade", "coords": [72.8190, 18.9100], "depth": -20},
                {"name": "Vidhan Bhavan", "coords": [72.8250, 18.9250], "depth": -22},
                {"name": "Churchgate", "coords": [72.8280, 18.9350], "depth": -24},
                {"name": "CSMT Underground", "coords": [72.8350, 18.9400], "depth": -25},
                {"name": "Girgaon", "coords": [72.8180, 18.9550], "depth": -22},
                {"name": "Worli", "coords": [72.8220, 18.9980], "depth": -21},
                {"name": "Siddhivinayak", "coords": [72.8320, 19.0180], "depth": -20},
                {"name": "Dharavi", "coords": [72.8520, 19.0480], "depth": -22},
                {"name": "BKC Metro Interchange", "coords": [72.8640, 19.0660], "depth": -26},
                {"name": "Santacruz Domestic Airport T1", "coords": [72.8550, 19.0900], "depth": -20},
                {"name": "CSMIA International Airport T2", "coords": [72.8750, 19.0980], "depth": -24},
                {"name": "SEEPZ Terminal", "coords": [72.8820, 19.1250], "depth": -18},
                {"name": "Aarey Depot", "coords": [72.8780, 19.1450], "depth": 0}
            ],
            "coordinates": [
                [72.8190, 18.9100, -20.0],
                [72.8250, 18.9250, -22.0],
                [72.8280, 18.9350, -24.0],
                [72.8350, 18.9400, -25.0],
                [72.8180, 18.9550, -22.0],
                [72.8220, 18.9980, -21.0],
                [72.8320, 19.0180, -20.0],
                [72.8520, 19.0480, -22.0],
                [72.8640, 19.0660, -26.0],
                [72.8550, 19.0900, -20.0],
                [72.8750, 19.0980, -24.0],
                [72.8820, 19.1250, -18.0],
                [72.8780, 19.1450, 0.0]
            ],
            "active_trains": [
                {"train_id": "M3-TRN-101", "speed_kmh": 64, "occupancy_pct": 78, "current_station": "BKC", "next_station": "Domestic Airport T1", "direction": "Northbound"},
                {"train_id": "M3-TRN-104", "speed_kmh": 58, "occupancy_pct": 62, "current_station": "Worli", "next_station": "Girgaon", "direction": "Southbound"},
                {"train_id": "M3-TRN-108", "speed_kmh": 70, "occupancy_pct": 85, "current_station": "CSMT", "next_station": "Churchgate", "direction": "Southbound"}
            ],
            "data_provenance": "MMRC_TRAIN_SUPERVISION_LIVE",
            "freshness": "Realtime (2s ago)"
        },
        {
            "id": "metro_line_1",
            "name": "Metro Line 1 (Blue Line) - Versova - Andheri - Ghatkopar",
            "status": "Operational",
            "color": "#0284C7",
            "type": "Elevated Metro",
            "depth_meters": 14.0,
            "length_km": 11.4,
            "daily_ridership": 420000,
            "frequency_mins": 3.0,
            "stations": [
                {"name": "Versova", "coords": [72.8210, 19.1310], "depth": 14},
                {"name": "DN Nagar", "coords": [72.8350, 19.1260], "depth": 14},
                {"name": "Azad Nagar", "coords": [72.8420, 19.1230], "depth": 14},
                {"name": "Andheri West Interchange", "coords": [72.8480, 19.1200], "depth": 16},
                {"name": "Western Express Highway", "coords": [72.8560, 19.1155], "depth": 16},
                {"name": "Chakala (JB Nagar)", "coords": [72.8680, 19.1110], "depth": 14},
                {"name": "Airport Road", "coords": [72.8750, 19.1080], "depth": 14},
                {"name": "Marol Naka", "coords": [72.8830, 19.1050], "depth": 14},
                {"name": "Saki Naka", "coords": [72.8900, 19.1020], "depth": 14},
                {"name": "Asalpha", "coords": [72.8990, 19.0960], "depth": 14},
                {"name": "Jagruti Nagar", "coords": [72.9040, 19.0910], "depth": 14},
                {"name": "Ghatkopar Station Interchange", "coords": [72.9090, 19.0860], "depth": 16}
            ],
            "coordinates": [
                [72.8210, 19.1310, 14.0],
                [72.8350, 19.1260, 14.0],
                [72.8420, 19.1230, 14.0],
                [72.8480, 19.1200, 16.0],
                [72.8560, 19.1155, 16.0],
                [72.8680, 19.1110, 14.0],
                [72.8750, 19.1080, 14.0],
                [72.8830, 19.1050, 14.0],
                [72.8900, 19.1020, 14.0],
                [72.8990, 19.0960, 14.0],
                [72.9040, 19.0910, 14.0],
                [72.9090, 19.0860, 16.0]
            ],
            "active_trains": [
                {"train_id": "M1-TRN-04", "speed_kmh": 48, "occupancy_pct": 92, "current_station": "Andheri", "next_station": "WEH", "direction": "Eastbound"},
                {"train_id": "M1-TRN-09", "speed_kmh": 52, "occupancy_pct": 80, "current_station": "Saki Naka", "next_station": "Marol Naka", "direction": "Westbound"}
            ],
            "data_provenance": "MMOPL_SCADA_LIVE",
            "freshness": "Realtime (2s ago)"
        },
        {
            "id": "metro_line_2a_7",
            "name": "Metro Line 2A & Line 7 (Yellow/Red Lines) - Dahisar to Andheri",
            "status": "Operational",
            "color": "#EAB308",
            "type": "Elevated Metro",
            "depth_meters": 15.0,
            "length_km": 35.0,
            "daily_ridership": 280000,
            "frequency_mins": 5.0,
            "stations": [
                {"name": "Dahisar East", "coords": [72.8630, 19.2550], "depth": 15},
                {"name": "Borivali National Park", "coords": [72.8610, 19.2320], "depth": 15},
                {"name": "Kandivali East", "coords": [72.8590, 19.2080], "depth": 15},
                {"name": "Goregaon East / Aarey", "coords": [72.8570, 19.1650], "depth": 15},
                {"name": "Gundavali (WEH Interchange)", "coords": [72.8560, 19.1155], "depth": 16}
            ],
            "coordinates": [
                [72.8630, 19.2550, 15.0],
                [72.8610, 19.2320, 15.0],
                [72.8590, 19.2080, 15.0],
                [72.8570, 19.1650, 15.0],
                [72.8560, 19.1155, 16.0]
            ],
            "active_trains": [
                {"train_id": "M7-TRN-21", "speed_kmh": 56, "occupancy_pct": 65, "current_station": "Goregaon East", "next_station": "Gundavali", "direction": "Southbound"}
            ],
            "data_provenance": "MMMOCL_LIVE",
            "freshness": "Realtime (4s ago)"
        }
    ],
    "suburban_railway": [
        {
            "id": "rail_western_line",
            "name": "Western Railway Suburban Trunk Corridor",
            "status": "Operational (Lifeline of Mumbai)",
            "color": "#DC2626",
            "type": "Heavy Suburban Rail (Quad Track 25kV AC)",
            "daily_ridership": 3500000,
            "stations": [
                {"name": "Churchgate Terminus", "coords": [72.8277, 18.9355]},
                {"name": "Marine Lines", "coords": [72.8250, 18.9440]},
                {"name": "Charni Road", "coords": [72.8180, 18.9515]},
                {"name": "Grant Road", "coords": [72.8140, 18.9630]},
                {"name": "Mumbai Central", "coords": [72.8180, 18.9690]},
                {"name": "Mahalaxmi", "coords": [72.8235, 18.9830]},
                {"name": "Lower Parel", "coords": [72.8300, 18.9950]},
                {"name": "Prabhadevi", "coords": [72.8340, 19.0120]},
                {"name": "Dadar WR Junction", "coords": [72.8425, 19.0180]},
                {"name": "Matunga Road", "coords": [72.8450, 19.0300]},
                {"name": "Mahim Junction", "coords": [72.8420, 19.0410]},
                {"name": "Bandra Terminus & Station", "coords": [72.8400, 19.0550]},
                {"name": "Khar Road", "coords": [72.8400, 19.0700]},
                {"name": "Santacruz", "coords": [72.8410, 19.0830]},
                {"name": "Vile Parle", "coords": [72.8430, 19.0990]},
                {"name": "Andheri Super Hub", "coords": [72.8465, 19.1197]},
                {"name": "Jogeshwari", "coords": [72.8480, 19.1360]},
                {"name": "Goregaon", "coords": [72.8480, 19.1650]},
                {"name": "Malad", "coords": [72.8490, 19.1860]},
                {"name": "Kandivali", "coords": [72.8510, 19.2050]},
                {"name": "Borivali Major Terminus", "coords": [72.8567, 19.2307]}
            ],
            "coordinates": [
                [72.8277, 18.9355],
                [72.8250, 18.9440],
                [72.8180, 18.9515],
                [72.8140, 18.9630],
                [72.8180, 18.9690],
                [72.8235, 18.9830],
                [72.8300, 18.9950],
                [72.8340, 19.0120],
                [72.8425, 19.0180],
                [72.8450, 19.0300],
                [72.8420, 19.0410],
                [72.8400, 19.0550],
                [72.8400, 19.0700],
                [72.8410, 19.0830],
                [72.8430, 19.0990],
                [72.8465, 19.1197],
                [72.8480, 19.1360],
                [72.8480, 19.1650],
                [72.8490, 19.1860],
                [72.8510, 19.2050],
                [72.8567, 19.2307]
            ],
            "active_trains": [
                {"train_id": "WR-FAST-90214", "type": "12-Car AC EMU Fast Local", "speed_kmh": 85, "current_location": [72.8430, 19.0990], "next_stop": "Andheri", "status": "On-Time (+1m)", "occupancy": "Super Dense Crush Load (125%)"},
                {"train_id": "WR-SLOW-90432", "type": "15-Car Non-AC Slow Local", "speed_kmh": 55, "current_location": [72.8425, 19.0180], "next_stop": "Matunga Road", "status": "On-Time", "occupancy": "Dense (95%)"}
            ],
            "data_provenance": "CRIS_NTES_INDIAN_RAILWAYS",
            "freshness": "Realtime (3s ago)"
        },
        {
            "id": "rail_central_line",
            "name": "Central Railway Suburban Trunk Corridor (CSMT to Thane/Kalyan)",
            "status": "Operational",
            "color": "#B91C1C",
            "type": "Heavy Suburban Rail (Hexa Track 25kV AC)",
            "daily_ridership": 4200000,
            "stations": [
                {"name": "CSMT UNESCO World Heritage Terminus", "coords": [72.8355, 18.9400]},
                {"name": "Masjid", "coords": [72.8390, 18.9510]},
                {"name": "Sandhurst Road", "coords": [72.8400, 18.9610]},
                {"name": "Byculla", "coords": [72.8350, 18.9770]},
                {"name": "Currey Road", "coords": [72.8330, 18.9950]},
                {"name": "Parel", "coords": [72.8370, 19.0080]},
                {"name": "Dadar CR Central Hub", "coords": [72.8430, 19.0185]},
                {"name": "Matunga", "coords": [72.8550, 19.0280]},
                {"name": "Sion", "coords": [72.8620, 19.0400]},
                {"name": "Kurla Junction", "coords": [72.8790, 19.0650]},
                {"name": "Vidyavihar", "coords": [72.8950, 19.0780]},
                {"name": "Ghatkopar Major Interchange", "coords": [72.9090, 19.0860]},
                {"name": "Vikhroli", "coords": [72.9280, 19.1100]},
                {"name": "Kanjurmarg", "coords": [72.9350, 19.1250]},
                {"name": "Bhandup", "coords": [72.9390, 19.1450]},
                {"name": "Nahur", "coords": [72.9450, 19.1580]},
                {"name": "Mulund", "coords": [72.9550, 19.1720]},
                {"name": "Thane Mega Junction", "coords": [72.9750, 19.1860]}
            ],
            "coordinates": [
                [72.8355, 18.9400],
                [72.8390, 18.9510],
                [72.8400, 18.9610],
                [72.8350, 18.9770],
                [72.8330, 18.9950],
                [72.8370, 19.0080],
                [72.8430, 19.0185],
                [72.8550, 19.0280],
                [72.8620, 19.0400],
                [72.8790, 19.0650],
                [72.8950, 19.0780],
                [72.9090, 19.0860],
                [72.9280, 19.1100],
                [72.9350, 19.1250],
                [72.9390, 19.1450],
                [72.9450, 19.1580],
                [72.9550, 19.1720],
                [72.9750, 19.1860]
            ],
            "active_trains": [
                {"train_id": "CR-FAST-T105", "type": "12-Car Fast Local", "speed_kmh": 78, "current_location": [72.8790, 19.0650], "next_stop": "Ghatkopar", "status": "On-Time", "occupancy": "Dense (98%)"}
            ],
            "data_provenance": "CRIS_NTES_INDIAN_RAILWAYS",
            "freshness": "Realtime (3s ago)"
        }
    ],
    "best_buses": [
        {
            "route_no": "A-115 AC",
            "name": "Electric AC Express: Chhatrapati Shivaji Maharaj Terminus (CSMT) - NCPA Nariman Point",
            "fleet_type": "Olectra Electric AC Low-Floor",
            "frequency_mins": 8,
            "active_buses": [
                {"bus_id": "MH-01-EA-4210", "speed_kmh": 26, "occupancy": 38, "current_coord": [72.8250, 18.9320], "destination": "NCPA Nariman Point"}
            ],
            "data_provenance": "CHALO_BEST_LIVE_GPS",
            "freshness": "Realtime (5s ago)"
        },
        {
            "route_no": "Route 83",
            "name": "Santacruz Station West - Andheri SEEPZ",
            "fleet_type": "Tata CNG Bus",
            "frequency_mins": 10,
            "active_buses": [
                {"bus_id": "MH-02-BG-1892", "speed_kmh": 18, "occupancy": 52, "current_coord": [72.8720, 19.1180], "destination": "SEEPZ Bus Station"}
            ],
            "data_provenance": "CHALO_BEST_LIVE_GPS",
            "freshness": "Realtime (6s ago)"
        },
        {
            "route_no": "Route 332",
            "name": "Kurla Station West - Andheri Agarkar Chowk",
            "fleet_type": "Electric Double Decker AC",
            "frequency_mins": 12,
            "active_buses": [
                {"bus_id": "MH-01-EE-8801", "speed_kmh": 22, "occupancy": 68, "current_coord": [72.8680, 19.0780], "destination": "Andheri Station"}
            ],
            "data_provenance": "CHALO_BEST_LIVE_GPS",
            "freshness": "Realtime (4s ago)"
        }
    ]
}

# --- 4. INCIDENTS, ROAD DAMAGE & ALERTS ---
INCIDENTS_DATA: List[Dict[str, Any]] = [
    {
        "id": "inc_pothole_01",
        "category": "Road Damage / Pothole Cluster",
        "severity": "CRITICAL",
        "severity_score": 88,
        "title": "Severe Pothole Cluster on JVLR Westbound Carriage near SEEPZ",
        "location_name": "Jogeshwari-Vikhroli Link Road near Gate 1",
        "coordinates": [72.8850, 19.1300],
        "related_road_id": "road_jvlr_01",
        "timestamp": "2026-09-02T03:15:00+05:30",
        "status": "In Progress (Road Repair Van Dispatched)",
        "source": "BMC 24x7 Citizen Pothole App (Auto-GeoTagged)",
        "reported_by": "MahaTwin Citizen Telemetry",
        "image_url": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=60",
        "work_order_id": "BMC-HW-2026-8821",
        "estimated_resolution": "2026-09-02T11:00:00+05:30",
        "data_provenance": "LIVE_VERIFIED",
        "freshness": "Realtime (2m ago)"
    },
    {
        "id": "inc_waterlog_02",
        "category": "Waterlogging Risk / Sensor Alert",
        "severity": "WARNING",
        "severity_score": 65,
        "title": "Water Level Rise Warning at Milan Subway Sump",
        "location_name": "Milan Subway Underpass, Santacruz",
        "coordinates": [72.8420, 19.0880],
        "related_road_id": "road_sv_road_01",
        "timestamp": "2026-09-02T03:40:00+05:30",
        "status": "Monitored (Automatic Dewatering Pumps Active - 3/5 running)",
        "source": "BMC SWD IoT Acoustic Level Sensor MS-02",
        "reported_by": "Disaster Management Cell (BMC HQ)",
        "image_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=600&auto=format&fit=crop&q=60",
        "work_order_id": "SWD-PUMP-AUTO-409",
        "estimated_resolution": "Continuous Monitoring",
        "data_provenance": "LIVE_IOT_SENSOR",
        "freshness": "Realtime (30s ago)"
    },
    {
        "id": "inc_construct_03",
        "category": "Construction Lane Diversion",
        "severity": "MODERATE",
        "severity_score": 45,
        "title": "Metro Line 4 Pier Gantry Launching - Right 2 Lanes Diverted",
        "location_name": "LBS Marg near Phoenix Marketcity Kurla",
        "coordinates": [72.8980, 19.0910],
        "related_road_id": "road_lbs_01",
        "timestamp": "2026-08-30T00:00:00+05:30",
        "status": "Active Work Zone (MMRDA Traffic Marshal Stationed)",
        "source": "Mumbai Traffic Police Advisory (MTP)",
        "reported_by": "MMRDA Metro Division",
        "work_order_id": "MMRDA-M4-PKG02",
        "estimated_resolution": "2026-09-15T23:59:00+05:30",
        "data_provenance": "AUTHORITATIVE_MTP",
        "freshness": "Daily Verified"
    },
    {
        "id": "inc_signal_04",
        "category": "Damaged Infrastructure / Signal Fault",
        "severity": "HIGH",
        "severity_score": 75,
        "title": "Adaptive Traffic Signal Controller Fault - Kalanagar Eastbound",
        "location_name": "Kalanagar Junction, Bandra East",
        "coordinates": [72.8498, 19.0689],
        "related_road_id": "road_weh_01",
        "timestamp": "2026-09-02T03:52:00+05:30",
        "status": "Traffic Wardens Directing / Technician On-Site",
        "source": "Smart City ITMS Central Health Watchdog",
        "reported_by": "MTP ITMS Cell",
        "work_order_id": "ITMS-SIG-819",
        "estimated_resolution": "2026-09-02T05:30:00+05:30",
        "data_provenance": "LIVE_ITMS_TELEMETRY",
        "freshness": "Realtime (4m ago)"
    },
    {
        "id": "inc_pipe_05",
        "category": "Utility Damage / Water Pipe Leak",
        "severity": "MODERATE",
        "severity_score": 50,
        "title": "1200mm Secondary Supply Pipeline Gasket Weepage",
        "location_name": "Dr. Ambedkar Road near Lalbaug Flyover",
        "coordinates": [72.8360, 18.9920],
        "related_road_id": "road_lbs_01",
        "timestamp": "2026-09-01T21:00:00+05:30",
        "status": "Scheduled Night Maintenance (No Supply Interruption)",
        "source": "BMC Hydraulic Engineering Dept Sensor HE-LB-4",
        "reported_by": "BMC F/South Ward Office",
        "work_order_id": "BMC-HE-2026-119",
        "estimated_resolution": "2026-09-02T06:00:00+05:30",
        "data_provenance": "BMC_HYDRAULIC_SCADA",
        "freshness": "Realtime (15m ago)"
    }
]

# --- 5. ENVIRONMENTAL & AQI SENSORS ---
ENVIRONMENT_DATA: Dict[str, Any] = {
    "aqi_stations": [
        {"id": "aqi_bkc", "name": "BKC Central (SAFAR Continuous Station)", "coordinates": [72.8640, 19.0650], "aqi": 164, "category": "Moderate", "pm25": 68.2, "pm10": 142.0, "no2": 45.1, "temp_c": 28.4, "humidity_pct": 82, "status": "LIVE"},
        {"id": "aqi_colaba", "name": "Colaba Coastal (Navy Nagar)", "coordinates": [72.8180, 18.9080], "aqi": 72, "category": "Satisfactory", "pm25": 24.5, "pm10": 58.0, "no2": 18.0, "temp_c": 27.9, "humidity_pct": 86, "status": "LIVE"},
        {"id": "aqi_andheri", "name": "Andheri West SV Road", "coordinates": [72.8390, 19.1180], "aqi": 182, "category": "Moderate", "pm25": 78.4, "pm10": 168.0, "no2": 52.3, "temp_c": 29.1, "humidity_pct": 79, "status": "LIVE"},
        {"id": "aqi_borivali", "name": "Borivali East SGNP Edge", "coordinates": [72.8680, 19.2310], "aqi": 88, "category": "Satisfactory", "pm25": 31.0, "pm10": 72.0, "no2": 21.4, "temp_c": 27.2, "humidity_pct": 88, "status": "LIVE"},
        {"id": "aqi_chembur", "name": "Chembur Industrial Zone", "coordinates": [72.8950, 19.0550], "aqi": 210, "category": "Poor", "pm25": 94.2, "pm10": 198.0, "no2": 64.8, "temp_c": 29.5, "humidity_pct": 77, "status": "LIVE"},
        {"id": "aqi_worli", "name": "Worli Sea Face", "coordinates": [72.8160, 19.0120], "aqi": 95, "category": "Satisfactory", "pm25": 34.0, "pm10": 80.0, "no2": 26.1, "temp_c": 28.0, "humidity_pct": 85, "status": "LIVE"}
    ],
    "flood_risk_hotspots": [
        {"id": "fld_milan", "name": "Milan Subway Santacruz", "coordinates": [72.8420, 19.0880], "risk_level": "HIGH", "tide_sensitivity": "Moderate", "mitigation_installed": "20ML Holding Tank + 5 Dewatering Pumps", "status": "CLEAR"},
        {"id": "fld_hindmata", "name": "Hindmata Flyover Underpass, Dadar", "coordinates": [72.8420, 19.0120], "risk_level": "HIGH", "tide_sensitivity": "High", "mitigation_installed": "Pramod Mahajan Park Holding Pond", "status": "CLEAR"},
        {"id": "fld_gandhi", "name": "Gandhi Market King's Circle, Sion", "coordinates": [72.8600, 19.0340], "risk_level": "HIGH", "tide_sensitivity": "Very High", "mitigation_installed": "High-capacity SWD pumps", "status": "CLEAR"},
        {"id": "fld_kurla_kamani", "name": "Kurla Kamani / Bail Bazar", "coordinates": [72.8820, 19.0720], "risk_level": "MODERATE", "tide_sensitivity": "Mithi Inflow Dependent", "mitigation_installed": "Channel Retaining Wall", "status": "CLEAR"}
    ]
}

# --- 6. CIVIC & EMERGENCY FACILITIES ---
CIVIC_FACILITIES: List[Dict[str, Any]] = [
    {
        "id": "civ_hosp_kem",
        "name": "KEM Hospital & Seth GS Medical College",
        "category": "Tertiary Apex Public Hospital",
        "type": "HOSPITAL",
        "beds": 2250,
        "emergency_trauma_level": "Level 1 Apex Trauma Centre",
        "icu_beds_available": 14,
        "coordinates": [72.8415, 19.0035],
        "connected_roads": ["road_lbs_01", "Dr. E Borges Road"],
        "nearby_utilities": ["Parel Trunk Water Line", "Dedicated Tata Power Hospital Feeder Grid"],
        "data_provenance": "BMC_HEALTH_LIVE",
        "freshness": "Realtime (5m ago)"
    },
    {
        "id": "civ_hosp_lilavati",
        "name": "Lilavati Hospital & Research Centre",
        "category": "Multi-Speciality Quaternary Hospital",
        "type": "HOSPITAL",
        "beds": 320,
        "emergency_trauma_level": "Level 1 Trauma & Cardiac",
        "icu_beds_available": 6,
        "coordinates": [72.8320, 19.0515],
        "connected_roads": ["road_bwsl_01", "road_sv_road_01"],
        "nearby_utilities": ["Bandra Feeder Main", "High-Priority Telecom Dark Fiber"],
        "data_provenance": "LILAVATI_HEALTH_LIVE",
        "freshness": "Realtime (10m ago)"
    },
    {
        "id": "civ_hosp_bombay",
        "name": "Bombay Hospital & Medical Research Centre",
        "category": "Apex Super Speciality Hospital",
        "type": "HOSPITAL",
        "beds": 830,
        "emergency_trauma_level": "Level 1 Emergency",
        "icu_beds_available": 11,
        "coordinates": [72.8285, 18.9385],
        "connected_roads": ["road_marine_drive_01", "New Marine Lines"],
        "nearby_utilities": ["South Mumbai High Pressure Water Line"],
        "data_provenance": "BOMBAY_HOSP_LIVE",
        "freshness": "Realtime (12m ago)"
    },
    {
        "id": "civ_fire_hq",
        "name": "Mumbai Fire Brigade Headquarters & Control Room",
        "category": "Emergency Command HQ",
        "type": "FIRE_STATION",
        "fleet_units": 18,
        "turnout_time_mins": 3.5,
        "coordinates": [72.8335, 18.9765],
        "connected_roads": ["Byculla Road", "road_lbs_01"],
        "nearby_utilities": ["High-capacity dedicated fire hydrants"],
        "data_provenance": "MFB_DISPATCH_LIVE",
        "freshness": "Realtime (1s ago)"
    },
    {
        "id": "civ_police_hq",
        "name": "Mumbai Police Commissionerate & CCTV Command Center",
        "category": "Law Enforcement & Surveillance HQ",
        "type": "POLICE_HQ",
        "active_cctv_feeds": 7500,
        "coordinates": [72.8340, 18.9460],
        "connected_roads": ["road_marine_drive_01", "LT Marg"],
        "nearby_utilities": ["Encrypted Police Optical WAN"],
        "data_provenance": "MUMBAI_POLICE_ITMS",
        "freshness": "Realtime (1s ago)"
    }
]

# --- 7. 4D TEMPORAL SCENARIOS ---
TEMPORAL_STATES: Dict[str, Any] = {
    "historical_2020": {
        "year": 2020,
        "title": "Historical 2020: Baseline Pre-Coastal Road",
        "description": "Mumbai baseline prior to Coastal Road reclamation, Metro Line 3 tunneling active underground, Metro 2A/7 in civil construction stage.",
        "coastal_road_status": "Reclamation & Seawall Construction (32% complete)",
        "metro_line_3_status": "TBM Tunneling Stage (17 TBMs active under South Mumbai)",
        "avg_peak_commute_mins": 74,
        "air_quality_avg_aqi": 185
    },
    "historical_2023": {
        "year": 2023,
        "title": "Historical 2023: Undersea Tunnel Breakthrough & Metro 2A/7 Launch",
        "description": "Girgaon twin undersea road tunnels excavated, Metro Line 2A & 7 fully open to public, BWSL integration ramps progressing.",
        "coastal_road_status": "Twin Undersea Tunnels Completed (88% overall project)",
        "metro_line_3_status": "Track laying and sub-station electrification",
        "avg_peak_commute_mins": 62,
        "air_quality_avg_aqi": 158
    },
    "live_2026": {
        "year": 2026,
        "title": "LIVE Real-Time Digital Twin (Operational)",
        "description": "Active smart city operations, Phase 1 Coastal Road connected to BWSL, Metro 3 Aqua Line Phase 1 & 2 operational, live IoT water SCADA & dynamic traffic controllers.",
        "coastal_road_status": "Fully Operational (8 lanes with SCADA monitoring)",
        "metro_line_3_status": "Fully Operational carrying 450k daily commuters",
        "avg_peak_commute_mins": 44,
        "air_quality_avg_aqi": 142
    },
    "future_2028": {
        "year": 2028,
        "title": "Simulated Future 2028: Multi-Modal Metro Network & Bullet Train",
        "description": "Simulated scenario with Metro Lines 4, 6, and 11 fully integrated, Mumbai-Ahmedabad High-Speed Rail underground BKC terminal operational, Coastal Road North extension to Versova.",
        "coastal_road_status": "Phase 2 Versova Extension Operational",
        "metro_line_3_status": "Integrated with Metro 6 and Bullet Train Hub",
        "avg_peak_commute_mins": 31,
        "air_quality_avg_aqi": 110
    },
    "future_2030": {
        "year": 2030,
        "title": "Simulated Future 2030: Zero-Emission Transit & Climate Resilience",
        "description": "100% electrified public transport bus fleet, BRIMSTOWAD 2.0 automated tidal surge gates at Mithi and Love Grove, smart grid micro-turbines along coastal seawall.",
        "coastal_road_status": "Autonomous EV dedicated lanes enabled",
        "metro_line_3_status": "Continuous AI-optimized signaling (CBTC 90s headway)",
        "avg_peak_commute_mins": 24,
        "air_quality_avg_aqi": 82
    }
}


# This repository ships a demonstrator dataset, not a licensed municipal feed.
# Keep the label at the source of truth so an API or websocket consumer cannot
# accidentally present fixtures as operational data.
def _mark_bundled_data_as_sample(value: Any) -> None:
    if isinstance(value, dict):
        if "data_provenance" in value:
            value["data_provenance"] = "SAMPLE_BUNDLED_DATA"
        if "freshness" in value:
            value["freshness"] = "Bundled sample — not a live feed"
        if value.get("status") == "LIVE":
            value["status"] = "SAMPLE"
        for nested in value.values():
            _mark_bundled_data_as_sample(nested)
    elif isinstance(value, list):
        for nested in value:
            _mark_bundled_data_as_sample(nested)


for _dataset in (ROADS_DATA, UTILITIES_DATA, TRANSIT_DATA, INCIDENTS_DATA, ENVIRONMENT_DATA, CIVIC_FACILITIES):
    _mark_bundled_data_as_sample(_dataset)

TEMPORAL_STATES["live_2026"]["title"] = "Current Demonstration State (SIMULATED)"
TEMPORAL_STATES["live_2026"]["description"] = (
    "Current-time simulation using bundled Mumbai demonstration data; no external live feed is configured."
)
