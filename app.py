from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
from color_extraction import extract_colors
from PIL import Image  # Digunakan untuk mengubah ukuran gambar

app = Flask(__name__)
app.secret_key = 'isi_bebas'  # Dibutuhkan untuk session
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder upload ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fungsi untuk mengubah ukuran gambar
def resize_image(image_path, output_path, size=(200, 200)):
    """
    Mengubah ukuran gambar menjadi ukuran tetap (default: 200x200 piksel).
    :param image_path: Path ke file gambar asli.
    :param output_path: Path untuk menyimpan gambar yang telah diubah ukurannya.
    :param size: Tuple (lebar, tinggi) untuk ukuran baru.
    """
    with Image.open(image_path) as img:
        # Ubah ukuran gambar
        resized_img = img.resize(size)
        # Simpan gambar yang telah diubah ukurannya
        resized_img.save(output_path)

# Halaman utama (index.html)
@app.route("/")
def index():
    # Bersihkan session saat pengguna membuka halaman utama
    session.pop("images", None)
    return render_template("index.html")  # Render halaman utama

# Halaman hasil ekstraksi warna
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        # Jika ada file yang diupload dari form
        if 'file' not in request.files:
            return redirect(request.url)  # Kembali ke halaman saat ini jika tidak ada file
        files = request.files.getlist("file")  # Ambil semua file yang diupload
        images = []
        for file in files:
            if file.filename == "":
                continue  # Lewati file kosong
            filename = secure_filename(file.filename)
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resized_path = os.path.join(app.config['UPLOAD_FOLDER'], f"resized_{filename}")
            
            # Simpan gambar asli
            file.save(original_path)
            
            # Ubah ukuran gambar menjadi 200x200 piksel
            resize_image(original_path, resized_path, size=(200, 200))
            
            # Ekstraksi warna dari gambar yang telah diubah ukurannya
            try:
                colors = extract_colors(resized_path, num_colors=10)  # Ekstrak 10 warna dominan
                images.append({"filename": f"resized_{filename}", "colors": colors})
            except ValueError as e:
                print(f"Error processing image {filename}: {e}")
                continue
        
        # Simpan hasil ke session
        session["images"] = images  # Hapus data lama dan simpan data baru
        session.modified = True  # Simpan perubahan session
        return render_template("result.html", images=images)  # Render hasil langsung
    
    # Jika GET request, bersihkan session dan tampilkan halaman result.html kosong
    session.pop("images", None)
    return render_template("result.html", images=[])

# Route untuk mereset session
@app.route('/reset', methods=['POST'])
def reset():
    # Debug: Cetak isi session sebelum reset
    print("Before reset - Session:", session)

    # Hapus data gambar dari session
    if 'images' in session:
        session.pop('images', None)
        print("Images removed from session.")
    else:
        print("No images found in session.")

    # Debug: Cetak isi session setelah reset
    print("After reset - Session:", session)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(debug=True)