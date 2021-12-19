from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(metadata_file_name)
    collectible_metadata = metadata_template
    if Path(metadata_file_name).exists():
        print(f"{metadata_file_name} already exists! Delete it to overwrite")
    else:
        print(f"Creating Metadata file: {metadata_file_name}")
        collectible_metadata["name"] = breed
        collectible_metadata["description"] = f"An adorable {breed} pup!"
        image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
        image_uri = upload_to_ipfs(image_path)
        collectible_metadata["image"] = image_uri
        with open(metadata_file_name, "w") as file:
            json.dump(
                collectible_metadata, file
            )  # save the dictionary collectible_metadata as JSON to metadata_file_name
        upload_to_ipfs(metadata_file_name)


# for testing:
# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:  # "rb": open/read as binary
        image_binary = fp.read()  # now the binary image is stored in image_binary
        ipfs_url = "http://127.0.0.1:5001"  # details from README.md
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()[
            "Hash"
        ]  # so if there is any alternation of the image, the hash will change

        filename = filepath.split("/")[-1:][0]  # "./img/0-PUG.png" -> "0-PUG.png"
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
