#!/usr/bin/env python
# coding: utf-8

# In[4]:


# convert coco dataset to only have images/labels with people: 
# 1) generates train2014_person.txt and val2014_person.txt
# 2) within labels directory, creates subdirectories train2014 
#    and val2014 with labels for people (keeps original labels
#    in subdirectories train2014_orig and val2014_orig)

# directory structure: 
# --- get_people.py
# --- (dir) images
# --- (dir) labels

import os

year = 2014
year = str(year)

for trainval in ['train', 'val']:
    labels_dir = os.path.join('labels', trainval + year)
    person_dir = os.path.join('labels', trainval + year + '_person')
    os.makedirs(person_dir, exist_ok=True)
    # loop through 'labels_dir', save to 'person_dir'
    for filename in os.listdir(labels_dir):
        if filename.endswith('.txt'):
            file = os.path.join(labels_dir, filename) # relative path to filename
            person_file = os.path.join(person_dir, filename)
            with open(file, 'r') as f:
                lines = f.readlines()
            person_lines = [line for line in lines if line.split(' ')[0] == '0']
            if len(person_lines) != 0:
                with open(person_file, 'w') as f:
                    f.writelines(person_lines)

    files = os.listdir(person_dir)
    files = [file.replace('.txt', '.jpg\n') for file in files]
    files = [os.path.join('data/coco%s/images/%s%s/' % (year, trainval, year), file) for file in files]
    with open(trainval + year + '_person.txt', 'w') as f:
        f.writelines(files)
        
    os.rename('labels/%s%s', 'labels/%s%s_orig' % (trainval, year))
    os.rename('labels/%s%s_person', 'labels/%s%s' % (trainval, year))

