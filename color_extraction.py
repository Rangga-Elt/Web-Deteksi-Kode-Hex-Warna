from sklearn.cluster import KMeans
import cv2
import numpy as np
import matplotlib.colors as mcolors

def adjust_brightness_contrast(image, alpha=1.5, beta=30):
    """
    Menyesuaikan kecerahan dan kontras gambar.
    - Alpha (>1 meningkatkan kontras, <1 menguranginya).
    - Beta menambah/mengurangi kecerahan (positif untuk lebih terang, negatif untuk lebih gelap).
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def extract_colors(image_path, num_colors=10):
    """
    Mengekstraksi warna dominan dari gambar menggunakan K-Means Clustering.
    :param image_path: Path ke file gambar.
    :param num_colors: Jumlah warna dominan yang ingin diekstraksi.
    :return: List tuple (kode warna HEX, persentase kemunculan).
    """
    # Baca gambar menggunakan OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Gambar tidak dapat dibaca dari path: {image_path}")
    
    # Konversi gambar ke format RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Cek kecerahan rata-rata gambar
    brightness = np.mean(image)
    if brightness < 50:  # Gambar terlalu gelap
        image = adjust_brightness_contrast(image, alpha=1.8, beta=50)
    elif brightness > 200:  # Gambar terlalu terang
        image = adjust_brightness_contrast(image, alpha=0.8, beta=-30)
    
    # Ubah gambar menjadi array 2D (pixel, RGB)
    image = image.reshape((-1, 3))
    
    # Gunakan K-Means Clustering untuk menemukan warna dominan
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(image)
    
    # Ambil warna dominan (pusat cluster) dan hitung persentase kemunculannya
    colors = kmeans.cluster_centers_.astype(int)  # Warna RGB dominan
    percentages = np.bincount(kmeans.labels_) / len(kmeans.labels_) * 100  # Persentase tiap warna
    
    # Konversi warna RGB ke format HEX
    extracted_colors = [
        (mcolors.to_hex(color / 255.0), round(percent, 2))  # RGB ke HEX, persentase dibulatkan
        for color, percent in zip(colors, percentages)
    ]
    
    # Urutkan hasil berdasarkan persentase terbesar ke terkecil
    extracted_colors.sort(key=lambda x: x[1], reverse=True)
    
    return extracted_colors