# Make importing files easier
import pygame
from csv import reader
from os import walk

# Import CSV file and converting into a readable form
def import_csv_layout(path):
    terrain_map = []
    # Open the CSV file
    with open(path) as map:
        layout = reader(map, delimiter = ",")
        
        # Convert CSV to list form
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

# Get all images from a folder, ignoring subfolders, etc and makes pygame load it
def import_folder(path):
    surface_list = []
    
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list