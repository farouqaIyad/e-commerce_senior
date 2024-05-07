from cloudinary import CloudinaryImage
from dotenv import load_dotenv
import cloudinary.uploader
import cloudinary.api
import cloudinary
import json

load_dotenv()

config = cloudinary.config(secure=True)


def uploadImage(image_path):

    cloudinary.uploader.upload(
        r"{}".format(image_path),
        public_id="quickstart",
        unique_filename=False,
        overwrite=True,
    )
    srcURL = CloudinaryImage("quickstart").build_url()
    print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")


def getAssetInfo():

    image_info = cloudinary.api.resource("quickstart_butterfly")
    print(
        "****3. Get and use details of the image****\nUpload response:\n",
        json.dumps(image_info, indent=2),
        "\n",
    )

    if image_info["width"] > 900:
        update_resp = cloudinary.api.update("quickstart_butterfly", tags="large")
    elif image_info["width"] > 500:
        update_resp = cloudinary.api.update("quickstart_butterfly", tags="medium")
    else:
        update_resp = cloudinary.api.update("quickstart_butterfly", tags="small")

    # Log the new tag to the console.
    print("New tag: ", update_resp["tags"], "\n")
