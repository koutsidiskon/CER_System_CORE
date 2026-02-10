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
# Metrics: num_results, num_drops, exec_time, detection_delay
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
            "num_results": [20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258],
            "num_drops":   [79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434],
            "exec_time":   [4.69, 4.59, 4.56, 5.24, 4.54, 4.56, 4.52, 4.57, 4.58, 5.19, 4.55, 4.56, 4.59, 4.58, 4.77],
            "avg_detection_delay": [262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982, 262.95982],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [28640, 28640, 28640, 28640, 28640, 28640, 29210, 29670, 30197, 30634, 30808, 30851, 30862, 30867, 30870],
            "num_drops":   [14524, 14519, 14501, 14459, 14396, 14241, 11085, 8213, 4512, 1574, 472, 175, 75, 34, 24],
            "exec_time":   [4.80, 4.70, 4.75, 4.71, 4.71, 4.69, 4.69, 4.67, 4.81, 4.76, 4.82, 4.78, 4.74, 4.74, 4.76],
            "avg_detection_delay": [266.58520, 266.58520, 266.58520, 266.58520, 266.58520, 266.58520, 267.40774, 268.29323, 269.74269, 272.18777, 273.67502, 275.18784, 276.34178, 277.12897, 277.12925],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay":[132.60408, 132.60408, 132.60408, 132.60408, 132.60408, 132.60408, 133.98298, 136.6398, 140.43566, 147.29357, 153.07384, 165.144, 177.29505, 193.8333, 193.82408],
            "p95_detection_delay": [480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.0, 480.00001, 540.0, 540.0, 540.0]
        },
        "jump_and_decay": {
            "num_results": [30853, 30853, 30853, 30853, 30853, 30853, 30853, 30853, 30853, 30853, 30853, 30854, 30865, 30867, 30870], 
            "num_drops": [130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 111, 55, 34, 24], 
            "exec_time": [4.59, 4.63, 4.66, 4.65, 4.67, 4.71, 4.65, 4.64, 4.94, 4.55, 4.52, 4.58, 4.55, 5.30, 4.50],
            "avg_detection_delay": [275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.38083, 277.11388, 277.12897, 277.12925],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay":[166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.90115, 193.81231, 193.8333, 193.82408],
            "p95_detection_delay": [540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0]
        },
        "max": {
            "num_results": [30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30854,30865,30867,30870], 
            "num_drops": [131,131,131,131,131,131,131,131,131,131,131,112,55,34,24], 
            "exec_time": [4.60, 4.71, 4.59, 4.48, 4.80, 5.10, 5.08, 5.00, 5.47, 5.00, 4.75, 4.75, 4.74, 4.77, 4.79],
            "avg_detection_delay": [275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.31391, 275.38083, 277.11388, 277.12897, 277.12925],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay":[166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.48944, 166.90115, 193.81231, 193.8333, 193.82408],
            "p95_detection_delay": [540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0]
            
        },
        "Individual per event": {
            'num_results': [30855, 30855, 30855, 30855, 30855, 30855, 30855, 30855, 30855, 30855, 30855, 30859, 30865, 30867, 30870],
            'num_drops': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 88, 52, 33, 24],
            "exec_time":   [4.35, 4.41, 4.41, 4.41, 4.47, 4.49, 5.10, 4.44, 4.48, 4.85, 4.51, 4.49, 4.79, 4.52, 4.52],
            "avg_detection_delay": [276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.15557, 276.36670, 277.11388, 277.12897, 277.12925],
            "median_detection_delay": [240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0, 240.0],
            "std_detection_delay":[184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 184.36705, 186.26521, 193.81231, 193.8333, 193.82408],
            "p95_detection_delay": [540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0, 540.0]
        },
        "Sorted": {
            "num_results": [30874,30874,30874,30874,30874,30874,30874,30874,30874,30874,30874,30874,30874,30874,30874],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "avg_detection_delay": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [27661,27661,27661,27661,27661,27661,27661,27661,27661,27661,27661,27661,27661,27661,27661],
            "num_drops":   [336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293],
            "exec_time":   [11.82, 11.82, 11.90, 11.82, 11.79, 11.82, 11.86, 12.20, 11.75, 11.73, 11.73, 11.95, 11.83, 11.80, 11.76],
            "avg_detection_delay": [0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018, 0.31018],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [29068, 29068, 29068, 29068, 29068, 29068, 33488, 36495, 40925, 44787, 47454, 48951, 49511, 49636, 49704],
            "num_drops":   [313826, 313826, 313826, 313826, 313826, 313826, 274143, 215379, 126483, 60387, 21780, 7209, 2342, 631, 140],
            "exec_time":   [12.11, 12.21, 12.68, 12.08, 12.10, 12.17, 12.49, 12.43, 12.98, 13.41, 13.55, 13.56, 13.54, 13.33, 13.08],
            "avg_detection_delay": [4.96835, 4.96835, 4.96835, 4.96835, 4.96835, 4.96835, 52.77771, 103.38841, 231.48198, 447.44210, 714.64281, 988.99553, 1154.35084, 1212.42647, 1255.85271],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay":[24.14099, 24.14099, 24.14099, 24.14099, 24.14099, 24.14099, 147.51542, 242.46425, 477.31588, 915.6692, 1508.05556, 2247.57456, 2773.28581, 3013.82422, 3236.93902],
            "p95_detection_delay": [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 360.0, 660.0, 1320.0, 2460.0, 3960.0, 5640.0, 6240.0, 6360.0, 6420.0]
        },
        "jump_and_decay": {
            "num_results": [49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49704, 49704, 49704, 49704, 49704, 49704], 
            "num_drops": [147, 147, 147, 147, 147, 147, 147, 141, 141, 135, 135, 117, 103, 74, 58], 
            "exec_time": [11.91, 12.51, 12.11, 12.12, 12.40, 12.11, 12.27, 12.56, 12.15, 12.32, 12.02, 12.16, 12.65, 12.59, 12.45],
            "avg_detection_delay": [1255.74978, 1255.74593, 1255.73475, 1255.74593, 1255.69091, 1255.74593, 1255.78131, 1255.74593, 1255.74785, 1255.84983, 1255.84983, 1255.84983, 1255.84983, 1255.84983, 1255.84983],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay":[3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902],
            "p95_detection_delay": [6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0]
        },
        "max": {
            "num_results": [49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49704, 49704, 49704, 49704, 49704, 49704], 
            "num_drops": [148, 148, 148, 148, 148, 148, 148, 142, 142, 136, 136, 118, 104, 77, 58], 
            "exec_time": [12.48, 12.25, 12.40, 12.43, 13.45, 12.43, 12.50, 13.09, 12.61, 12.55, 12.57, 12.39, 12.93, 12.49, 12.52],
            "avg_detection_delay": [1255.74701, 1255.74593, 1255.75049, 1255.74593, 1255.74593, 1255.75170, 1255.74593, 1255.74593, 1255.74593, 1255.84983, 1255.84813, 1255.83973, 1255.84730, 1255.84586, 1255.79374],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay":[3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902],
            "p95_detection_delay": [6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0]
        },
        "Individual per event": {
            'num_results': [49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49703, 49704, 49704, 49704, 49704, 49704, 49704],
            'num_drops': [33, 33, 33, 33, 33, 33, 33, 29, 29, 17, 17, 17, 17, 17, 17],
            "exec_time":   [12.40, 12.40, 12.57, 12.54, 11.85, 12.54, 11.90, 12.11, 11.96, 11.63, 11.54, 11.49, 11.60, 11.88, 11.52],
            "avg_detection_delay": [1255.74340, 1255.74593, 1255.68418, 1255.74233, 1255.74628, 1255.74593, 1255.74593, 1255.74593, 1255.74593, 1255.84983, 1255.84983, 1255.84983, 1255.79178, 1255.84983, 1255.84225],
            "median_detection_delay": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "std_detection_delay":[3236.8887, 3236.8887, 3236.8887, 3236.7848, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.8887, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902, 3236.93902],
            "p95_detection_delay": [6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0, 6420.0]
        },
        "Sorted": {
            "num_results": [49704,49704,49704,49704,49704,49704,49704,49704,49704,49704,49704,49704,49704,49704,49704],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "avg_detection_delay": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [104,104,104,104,104,104,104,104,104,104,104,104,104,104,104],
            "num_drops":   [1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280],
            "exec_time":   [14.57, 14.45, 14.64, 14.79, 14.58, 14.50, 14.61, 14.48, 14.12, 14.49, 14.75, 14.67, 14.67, 14.01, 14.59],
            "avg_detection_delay": [73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462, 73.88462],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
        "Fixed-Time": {
            "num_results": [90866, 90885, 90991, 91029, 91446, 93187, 95786, 99361, 105197, 120006, 138147, 159719, 183183, 188627, 189903],
            "num_drops":   [537992, 537814, 537226, 536837, 534910, 526003, 509382, 486391, 452175, 362680, 257363, 135701, 32900, 7470, 1342],
            "exec_time":   [19.06, 18.91, 18.68, 19.15, 19.58, 19.60, 19.14, 19.34, 19.61, 19.90, 20.58, 23.24, 24.18, 24.66, 24.84],
            "avg_detection_delay": [442.94307, 445.40647, 444.52015, 444.86068, 447.01422, 455.49752, 470.90506, 491.12605, 515.85595, 590.79540, 717.51023, 1005.29688, 2245.08046, 2978.42675, 3214.09628],
            "median_detection_delay": [333.0, 333.0, 333.0, 333.0, 334.0, 340.0, 348.0, 358.0, 375.0, 421.0, 483.0, 554.0, 634.0, 656.0, 660.0],
            "std_detection_delay":[394.67251, 395.817, 398.48456, 398.82684, 400.32504, 406.73244, 427.86113, 455.01752, 479.47854, 555.61539, 718.13364, 1293.49619, 5425.05246, 7958.93089, 9099.87394],
            "p95_detection_delay": [1203.0, 1205.0, 1207.0, 1210.0, 1216.0, 1233.0, 1292.0, 1369.0, 1445.0, 1686.0, 2210.0, 3657.0, 10415.0, 15834.0, 17128.0]
        },
        "jump_and_decay": {
            "num_results": [163765, 163765, 163765, 163763, 163765, 163765, 163765, 163765, 163765, 163765, 165860, 171700, 184205, 189061, 189934], 
            "num_drops": [119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 110818, 82589, 27918, 5533, 1210], 
            "exec_time": [19.73, 19.30, 19.95, 19.70, 19.47, 19.91, 19.30, 19.67, 19.35, 19.38, 20.09, 19.59, 20.01, 20.32, 21.68],
            "avg_detection_delay": [1229.26576, 1229.26576, 1229.55994, 1229.26623, 1229.26576, 1229.26576, 1229.26576, 1229.26557, 1229.26517, 1229.27286, 1252.35372, 1438.83522, 2387.00267, 3029.93030, 3220.26216],
            "median_detection_delay": [572.0, 572.0, 572.0, 572.0, 572.0, 572.0, 572.0, 572.0, 572.0, 572.0, 579.0, 598.0, 638.0, 657.0, 661.0],
            "std_detection_delay":[2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2090.29778, 2107.89264, 2680.18473, 5977.09, 8126.52416, 9122.14149],
            "p95_detection_delay": [4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4471.0, 4584.0, 5688.0, 11165.0, 16180.0, 17161.0]
        },
        "max": {
            "num_results": [163021, 163021, 163021, 163021, 163021, 163021, 163023, 163021, 163020, 163021, 165100, 171700, 184205, 188781, 189934], 
            "num_drops": [123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 114730, 82589, 27918, 6739, 1210], 
            "exec_time": [20.02, 19.95, 19.92, 20.58, 19.42, 20.07, 20.23, 19.72, 20.63, 19.97, 19.70, 21.44, 21.07, 21.36, 23.14],
            "avg_detection_delay": [1225.61857, 1225.60866, 1225.60866, 1225.61119, 1225.60866, 1225.60866, 1225.60926, 1225.60866, 1225.60893, 1225.61059, 1248.38866, 1438.83522, 2387.00626, 3002.11804, 3220.26216],
            "median_detection_delay": [570.0, 570.0, 570.0, 570.0, 570.0, 570.0, 570.0, 570.0, 570.0, 570.0, 576.0, 598.0, 638.0, 657.0, 661.0],
            "std_detection_delay":[2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2092.60539, 2110.01693, 2680.18473, 5977.09, 8043.87387, 9122.14149],
            "p95_detection_delay": [4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4496.0, 4596.0, 5688.0, 11165.0, 15953.0, 17161.0]
        },
        "Individual per event": {
            'num_results': [189956, 189956, 189956, 189956, 189956, 189953, 189956, 189956, 189956, 189956, 189956, 189956, 189956, 189956, 190129],
            'num_drops': [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1021, 1015, 456],
            "exec_time":   [22.03, 22.25, 22.05, 22.17, 21.75, 22.64, 21.71, 22.05, 21.88, 21.64, 22.05, 22.62, 22.31, 21.95, 21.78],
            "avg_detection_delay": [3238.19629, 3238.19397, 3238.19629, 3238.19629, 3238.19486, 3238.19629, 3238.19585, 3238.19629, 3238.20277, 3238.19588, 3238.26112, 3238.19629, 3238.20480, 3238.20239, 3260.18691],
            "median_detection_delay": [661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0, 661.0],
            "std_detection_delay":[9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9276.03168, 9388.56462],
            "p95_detection_delay": [17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17163.0, 17197.0]
        },
        "Sorted": {
            "num_results": [190325,190325,190325,190325,190325,190325,190325,190325,190325,190325,190325,190325,190325,190325,190325],
            "num_drops": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "exec_time": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "avg_detection_delay": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "median_detection_delay": [],
            "std_detection_delay":[],
            "p95_detection_delay": []
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


def _format_value(val):
    return f"{int(val):,}" if float(val).is_integer() else f"{val:.2f}"


def _annotate_ranked(x_vals, series_yvals, labels, key_indices, spacing=6):
    """Annotate selected points, stacking labels above/below while preserving order."""
    for i, x in enumerate(x_vals):
        entries = []
        for s_idx, y_series in enumerate(series_yvals):
            if i in key_indices:
                entries.append((s_idx, y_series[i], labels[s_idx][i]))
        if not entries:
            continue
        # Deduplicate exact y-values (keep first)
        by_y = {}
        for item in entries:
            y_val = item[1]
            if y_val not in by_y:
                by_y[y_val] = item
        uniq_items = list(by_y.values())

        # Group decimals by integer part; keep only min and max per integer part
        decimals_by_int = {}
        integers = []
        for it in uniq_items:
            y_val = float(it[1])
            if y_val.is_integer():
                integers.append(it)
            else:
                key = int(y_val)
                decimals_by_int.setdefault(key, []).append(it)

        selected = []
        for group in decimals_by_int.values():
            if not group:
                continue
            min_dec = min(group, key=lambda t: t[1])
            max_dec = max(group, key=lambda t: t[1])
            selected.append(min_dec)
            if max_dec[1] != min_dec[1]:
                selected.append(max_dec)

        # add all unique integers
        selected.extend(integers)
        # Stack selected labels centered on the point
        selected.sort(key=lambda t: t[1])
        center = (len(selected) - 1) / 2.0
        for rank, (_, y_val, text) in enumerate(selected):
            offset = spacing * (rank - center)
            va = 'bottom' if offset >= 0 else 'top'
            plt.annotate(text, (x, y_val), textcoords="offset points", xytext=(0, offset),
                         ha='center', va=va, fontsize=8, fontweight='bold')


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
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
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
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
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
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
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
            tables["detection_delay"].to_excel(writer, sheet_name=f"{dataset_name}_DetDelay", index=False)
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
        plot_lines(tables, "detection_delay", "Detection Delay (s)", f"compare_{safe_name}_detection_delay.png", dataset_name)
        
        # Top 3 quarantine implementations plots
        plot_lines_top3(tables, "num_results", "Number of Results", f"compare_{safe_name}_results_top3.png", dataset_name)
        plot_drops_enhanced_top3(tables, dataset_name)
        plot_lines_top3(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time_top3.png", dataset_name)
        plot_lines_top3(tables, "detection_delay", "Detection Delay (s)", f"compare_{safe_name}_detection_delay_top3.png", dataset_name)


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
        print(tables["detection_delay"].to_string(index=False))
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
