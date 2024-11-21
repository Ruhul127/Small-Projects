from flask import Flask, request, jsonify, send_file, render_template
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML template from the templates folder
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    try:
        # Get the URL data from the request
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to an in-memory file
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the QR code image as a downloadable file
        return send_file(img_io, mimetype='image/png', download_name='qrcode.png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

