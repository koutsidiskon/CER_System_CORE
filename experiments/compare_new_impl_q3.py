"""
Compare new implementation vs Direct and Fixed-Time quarantine.
Usage:
  python compare_new_impl.py

Edit the DATA section to plug in your actual results.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# ==================== DATA (EDIT THESE) ====================
# Quarantine buffer sizes (seconds) used in your runs
QUARANTINE_TIMES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]

# Data for multiple datasets
# Each dataset has metrics for three implementations: Direct, Fixed-Time, Individual per event
# Metrics: num_results, num_drops, exec_time, avg_detection_delay
IMPLEMENTATIONS = ["Direct", "Fixed-Time", "jump_and_decay", "max", "Individual per event", "Sorted"]

# Color scheme for consistent coloring across all plots
COLORS = {
    "Direct": "#1f77b4",  
    "Fixed-Time": "#ff7f0e",  
    "jump_and_decay": "#2ca02c",  
    "max": "#d62728",  
    "Individual per event": "#9467bd",  
    "Sorted": "#8c564b",  
    "BoundedWaitTimePolicy": "#e377c2", 
    "NewFixedTimePolicy": "#7f7f7f",  
    "WaitFixedTimePolicy": "#bcbd22",  
}

DATASETS = {
    "Fires": {
        "Direct": {
            "num_results": [23,23,23,23,23,23,23,23,23,23,23,23,23,23,23],
            "num_drops":   [79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434],
            "exec_time":   [9.90, 9.85, 9.87, 9.84, 9.86, 9.79, 9.84, 9.79, 9.83, 9.80, 9.86, 9.74, 9.57, 9.66, 9.76],
            "avg_detection_delay": [240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [44, 44, 44, 44, 44, 44, 44, 44, 46, 46, 46, 46, 46, 46, 46],
            "num_drops":   [14524, 14519, 14501, 14459, 14396, 14241, 11085, 8213, 4512, 1574, 472, 175, 75, 34, 24],
            "exec_time":   [10.59, 10.59, 10.53, 10.73, 10.63, 10.52, 10.57, 10.65, 10.79, 10.85, 10.75, 11.37, 10.67, 10.84, 10.72],
            "avg_detection_delay": [216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay": [75.91181, 75.91181, 75.91181, 75.91181, 75.91181, 75.91181, 75.91181, 75.91181, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617],
            "p95_detection_delay": [300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0]
        },
        "jump_and_decay": {
            "num_results": [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46], 
            "num_drops": [130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 111, 55, 34, 24], 
            "exec_time": [9.45, 9.31, 9.44, 9.47, 9.40, 11.07, 9.66, 10.07, 9.60, 10.01, 10.06, 9.46, 10.06, 9.70, 9.46],
            "avg_detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay": [80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617],
            "p95_detection_delay": [360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0]
        },
        "max": {
            "num_results": [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46], 
            "num_drops": [131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 112, 55, 34, 24], 
            "exec_time": [9.72, 9.34, 9.25, 9.68, 9.16, 9.08, 9.01, 9.15, 9.13, 9.24, 9.07, 9.07, 9.12, 9.14, 9.17],
            "avg_detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay": [80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617],
            "p95_detection_delay": [360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0]
        },
        "Individual per event": {
            'num_results': [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46],
            'num_drops': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 88, 52, 33, 24],
            "exec_time":   [9.60, 9.96, 9.35, 9.88, 9.42, 9.78, 9.94, 9.25, 9.90, 9.30, 9.36, 9.06, 9.38, 9.13, 9.86],
            "avg_detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay": [80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617, 80.1617],
            "p95_detection_delay": [360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0]
        },
        "Sorted": {
            "num_results": [46,46,46,46,46,46,46,46,46,46,46,46,46,46,46],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [],
            "avg_detection_delay": [],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [265,265,265,265,265,265,265,265,265,265,265,265,265,265,265],
            "num_drops":   [336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293],
            "exec_time":   [12.66, 12.44, 12.50, 12.98, 12.55, 12.87, 13.13, 12.65, 12.72, 12.81, 12.99, 12.80, 12.90, 13.09, 12.72],
            "avg_detection_delay": [0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [282, 282, 282, 282, 282, 282, 316, 341, 399, 440, 473, 487, 492, 493, 493],
            "num_drops":   [313826, 313826, 313826, 313826, 313826, 313826, 274143, 215379, 126483, 60387, 21780, 7209, 2342, 631, 140],
            "exec_time":   [12.84, 12.56, 12.76, 12.50, 12.54, 12.57, 12.64, 12.75, 13.07, 13.50, 13.30, 13.34, 13.55, 13.37, 13.12],
            "avg_detection_delay": [6.17021, 6.17021, 6.17021, 6.17021, 6.17021, 6.17021, 45.00000, 79.17889, 256.99248, 480.81818, 809.04863, 1044.39425, 1203.65854, 1252.08925, 1252.08925],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay": [26.74173, 26.74173, 26.74173, 26.74173, 26.74173, 26.74173, 135.1476, 190.62923, 545.91578, 945.07973, 1561.99449, 2077.79133, 2598.74947, 2809.5912, 2809.5912],
            "p95_detection_delay": [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 360.0, 540.0, 1440.0, 2520.0, 4740.0, 5640.0, 6300.0, 6780.0, 6780.0]
        },
        "jump_and_decay": {
            "num_results": [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493], 
            "num_drops": [147, 147, 147, 147, 147, 147, 147, 141, 141, 135, 135, 117, 103, 74, 58], 
            "exec_time": [11.67, 11.69, 11.67, 11.74, 12.13, 11.95, 12.33, 11.94, 11.78, 11.83, 12.48, 12.37, 12.41, 11.89, 11.55],
            "avg_detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1251.83579, 1252.08925, 1252.08925],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay": [2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912],
            "p95_detection_delay": [6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0]
        },
        "max": {
            "num_results": [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493], 
            "num_drops": [148, 148, 148, 148, 148, 148, 148, 142, 142, 136, 136, 118, 104, 77, 58], 
            "exec_time": [12.16, 12.15, 12.14, 12.18, 12.23, 11.87, 12.07, 12.13, 12.16, 12.08, 12.23, 12.25, 12.25, 12.18, 12.25],
            "avg_detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay": [2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912],
            "p95_detection_delay": [6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0]
        },
        "Individual per event": {
            'num_results': [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493],
            'num_drops': [33, 33, 33, 33, 33, 33, 33, 29, 29, 17, 17, 17, 17, 17, 17],
            "exec_time":   [12.02, 12.19, 12.27, 11.56, 12.21, 12.28, 12.25, 11.63, 12.08, 12.01, 11.56, 11.90, 11.90, 11.57, 11.33],
            "avg_detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay": [2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912, 2809.5912],
            "p95_detection_delay": [6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0, 6780.0]
        },
        "Sorted": {
            "num_results": [493,493,493,493,493,493,493,493,493,493,493,493,493,493,493],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [],
            "avg_detection_delay": [],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            "num_drops":   [1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280],
            "exec_time":   [14.76, 14.62, 14.38, 14.68, 14.52, 14.82, 14.60, 14.41, 14.33, 14.62, 14.29, 14.93, 14.61, 14.35, 14.60],
            "avg_detection_delay": [13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [1314, 1314, 1317, 1318, 1324, 1375, 1446, 1515, 1618, 2012, 2392, 2926, 3656, 3849, 3886],
            "num_drops":   [537992, 537814, 537226, 536837, 534910, 526003, 509382, 486391, 452175, 362680, 257363, 135701, 32900, 7470, 1342],
            "exec_time":   [17.66, 16.83, 16.54, 16.71, 17.01, 16.97, 16.93, 16.82, 16.80, 16.87, 16.89, 16.87, 17.61, 18.29, 18.39],
            "avg_detection_delay": [369.95129, 369.95129, 370.75323, 371.44993, 373.55891, 393.05891, 422.87483, 446.67261, 470.48022, 577.06113, 707.93144, 982.69036, 2086.65099, 2827.87789, 2933.38420],
            "median_detection_delay": [292.5, 292.5, 293.0, 293.5, 296.0, 304.0, 312.0, 327.0, 341.0, 399.5, 453.0, 538.5, 630.0, 656.0, 658.5],
            "std_detection_delay": [335.64995, 335.64995, 336.17886, 337.00109, 339.14005, 355.45287, 388.57302, 421.36189, 450.31592, 572.58858, 749.83109, 1210.21073, 4835.8577, 7534.65713, 7936.39053],
            "p95_detection_delay": [1014.0, 1014.0, 1040.0, 1047.0, 1047.0, 1116.0, 1228.0, 1305.0, 1334.0, 1639.0, 2255.0, 3688.0, 9265.0, 15324.0, 15802.0]
        },
        "jump_and_decay": {
            "num_results": [2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 3055, 3228, 3701, 3863, 3887], 
            "num_drops": [119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 110818, 82589, 27918, 5533, 1210], 
            "exec_time": [14.93, 15.38, 14.89, 15.34, 14.84, 16.03, 15.27, 15.35, 15.20, 15.53, 15.11, 15.38, 15.69, 15.74, 15.69],
            "avg_detection_delay": [1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.44270, 1185.47289, 1185.47289, 1189.73944, 1368.78408, 2333.45988, 2894.75123, 2932.63288],
            "median_detection_delay": [563.0, 563.0, 563.0, 563.0, 563.0, 563.0, 563.0, 563.0, 563.0, 563.0, 567.0, 589.5, 640.0, 657.0, 658.0],
            "std_detection_delay": [1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1949.18441, 1939.69028, 2496.05708, 5879.88043, 7767.10894, 7935.50779],
            "p95_detection_delay": [4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4285.0, 4272.0, 4895.0, 10962.0, 15534.0, 15802.0]
        },
        "max": {
            "num_results": [2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 3036, 3228, 3701, 3857, 3887], 
            "num_drops": [123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 114730, 82589, 27918, 6739, 1210], 
            "exec_time": [15.35, 15.32, 15.29, 15.29, 15.63, 15.40, 15.47, 15.57, 15.53, 15.53, 15.67, 15.55, 15.76, 16.20, 16.06],
            "avg_detection_delay": [1177.95490, 1177.95490, 1177.95490, 1177.95490, 1177.96742, 1177.95490, 1177.95490, 1177.95490, 1177.95490, 1177.95490, 1182.73814, 1368.78408, 2333.45988, 2858.24190, 2932.63288],
            "median_detection_delay": [559.0, 559.0, 559.0, 559.0, 559.0, 559.0, 559.0, 559.0, 559.0, 559.0, 565.5, 589.5, 640.0, 657.0, 658.0],
            "std_detection_delay": [1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1949.25801, 1940.28953, 2496.05708, 5879.88043, 7655.91532, 7935.50779],
            "p95_detection_delay": [4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4272.0, 4895.0, 10962.0, 15534.0, 15802.0]
        },
        "Individual per event": {
            'num_results': [3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3898],
            'num_drops': [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1021, 1015, 456],
            "exec_time":   [16.49, 16.65, 16.48, 16.59, 16.65, 16.54, 16.47, 16.55, 16.60, 16.07, 16.43, 16.27, 16.43, 16.26, 16.35],
            "avg_detection_delay": [2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2966.86301],
            "median_detection_delay": [659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 659.0, 660.0],
            "std_detection_delay": [7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 7933.51712, 8103.29739],
            "p95_detection_delay": [15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 15802.0, 16389.0]
        },
        "Sorted": {
            "num_results": [3908,3908,3908,3908,3908,3908,3908,3908,3908,3908,3908,3908,3908,3908,3908],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [],
            "avg_detection_delay": [],
            "median_detection_delay": [],
            "std_detection_delay": [],
            "p95_detection_delay": []
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


def _annotate_first_last_extremes(x_pos, all_solutions_values):
    """Annotate global min/max at first, middle, and last x positions across all solutions."""
    if not all_solutions_values or not x_pos:
        return
    
    def format_val(v):
        return f'{int(v)}' if v == int(v) else f'{v:.2f}'
    
    # Get values at first position (x=0)
    first_vals = [vals[0] for vals in all_solutions_values if len(vals) > 0]
    # Get values at middle position
    mid_idx = len(x_pos) // 2
    mid_vals = [vals[mid_idx] for vals in all_solutions_values if len(vals) > mid_idx]
    # Get values at last position (x=last)
    last_vals = [vals[-1] for vals in all_solutions_values if len(vals) > 0]
    
    first_x = x_pos[0]
    mid_x = x_pos[mid_idx]
    last_x = x_pos[-1]
    
    if first_vals:
        global_min_first = min(first_vals)
        global_max_first = max(first_vals)
        plt.annotate(format_val(global_max_first), (first_x, global_max_first),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_first != global_max_first:
            plt.annotate(format_val(global_min_first), (first_x, global_min_first),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')
    
    if mid_vals:
        global_min_mid = min(mid_vals)
        global_max_mid = max(mid_vals)
        plt.annotate(format_val(global_max_mid), (mid_x, global_max_mid),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_mid != global_max_mid:
            plt.annotate(format_val(global_min_mid), (mid_x, global_min_mid),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')
    
    if last_vals:
        global_min_last = min(last_vals)
        global_max_last = max(last_vals)
        plt.annotate(format_val(global_max_last), (last_x, global_max_last),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_last != global_max_last:
            plt.annotate(format_val(global_min_last), (last_x, global_min_last),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')


def build_tables():
    # Build tables for each dataset and derived summaries
    all_dataset_tables = {}
    for dataset_name, implementations in DATASETS.items():
        tables = {}
        # Core metrics tables
        for metric in ["num_results", "num_drops", "exec_time", "avg_detection_delay"]:
            data = {"Quarantine Time (s)": QUARANTINE_TIMES}
            for impl_name in IMPLEMENTATIONS:
                data[impl_name] = implementations.get(impl_name, {}).get(metric, [])
            tables[metric] = pd.DataFrame(data)

        # Derived: percent of Sorted results
        if "Sorted" in tables["num_results"].columns:
            sorted_series = pd.Series(
                tables["num_results"]["Sorted"].values,
                index=range(len(QUARANTINE_TIMES))
            )
            pct_data = {"Quarantine Time (s)": QUARANTINE_TIMES}
            for impl in [i for i in IMPLEMENTATIONS if i != "Sorted"]:
                impl_series = pd.Series(
                    tables["num_results"][impl].values,
                    index=range(len(QUARANTINE_TIMES))
                )
                pct = (impl_series / sorted_series * 100).replace([np.inf, -np.inf], np.nan)
                pct_data[f"{impl} (% of Sorted)"] = pct.values.tolist()
            tables["sorted_pct"] = pd.DataFrame(pct_data)

        # Derived: combined jump (diff) and decay (% change) for all metrics per implementation
        jnd_data = {"Quarantine Time (s)": QUARANTINE_TIMES}
        for metric in ["num_results", "num_drops", "exec_time", "avg_detection_delay"]:
            metric_df = tables[metric]
            for col in metric_df.columns[1:]:
                series = pd.Series(metric_df[col].values)
                jump = series.diff().fillna(0).values.tolist()
                with np.errstate(divide='ignore', invalid='ignore'):
                    decay = series.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0).multiply(100).values.tolist()
                jnd_data[f"{metric} - {col} Jump"] = jump
                jnd_data[f"{metric} - {col} Decay (%)"] = decay
        tables["jump_and_decay"] = pd.DataFrame(jnd_data)

        # Derived: max per metric per implementation
        max_rows = []
        for metric in ["num_results", "num_drops", "exec_time", "avg_detection_delay"]:
            row = {"Metric": metric}
            for impl in IMPLEMENTATIONS:
                vals = tables[metric][impl].values if impl in tables[metric] else []
                row[impl] = float(pd.Series(vals).max()) if len(vals) > 0 else float('nan')
            max_rows.append(row)
        tables["max"] = pd.DataFrame(max_rows)

        all_dataset_tables[dataset_name] = tables
    return all_dataset_tables


def save_excel(all_dataset_tables, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, tables in all_dataset_tables.items():
            tables["num_results"].to_excel(writer, sheet_name=f"{dataset_name}_Results", index=False)
            tables["num_drops"].to_excel(writer, sheet_name=f"{dataset_name}_Drops", index=False)
            tables["exec_time"].to_excel(writer, sheet_name=f"{dataset_name}_ExecTime", index=False)
            tables["avg_detection_delay"].to_excel(writer, sheet_name=f"{dataset_name}_DetDelay", index=False)
            tables["jump_and_decay"].to_excel(writer, sheet_name=f"{dataset_name}_JumpAndDecay", index=False)
            tables["max"].to_excel(writer, sheet_name=f"{dataset_name}_Max", index=False)
    print(f"✓ Saved Excel: {path}")


def save_excel_pct(all_dataset_tables, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, tables in all_dataset_tables.items():
            if "sorted_pct" in tables:
                df = tables["sorted_pct"].copy()
                for col in df.columns[1:]:
                    df[col] = df[col].apply(lambda x: f"{x:.4f}" if pd.notna(x) else x)
                df.to_excel(writer, sheet_name=f"{dataset_name}", index=False)
    print(f"✓ Saved Excel: {path}")


def plot_lines(tables, metric, ylabel, filename, dataset_name):
    df = tables[metric]
    x = list(range(len(df["Quarantine Time (s)"])))
    plt.figure(figsize=(12, 6))
    series_names = [c for c in df.columns[1:] if c != "Sorted"]
    y_series = []
    for col in series_names:
        y_vals = df[col].values
        y_series.append(y_vals)
        color = COLORS.get(col, None)
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, y_series)
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(f"{ylabel} vs Quarantine Time - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    if metric == "exec_time":
        plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_drops_enhanced(tables, dataset_name):
    """Create enhanced drops plot with better visibility for differences"""
    df = tables["num_drops"]
    x = list(range(len(df["Quarantine Time (s)"])))
    
    # Single plot with log scale for better visibility of differences
    plt.figure(figsize=(12, 6))
    series_names = [c for c in df.columns[1:] if c != "Sorted"]
    y_series = []
    for col in series_names:
        plotted_vals = [v + 1 for v in df[col]]
        y_series.append(plotted_vals)
        color = COLORS.get(col, None)
        plt.plot(x, plotted_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, [df[col].values for col in series_names])
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Dropped Events (log scale, +1)", fontsize=11)
    plt.title(f"Dropped Events vs Quarantine Time (Log Scale) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    plt.yscale('log')
    plt.grid(True, which="both")
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    
    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"compare_{safe_name}_drops_enhanced.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_lines_top3(tables, metric, ylabel, filename, dataset_name):
    """Plot top 3 quarantine implementations (jump_and_decay, max, Individual per event)"""
    df = tables[metric]
    # Filter out Direct and Fixed-Time columns
    cols_to_plot = [col for col in df.columns[1:] if col not in ["Direct", "Fixed-Time", "Sorted"]]
    x = list(range(len(df["Quarantine Time (s)"])))
    plt.figure(figsize=(12, 6))
    series_names = cols_to_plot
    y_series = []
    for col in series_names:
        y_vals = df[col].values
        y_series.append(y_vals)
        color = COLORS.get(col, None)
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, y_series)
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(f"{ylabel} vs Quarantine Time (Top 3) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    if metric == "exec_time":
        plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_drops_enhanced_top3(tables, dataset_name):
    """Create enhanced drops plot for top 3 quarantine implementations"""
    df = tables["num_drops"]
    # Filter out Direct and Fixed-Time columns
    cols_to_plot = [col for col in df.columns[1:] if col not in ["Direct", "Fixed-Time", "Sorted"]]
    x = list(range(len(df["Quarantine Time (s)"])))
    
    # Single plot with log scale for better visibility of differences
    plt.figure(figsize=(12, 6))
    series_names = cols_to_plot
    y_series = []
    for col in series_names:
        plotted_vals = [v + 1 for v in df[col]]
        y_series.append(plotted_vals)
        color = COLORS.get(col, None)
        plt.plot(x, plotted_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, [df[col].values for col in series_names])
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Dropped Events (log scale, +1)", fontsize=11)
    plt.title(f"Dropped Events vs Quarantine Time (Log Scale, Top 3) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    plt.yscale('log')
    plt.grid(True, which="both")
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    
    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"compare_{safe_name}_drops_enhanced_top3.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_all(all_dataset_tables):
    for dataset_name, tables in all_dataset_tables.items():
        safe_name = dataset_name.lower().replace(" ", "_")
        # Original plots with all implementations
        plot_lines(tables, "num_results", "Number of Results", f"compare_{safe_name}_results.png", dataset_name)
        plot_drops_enhanced(tables, dataset_name)
        plot_lines(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time.png", dataset_name)
        plot_lines(tables, "avg_detection_delay", "Detection Delay (s)", f"compare_{safe_name}_avg_detection_delay.png", dataset_name)
        
        # Top 3 quarantine implementations plots
        plot_lines_top3(tables, "num_results", "Number of Results", f"compare_{safe_name}_results_top3.png", dataset_name)
        plot_drops_enhanced_top3(tables, dataset_name)
        plot_lines_top3(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time_top3.png", dataset_name)
        plot_lines_top3(tables, "avg_detection_delay", "Detection Delay (s)", f"compare_{safe_name}_avg_detection_delay_top3.png", dataset_name)


def print_tables(all_dataset_tables):
    for dataset_name, tables in all_dataset_tables.items():
        print(f"\n{'='*80}")
        print(f"DATASET: {dataset_name}")
        print('='*80)
        print("\n=== Results ===")
        print(tables["num_results"].to_string(index=False))
        print("\n=== Drops ===")
        print(tables["num_drops"].to_string(index=False))
        print("\n=== Execution Time (s) ===")
        print(tables["exec_time"].to_string(index=False))
        print("\n=== Detection Delay (s) ===")
        print(tables["avg_detection_delay"].to_string(index=False))
        print("\n=== Jump + Decay (num_results diff and % change) ===")
        print(tables["jump_and_decay"].to_string(index=False))
        print("\n=== Max values across quarantine times ===")
        print(tables["max"].to_string(index=False))
        if "sorted_pct" in tables:
            print("\n=== % Results vs Sorted (num_results) ===")
            print(tables["sorted_pct"].to_string(index=False))


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_dataset_tables = build_tables()
    print_tables(all_dataset_tables)
    excel_path = os.path.join(OUTPUT_DIR, "compare_new_impl.xlsx")
    save_excel(all_dataset_tables, excel_path)
    excel_pct_path = os.path.join(OUTPUT_DIR, "compare_new_impl_sorted_pct.xlsx")
    save_excel_pct(all_dataset_tables, excel_pct_path)
    plot_all(all_dataset_tables)
    print("\n" + "="*80)
    print("Done! Update the DATASETS section with your real measurements if needed.")
    print("="*80)
