from flask import Flask, jsonify, request
import base64
from rembg import remove, new_session
import os
from PIL import Image
import io
import logging
import numpy as np

app = Flask(__name__)

# This is used to indicate if the server is running or not
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'The service is running!'})


# This is used to remove the background from the image
@app.route('/remove', methods=['POST'])
def remove_bg():
    # we still need the parameters to choose the model.
    data = request.get_json()
    try:
        encoded_image = data['input_image']
    except KeyError:
        return jsonify({'error':'You must provide the input image.'})
    
    model = data.get('model', 'u2net')
    if model not in {"u2net", "u2netp",
                     "u2net_human_seg", 
                     "u2net_cloth_seg",
                     "silueta"}:
        return jsonify({'error':'You must provide a valid model.'})
    session = new_session(model)
    # Decode the base64-encoded image
    decoded_image = base64.b64decode(encoded_image)
    # Use the `PIL` module to create an image from the decoded data
    image = Image.open(io.BytesIO(decoded_image))
    
    logging.info("removal started")
    output = remove(image, session=session)
    logging.info("removal finished")
    
    #----------------------------------------------------------------#
    #         Replace the transparent part into white background.    #
    #----------------------------------------------------------------#
    img_rmbg = np.asarray(output)
    # Split RGBA to RGB and Alpha
    rgb_rmbg = img_rmbg[...,0:3]
    alpha_rmbg = img_rmbg[..., -1:]
    
    # Paste the image onto a white background
    white_background = np.ones(rgb_rmbg.shape) * 255
    mask = alpha_rmbg > 125
    final_img = mask * rgb_rmbg + ~mask * white_background
    output = Image.fromarray(np.uint8(final_img))
    
    # img to base64 string
    im_bytes = io.BytesIO()
    output.save(im_bytes, format='PNG')
    im_bytes = im_bytes.getvalue()
    im_base64 = base64.b64encode(im_bytes).decode()
    
    # convert the output to base64
    return jsonify({'message': "success",
                    'output_image': im_base64})


# This is used to remove the background from the image
@app.route('/remove-opacity', methods=['POST'])
def remove_bg_opacity():
    # we still need the parameters to choose the model.
    data = request.get_json()
    try:
        encoded_image = data['input_image']
    except KeyError:
        return jsonify({'error':'You must provide the input image.'})
    
    model = data.get('model', 'u2net')
    if model not in {"u2net", "u2netp",
                     "u2net_human_seg", 
                     "u2net_cloth_seg",
                     "silueta"}:
        return jsonify({'error':'You must provide a valid model.'})
    session = new_session(model)
    # Decode the base64-encoded image
    decoded_image = base64.b64decode(encoded_image)
    # Use the `PIL` module to create an image from the decoded data
    image = Image.open(io.BytesIO(decoded_image))
    
    logging.info("removal started")
    output = remove(image, session=session)
    logging.info("removal finished")
    
    im_bytes = io.BytesIO()
    output.save(im_bytes, format='PNG')
    im_bytes = im_bytes.getvalue()
    im_base64 = base64.b64encode(im_bytes).decode()
    
    # convert the output to base64
    return jsonify({'message': "success",
                    'output_image': im_base64})




if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 4000)),
            host='0.0.0.0', debug=True)
    
    
    
    

    
    
            
    