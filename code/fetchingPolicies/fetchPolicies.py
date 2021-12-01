#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 21:10:04 2021

@author: patrickzoechbauer
"""

import json
import pandas as pd
import glob, os
import sys

def load_github_log(filepath_log):
    
    #load log files from GitHub
    with open(filepath_log) as f:
        lines = f.read().splitlines()
    lines = list(filter((',').__ne__, lines))
    lines = ['},' if x == '}' else x for x in lines]
    lines[-1] = '}'
    lines.insert(0, '[')
    lines.append(']')
    data = json.loads(''.join(lines))
    
    #Convert to pandas df
    df = pd.json_normalize(data)
    return df

def fetch_file_paths(sites):
    all_files = []
    for website in sites:
        text_files = glob.glob(path_privacy_policies + "/**/"+website+".md", 
                               recursive = True)
        all_files.append(text_files)
    
    return all_files
    
if __name__ == "__main__":
    #input: 
    number_of_policies = int(sys.argv[1])
    year = int(sys.argv[2])
    path_privacy_policies = '/Users/patrickzoechbauer/Documents/LawCS/privacy-policy-historical'   
    filepath_log = 'gitHubLog.json'

    df = load_github_log(filepath_log)  
    
    #select random subsample
    df_y = df[df['year'] == year]
    sites = list(df_y.sample(number_of_policies)['site_hostname'])
    
    all_files = fetch_file_paths(sites)  
    
    #Load
    file1 = all_files[0][0]
    
    print('###########################')
    print('Selected website: {}'.format(sites))
    print('###########################')
    
    with open(file1, 'r') as f:
        lines = f.read().splitlines()
    
    for line in lines:
        print(line)
    
    #lines = list(filter(('').__ne__, lines))
    
    
    
    
    
    