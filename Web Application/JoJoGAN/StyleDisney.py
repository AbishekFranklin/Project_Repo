import torch
from torchvision import transforms, utils
import torch.nn.functional as F
import dlib
from PIL import Image
import numpy as np
import math
import torchvision
import scipy
import scipy.ndimage
import torchvision.transforms as transforms
import math
import random
import os
import argparse
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import numpy as np
from torch import nn, autograd, optim
from torch.nn import functional as F
from tqdm import tqdm
import wandb
from copy import deepcopy
import matplotlib.pyplot as plt

# JoJoGAN Specific Import
from model import *
from e4e_projection import projection as e4e_projection
from util import *


# Set the environment variable
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

latent_dim = 512

def parse_arguments():
    parser = argparse.ArgumentParser(description="Style Transfer with JoJoGAN")
    parser.add_argument("-f", "--filename", type=str, required=True, help="Input image filename")
    return parser.parse_args()

args = parse_arguments()
filename = args.filename

# Load original generator
original_generator = Generator(1024, latent_dim, 8, 2).to(device)
ckpt = torch.load('models/stylegan2-ffhq-config-f.pt', map_location=lambda storage, loc: storage)
original_generator.load_state_dict(ckpt["g_ema"], strict=False)
mean_latent = original_generator.mean_latent(10000)

# to be finetuned generator
generator = deepcopy(original_generator)

transform = transforms.Compose(
    [
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)



plt.rcParams['figure.dpi'] = 150

#@title Choose input face
#filename = 'qbi.jpeg' #param {type:"string"}

#filename = 'img1.jpeg' #param {type:"string"}

filepath = filename #f'test_input/{filename}'


# uploaded = files.upload()
# filepath = list(uploaded.keys())[0]
name = strip_path_extension(filepath)+'.pt'

# aligns and crops face from the source image
aligned_face = align_face(filepath)

# my_w = restyle_projection(aligned_face, name, device, n_iters=1).unsqueeze(0)
my_w = e4e_projection(aligned_face, name, device).unsqueeze(0)


plt.rcParams['figure.dpi'] = 150
pretrained = 'disney' #param ['art', 'arcane_multi', 'sketch_multi', 'arcane_jinx', 'arcane_caitlyn', 'jojo_yasuho', 'jojo', 'disney']
preserve_color = True #param{type:"boolean"}

ckpt = f'{pretrained}_preserve_color.pt'

#ckpt = f'MyStyle_JoJoGAN.pt'

#@title Generate results
n_sample =  5#param {type:"number"}
seed = 3000 #param {type:"number"}



ckpt = torch.load(os.path.join('models', ckpt), map_location=lambda storage, loc: storage)
generator.load_state_dict(ckpt["g"], strict=False)


torch.manual_seed(seed)
with torch.no_grad():
    generator.eval()
    z = torch.randn(n_sample, latent_dim, device=device)

    original_sample = original_generator([z], truncation=0.7, truncation_latent=mean_latent)
    sample = generator([z], truncation=0.7, truncation_latent=mean_latent)

    original_my_sample = original_generator(my_w, input_is_latent=True)
    my_sample = generator(my_w, input_is_latent=True)


style_path = f'style_images_aligned/{pretrained}.png'

style_image = transform(Image.open(style_path)).unsqueeze(0).to(device)

normalized_my_output = (my_sample + 1) / 2

target_im = utils.make_grid(normalized_my_output, normalize=False)

# Display the grid using matplotlib
plt.figure(figsize=(5, 5))
plt.imshow(target_im.permute(1, 2, 0).cpu().numpy())
plt.axis('off')
plt.title('My Disney Face')
plt.savefig('C:/Users/Abishek/Documents/JoJoGAN/output/output_image.png')

#output_filename = 'C:/Users/Abishek/Documents/JoJoGAN/output/output_image.png'

# Azure Storage Account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=tshfhjabishekasrcache;AccountKey=inz+3kkO6JnpA6DyO+fWa/N72Qc60ijYntyU+wxeWZjLS4u7uNdJrf6h47lErtirJixu8PjVa82g+AStK2XcWQ==;EndpointSuffix=core.windows.net"

# Blob Container name
container_name = "asr-254ad3cd-421e-9b77-0ccfb919371a"

# Get the current datetime in the desired format (e.g., YYYYMMDD_HHMMSS)
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create a ContainerClient
container_client = blob_service_client.get_container_client(container_name)

# Define the local file path and the desired name for the blob in Azure Storage
output_filename = 'C:/Users/Abishek/Documents/JoJoGAN/output/output_image.png'
base_filename, file_extension = os.path.splitext(os.path.basename(output_filename))
new_blob_name = f'{base_filename}_{current_datetime}{file_extension}'

# Upload the image to Azure Blob Storage
with open(output_filename, "rb") as data:
    container_client.upload_blob(name=new_blob_name, data=data)

# Generate the Azure Blob Storage URL for the uploaded image
azure_blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{new_blob_name}"

# Now, you can use 'azure_blob_url' to access the image in Azure Blob Storage.
#print(f"Image uploaded to Azure Blob Storage. URL: {azure_blob_url}")
