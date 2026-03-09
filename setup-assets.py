import requests
import os

# 1. Define folder and test images
SAVE_DIR = "assets"
test_images = {
    "dog_test.jpg": "https://images.unsplash.com/photo-1543466835-00a7907e9de1",
    "cat_test.jpg": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",
    "person_test.jpg": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80",
    "dog_and_cat.jpg": "https://images.pexels.com/photos/46024/pexels-photo-46024.jpeg",    # Dog + Cat
    "person_and_cat.jpg": "https://images.pexels.com/photos/1643457/pexels-photo-1643457.jpeg", # Person + Cat
    "person_and_dog.jpg": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg", # Person + Dog
    "all_targets.jpg": "https://images.pexels.com/photos/662417/pexels-photo-662417.jpeg",    # Person + Dog + Cat
    "no_target.jpg": "https://images.unsplash.com/photo-1506744038136-46273834b3fb" # Landscape
}

def setup_test_data():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"Created directory: {SAVE_DIR}")

    for filename, url in test_images.items():
        path = os.path.join(SAVE_DIR, filename)
        
        # Download the image
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Failed to download {filename}")

if __name__ == "__main__":
    setup_test_data()