-- Inisialisasi database untuk TANI-AI
-- Buat database dan tabel yang diperlukan

-- Tabel untuk data panen (berdasarkan model DataPanen di utils.py)
CREATE TABLE IF NOT EXISTS data_panen (
    id SERIAL PRIMARY KEY,
    provinsi VARCHAR NOT NULL,
    kabupaten VARCHAR NOT NULL,
    kecamatan VARCHAR NOT NULL,
    bulan VARCHAR NOT NULL,
    tahun INTEGER NOT NULL,
    luas_tanam INTEGER,
    luas_panen INTEGER,
    luas_puso INTEGER,
    produksi_padi INTEGER,
    produksi_beras INTEGER,
    produktivitas_padi DECIMAL,
    produktivitas_beras DECIMAL,
    harga_gabah_petani INTEGER,
    harga_beras_premium INTEGER,
    harga_beras_medium INTEGER,
    curah_hujan INTEGER,
    suhu DECIMAL,
    kelembaban DECIMAL,
    lama_penyinaran DECIMAL
);

-- Tabel untuk data iklim (berdasarkan model Iklim di utils.py)
CREATE TABLE IF NOT EXISTS data_iklim (
    id SERIAL PRIMARY KEY,
    stasiun VARCHAR NOT NULL,
    provinsi VARCHAR NOT NULL,
    bulan VARCHAR NOT NULL,
    curah_hujan INTEGER,
    suhu INTEGER,
    kelembaban INTEGER,
    lama_penyinaran INTEGER
);

-- Tabel untuk data KSA (berdasarkan model KSA di utils.py)
CREATE TABLE IF NOT EXISTS data_ksa (
    id SERIAL PRIMARY KEY,
    provinsi VARCHAR NOT NULL,
    kabupaten VARCHAR NOT NULL,
    bulan VARCHAR NOT NULL,
    tahun INTEGER NOT NULL,
    luas_panen INTEGER,
    produksi_beras INTEGER,
    produksi_padi INTEGER
);

-- Insert sample data untuk testing
INSERT INTO data_panen (provinsi, kabupaten, kecamatan, bulan, tahun, luas_tanam, luas_panen, produksi_padi, produksi_beras) VALUES
('JAWA BARAT', 'BANDUNG', 'MARGAHAYU', 'JANUARI', 2024, 1000, 950, 4500, 4200),
('JAWA TENGAH', 'SEMARANG', 'GUNUNGPATI', 'FEBRUARI', 2024, 1200, 1150, 5200, 4800),
('JAWA TIMUR', 'SURABAYA', 'GUBENG', 'MARET', 2024, 800, 780, 3600, 3400),
('DI YOGYAKARTA', 'BANTUL', 'SEWON', 'APRIL', 2024, 600, 580, 2800, 2600),
('BANTEN', 'TANGERANG', 'CILEDUG', 'MEI', 2024, 900, 870, 4100, 3900);

INSERT INTO data_iklim (stasiun, provinsi, bulan, curah_hujan, suhu, kelembaban, lama_penyinaran) VALUES
('BANDUNG', 'JAWA BARAT', 'JANUARI', 250, 25, 80, 6),
('SEMARANG', 'JAWA TENGAH', 'FEBRUARI', 280, 27, 75, 7),
('SURABAYA', 'JAWA TIMUR', 'MARET', 200, 29, 70, 8),
('YOGYAKARTA', 'DI YOGYAKARTA', 'APRIL', 150, 28, 72, 7),
('TANGERANG', 'BANTEN', 'MEI', 180, 26, 78, 6);

INSERT INTO data_ksa (provinsi, kabupaten, bulan, tahun, luas_panen, produksi_beras, produksi_padi) VALUES
('JAWA BARAT', 'BANDUNG', 'JANUARI', 2024, 950, 4200, 4500),
('JAWA TENGAH', 'SEMARANG', 'FEBRUARI', 2024, 1150, 4800, 5200),
('JAWA TIMUR', 'SURABAYA', 'MARET', 2024, 780, 3400, 3600),
('DI YOGYAKARTA', 'BANTUL', 'APRIL', 2024, 580, 2600, 2800),
('BANTEN', 'TANGERANG', 'MEI', 2024, 870, 3900, 4100);
