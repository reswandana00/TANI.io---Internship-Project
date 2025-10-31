#!/usr/bin/env python3
"""
TANI.io Database Data Insertion Script
This script inserts agricultural data into the PostgreSQL database
"""

import os
import sys
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dev:tani@database:5432/tani_db")

# For local development, you might need to use localhost
if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    logger.warning("Using localhost database connection - make sure PostgreSQL is running locally")

# Create engine and session
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    sys.exit(1)

# Database Models
class DataPanen(Base):
    __tablename__ = 'data_panen'

    id = Column(Integer, primary_key=True, index=True)
    provinsi = Column(String, nullable=False)
    kabupaten = Column(String, nullable=False)
    kecamatan = Column(String, nullable=False)
    perkiraan_panen_september = Column(Integer, nullable=True)
    perkiraan_panen_oktober = Column(Integer, nullable=True)
    alsintan_september = Column(Integer, nullable=True)
    alsintan_oktober = Column(Integer, nullable=True)
    bera = Column(Integer, nullable=True)
    penggenangan = Column(Integer, nullable=True)
    tanam = Column(Integer, nullable=True)
    vegetatif_1 = Column(Integer, nullable=True)
    vegetatif_2 = Column(Integer, nullable=True)
    max_vegetatif = Column(Integer, nullable=True)
    generatif_1 = Column(Integer, nullable=True)
    generatif_2 = Column(Integer, nullable=True)
    panen = Column(Integer, nullable=True)
    standing_crop = Column(Integer, nullable=True)
    luas_baku_sawah = Column(Integer, nullable=True)


class Iklim(Base):
    __tablename__ = 'data_iklim'

    id = Column(Integer, primary_key=True, index=True)
    stasiun = Column(String, nullable=False)
    provinsi = Column(String, nullable=False)
    bulan = Column(String, nullable=False)
    curah_hujan = Column(Integer, nullable=True)
    suhu = Column(Integer, nullable=True)
    kelembaban = Column(Integer, nullable=True)
    lama_penyinaran = Column(Integer, nullable=True)


class KSA(Base):
    __tablename__ = 'data_ksa'

    id = Column(Integer, primary_key=True, index=True)
    provinsi = Column(String, nullable=False)
    kabupaten = Column(String, nullable=False)
    bulan = Column(String, nullable=False)
    tahun = Column(Integer, nullable=False)
    luas_panen = Column(Integer, nullable=True)
    produksi_beras = Column(Integer, nullable=True)
    produksi_padi = Column(Integer, nullable=True)


def check_data_files():
    """Check if required data files exist"""
    required_files = [
        "Latest/DATA ANALISIS & TABULAR 221.csv",
        "Latest/DATA ANALISIS & TABULAR 222.csv",
        "Latest/DATA IKLIM.csv",
        "Latest/DATA KSA.csv"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"Missing data files: {missing_files}")
        return False
    
    logger.info("All required data files found")
    return True


def create_tables():
    """Create database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        return False


def load_panen_data():
    """Load and process agricultural data"""
    logger.info("Loading agricultural data...")
    
    try:
        # Load the two data files
        df_221 = pd.read_csv("Latest/DATA ANALISIS & TABULAR 221.csv")
        df_222 = pd.read_csv("Latest/DATA ANALISIS & TABULAR 222.csv")
        
        # Fill missing values
        df_221 = df_221.fillna({'Kabupaten': '-', 'Kecamatan': '-'})
        df_222 = df_222.fillna({'Kabupaten': '-', 'Kecamatan': '-'})
        
        # Define numeric columns
        numeric_columns = [
            'Perkiraan Panen Bulan September',
            'Perkiraan Panen Bulan Oktober',
            'Alsintan September',
            'Alsintan Oktober',
            'Bera',
            'Penggenangan',
            'Tanam (1-15 Hst)',
            'Vegetatif 1 (16-30 Hst)',
            'Vegetatif 2 (31-40 Hst)',
            'Max Vegetatif (41-54 Hst)',
            'Generatif 1 (55-71 Hst)',
            'Generatif 2 (72-110 Hst)',
            'Panen',
            'Standing Crop',
            'Luas Baku Sawah (Ha)'
        ]
        
        # Convert numeric columns
        df_221[numeric_columns] = df_221[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        df_222[numeric_columns] = df_222[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        
        # Convert string columns
        for df in [df_221, df_222]:
            df['Provinsi'] = df['Provinsi'].astype(str)
            df['Kabupaten'] = df['Kabupaten'].astype(str)
            df['Kecamatan'] = df['Kecamatan'].astype(str)
        
        # Combine data (sum numeric columns)
        df_combined = df_221.copy()
        df_combined[numeric_columns] = df_221[numeric_columns] + df_222[numeric_columns]
        
        # Remove duplicates
        df_combined = df_combined.drop_duplicates()
        
        logger.info(f"Processed {len(df_combined)} agricultural records")
        return df_combined
        
    except Exception as e:
        logger.error(f"Failed to load agricultural data: {e}")
        return None


def load_iklim_data():
    """Load and process climate data"""
    logger.info("Loading climate data...")
    
    try:
        df_iklim = pd.read_csv("Latest/DATA IKLIM.csv")
        
        # Convert string columns
        df_iklim['Stasiun Meteorologi/Klimatologi/Geofisika'] = df_iklim['Stasiun Meteorologi/Klimatologi/Geofisika'].astype(str)
        df_iklim['Provinsi'] = df_iklim['Provinsi'].astype(str)
        
        # Transform to long format
        parameters = ['Curah Hujan', 'Suhu', 'Kelembaban', 'Lama Penyinaran']
        dfs = []
        
        for parameter in parameters:
            df_long = pd.melt(
                df_iklim,
                id_vars=['Stasiun Meteorologi/Klimatologi/Geofisika', 'Provinsi'],
                value_vars=[f"{parameter} - {bulan}" for bulan in [
                    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
                ]],
                var_name='Parameter-Bulan',
                value_name=parameter
            )
            df_long['Bulan'] = df_long['Parameter-Bulan'].str.extract(r'- (.+)')
            df_long = df_long.drop(columns=['Parameter-Bulan'])
            dfs.append(df_long)
        
        # Combine all DataFrames
        df_iklim_long = dfs[0]
        for df_long in dfs[1:]:
            df_iklim_long = df_iklim_long.merge(
                df_long, 
                on=['Stasiun Meteorologi/Klimatologi/Geofisika', 'Provinsi', 'Bulan'], 
                how='outer'
            )
        
        # Convert columns to proper types
        df_iklim_long['Stasiun Meteorologi/Klimatologi/Geofisika'] = df_iklim_long['Stasiun Meteorologi/Klimatologi/Geofisika'].astype(str)
        df_iklim_long['Provinsi'] = df_iklim_long['Provinsi'].astype(str)
        df_iklim_long['Bulan'] = df_iklim_long['Bulan'].astype(str)
        
        logger.info(f"Processed {len(df_iklim_long)} climate records")
        return df_iklim_long
        
    except Exception as e:
        logger.error(f"Failed to load climate data: {e}")
        return None


def load_ksa_data():
    """Load and process KSA data"""
    logger.info("Loading KSA data...")
    
    try:
        df_ksa = pd.read_csv("Latest/DATA KSA.csv")
        
        # Transform to long format
        parameters = ['Luas Panen', 'Produksi Padi', 'Produksi Beras']
        
        df_long = pd.melt(
            df_ksa,
            id_vars=['Kode Provinsi', 'Nama Provinsi', 'Kode Kab', 'Nama Kabupaten'],
            value_vars=[col for col in df_ksa.columns if any(param in col for param in parameters)],
            var_name='Parameter-Bulan-Tahun',
            value_name='Nilai'
        )
        
        # Extract parameter, month, and year
        df_long['Parameter'] = df_long['Parameter-Bulan-Tahun'].str.extract(r'^(.*?)_')[0]
        df_long['Bulan'] = df_long['Parameter-Bulan-Tahun'].str.extract(r'_(.*?)-')[0]
        df_long['Tahun'] = df_long['Parameter-Bulan-Tahun'].str.extract(r'-(\d+)$')[0]
        df_long = df_long.drop(columns=['Parameter-Bulan-Tahun'])
        
        # Pivot data
        df_pivot = df_long.pivot_table(
            index=['Kode Provinsi', 'Nama Provinsi', 'Kode Kab', 'Nama Kabupaten', 'Bulan', 'Tahun'],
            columns='Parameter',
            values='Nilai',
            aggfunc='first'
        ).reset_index()
        
        # Clean numeric data
        numeric_columns = ['Luas Panen', 'Produksi Padi', 'Produksi Beras']
        for col in numeric_columns:
            df_pivot[col] = df_pivot[col].astype(str).str.replace('.', '', regex=False).astype(int)
        
        # Map month names
        bulan_mapping = {
            'Jan': 'Januari', 'Feb': 'Februari', 'Mar': 'Maret', 'Apr': 'April',
            'Mei': 'Mei', 'Jun': 'Juni', 'Jul': 'Juli', 'Ags': 'Agustus',
            'Sep': 'September', 'Okt': 'Oktober', 'Nov': 'November', 'Des': 'Desember'
        }
        df_pivot['Bulan'] = df_pivot['Bulan'].map(bulan_mapping)
        
        # Clean province and kabupaten names
        df_pivot['Nama Provinsi'] = df_pivot['Nama Provinsi'].str.title()
        df_pivot['Nama Kabupaten'] = df_pivot['Nama Kabupaten'].str.replace(r'.* - ', '', regex=True)
        
        # Select and rename columns
        df_ksa = df_pivot[['Nama Provinsi', 'Nama Kabupaten', 'Bulan', 'Tahun', 'Luas Panen', 'Produksi Beras', 'Produksi Padi']]
        df_ksa = df_ksa.rename(columns={'Nama Provinsi': 'Provinsi', 'Nama Kabupaten': 'Kabupaten'})
        
        # Fix year format
        df_ksa['Tahun'] = df_ksa['Tahun'].replace({'24': '2024', '25': '2025'}).astype(int)
        
        # Filter out 2024 data
        df_ksa = df_ksa[df_ksa['Tahun'] != 2024]
        
        logger.info(f"Processed {len(df_ksa)} KSA records")
        return df_ksa
        
    except Exception as e:
        logger.error(f"Failed to load KSA data: {e}")
        return None


def insert_data():
    """Insert all data into database"""
    logger.info("Starting data insertion...")
    
    # Check if tables exist and are empty
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    db = SessionLocal()
    try:
        # Insert agricultural data
        df_panen = load_panen_data()
        if df_panen is not None:
            logger.info("Inserting agricultural data...")
            for index, row in df_panen.iterrows():
                record = DataPanen(
                    provinsi=row['Provinsi'],
                    kabupaten=row['Kabupaten'],
                    kecamatan=row['Kecamatan'],
                    perkiraan_panen_september=row['Perkiraan Panen Bulan September'],
                    perkiraan_panen_oktober=row['Perkiraan Panen Bulan Oktober'],
                    alsintan_september=row['Alsintan September'],
                    alsintan_oktober=row['Alsintan Oktober'],
                    bera=row['Bera'],
                    penggenangan=row['Penggenangan'],
                    tanam=row['Tanam (1-15 Hst)'],
                    vegetatif_1=row['Vegetatif 1 (16-30 Hst)'],
                    vegetatif_2=row['Vegetatif 2 (31-40 Hst)'],
                    max_vegetatif=row['Max Vegetatif (41-54 Hst)'],
                    generatif_1=row['Generatif 1 (55-71 Hst)'],
                    generatif_2=row['Generatif 2 (72-110 Hst)'],
                    panen=row['Panen'],
                    standing_crop=row['Standing Crop'],
                    luas_baku_sawah=row['Luas Baku Sawah (Ha)']
                )
                db.add(record)
            db.commit()
            logger.info(f"Successfully inserted {len(df_panen)} agricultural records")
        
        # Insert climate data
        df_iklim = load_iklim_data()
        if df_iklim is not None:
            logger.info("Inserting climate data...")
            for index, row in df_iklim.iterrows():
                record = Iklim(
                    stasiun=row['Stasiun Meteorologi/Klimatologi/Geofisika'],
                    provinsi=row['Provinsi'],
                    bulan=row['Bulan'],
                    curah_hujan=row['Curah Hujan'],
                    suhu=row['Suhu'],
                    kelembaban=row['Kelembaban'],
                    lama_penyinaran=row['Lama Penyinaran']
                )
                db.add(record)
            db.commit()
            logger.info(f"Successfully inserted {len(df_iklim)} climate records")
        
        # Insert KSA data
        df_ksa = load_ksa_data()
        if df_ksa is not None:
            logger.info("Inserting KSA data...")
            for index, row in df_ksa.iterrows():
                record = KSA(
                    provinsi=row['Provinsi'],
                    kabupaten=row['Kabupaten'],
                    bulan=row['Bulan'],
                    tahun=row['Tahun'],
                    luas_panen=row['Luas Panen'],
                    produksi_beras=row['Produksi Beras'],
                    produksi_padi=row['Produksi Padi']
                )
                db.add(record)
            db.commit()
            logger.info(f"Successfully inserted {len(df_ksa)} KSA records")
        
        logger.info("All data inserted successfully!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to insert data: {e}")
        return False
    finally:
        db.close()
    
    return True


def main():
    """Main function"""
    logger.info("Starting TANI.io database insertion process...")
    
    # Check if data files exist
    if not check_data_files():
        logger.error("Please ensure all required CSV files are in the Latest/ folder")
        return
    
    # Create tables
    if not create_tables():
        logger.error("Failed to create database tables")
        return
    
    # Insert data
    if insert_data():
        logger.info("Database insertion completed successfully!")
    else:
        logger.error("Database insertion failed!")


if __name__ == "__main__":
    main()