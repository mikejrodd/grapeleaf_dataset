import os
import json

# Define the description template for the conversation
descriptions = {
    "healthy": "The leaf should be green and healthy, without any signs of esca disease, which includes discoloration, brown spots, or unusual texture.",
    "rot": "The leaf shows signs of rot but not esca disease.",
    "blight": "The leaf shows signs of blight but not esca disease.",
    "esca": "The leaf shows signs of esca disease, which includes discoloration, brown spots, or unusual texture."
}

def create_conversation(description, is_abnormal):
    conversation = [
        {
            "from": "human",
            "value": f"This is a photo of a grape leaf for anomaly detection. {description} Is there any anomaly in the image?"
        }
    ]
    
    if is_abnormal:
        response = "Yes, there are anomalies in the image. The symptoms of the leaf disease appear to be caused by an Esca infection."
    else:
        response = "No, there is no anomaly in the image."
    
    conversation.append({
        "from": "gpt",
        "value": response
    })
    
    return conversation

def process_images(root_dir):
    data = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                image_name = os.path.relpath(file_path, root_dir)
                
                if "train/good" in file_path:
                    if "B.Rot" in file:
                        description = descriptions["rot"]
                    elif "L.Blight" in file:
                        description = descriptions["blight"]
                    else:
                        description = descriptions["healthy"]
                    conversation = create_conversation(description, False)
                
                elif "test/good" in file_path:
                    if "B.Rot" in file:
                        description = descriptions["rot"]
                    elif "L.Blight" in file:
                        description = descriptions["blight"]
                    else:
                        description = descriptions["healthy"]
                    conversation = create_conversation(description, False)
                
                elif "test/esca" in file_path:
                    description = descriptions["esca"]
                    # Assume all test esca images have anomalies. Modify as needed.
                    conversation = create_conversation(description, True)
                
                else:
                    continue

                data.append({
                    "image_name": image_name,
                    "conversation": conversation
                })
    
    return data

def save_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    root_dir = "/Users/michaelrodden/Desktop/ESCA_images/grapeleaf_images"
    output_path = "grapeleaves_instruction_data.json"
    
    data = process_images(root_dir)
    save_to_json(data, output_path)
    
    print(f"JSON file created at {output_path}")
