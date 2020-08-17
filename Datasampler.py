import glob
import json
import random
import csv
import os
import re
import argparse
import numpy as np
from tqdm import tqdm

def list_pictures(directory, ext='jpg|jpeg|bmp|png|ppm'):
    '''
    Returns path of folder/directory of every image present in directory by using simple regex expression
    '''
    return [os.path.join(root, f)
            for root, _, files in os.walk(directory) for f in files
            if re.match(r'([\w]+\.(?:' + ext + '))', f)]


def get_negative_images(all_images,image_names,num_neg_images):
    '''
    Returns randomly sampled 'n' negative images from all_images
    '''

    random_numbers = np.arange(len(all_images))
    np.random.shuffle(random_numbers)
    if int(num_neg_images)>(len(all_images)-1):
        num_neg_images = len(all_images)-1
    neg_count = 0
    negative_images = []
    for random_number in list(random_numbers):
        if all_images[random_number] not in image_names:
            negative_images.append(all_images[random_number])
            neg_count += 1
            if neg_count>(int(num_neg_images)-1):
                break
    return negative_images

def get_positive_images(image_name,image_names,num_pos_images):
    '''
    Returns randomly sampled 'n' positive images from all_images
    '''
    random_numbers = np.arange(len(image_names))
    np.random.shuffle(random_numbers)
    if int(num_pos_images)>(len(image_names)-1):
        num_pos_images = len(image_names)-1
    pos_count = 0
    positive_images = []
    for random_number in list(random_numbers):
        if image_names[random_number]!= image_name:
            positive_images.append(image_names[random_number])
            pos_count += 1
            if int(pos_count)>(int(num_pos_images)-1):
                break
    return positive_images

def triplet_sampler(directory_path, output_path,num_neg_images,num_pos_images):

    classes = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    all_images = []
    for class_ in classes:
        all_images += (list_pictures(os.path.join(directory_path,class_)))
    triplets = []
    for class_ in classes:
        image_names = list_pictures(os.path.join(directory_path,class_))
        for image_name in tqdm(image_names):
            image_names_set = set(image_names)
            query_image = image_name
            positive_images = get_positive_images(image_name,image_names,num_pos_images)
            for positive_image in positive_images:
                negative_images = get_negative_images(all_images,set(image_names),num_neg_images)
                for negative_image in negative_images:
                    triplets.append(query_image+',')
                    triplets.append(positive_image+',')
                    triplets.append(negative_image+'\n')

    f = open(os.path.join(output_path,"triplets.txt"),'w')
    f.write("".join(triplets))
    f.close()

input_directory=r'F:\Deep rank'
output_directory=r'F:\triplet sampler'
num_neg_images=10
num_pos_images=10
print (f"Input Directory: {input_directory}")
print (f"Output Directory: {output_directory}")
print (f"Number of Positive image per Query image:{ num_pos_images}")
print (f"Number of Negative image per Query image: {num_neg_images}")

triplet_sampler(directory_path=input_directory, output_path=output_directory, num_neg_images=num_neg_images, num_pos_images=num_pos_images)
