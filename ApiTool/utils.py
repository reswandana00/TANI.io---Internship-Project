"""
Database utilities and functions for agricultural data analysis.
This module contains all the database models and utility functions 
extracted from the DB tools notebook.
"""

import os
import pandas as pd
from typing import Literal
from sqlalchemy import create_engine, Column, Integer, String, Float, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


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


# Utility Functions
def determine_region_type(input_text: str) -> Literal["kecamatan", "kabupaten", "provinsi", "unknown", "nasional"]:
    """Determine the type of region based on input text."""
    input_text = input_text.lower()

    # Keywords for kecamatan, kabupaten, and provinsi
    kecamatan_keywords = ["kecamatan", "desa", "kelurahan"]
    kabupaten_keywords = ["kabupaten"]
    kota_keywords = ["kota"]
    provinsi_keywords = ["provinsi"]
    nasional_keywords = ["nasional", "indonesia", "seluruh", "semua provinsi", "semua"]

    # Determine the region type based on keywords
    if any(keyword in input_text for keyword in kecamatan_keywords):
        return "kecamatan"
    elif any(keyword in input_text for keyword in kabupaten_keywords):
        return "kabupaten"
    elif any(keyword in input_text for keyword in kota_keywords):
        return "kota"
    elif any(keyword in input_text for keyword in provinsi_keywords):
        return "provinsi"
    elif any(keyword in input_text for keyword in nasional_keywords):
        return "nasional"
    else:
        return "unknown"


def check_region_in_database(input_text: str) -> Literal["kecamatan", "kabupaten", "provinsi", "kota", "not_found"]:
    """Check if the input text matches any region in the database."""
    session = SessionLocal()
    try:
        # Check if the input matches a provinsi
        provinsi_match = session.query(DataPanen).filter(DataPanen.provinsi.ilike(f"%{input_text}%")).first()
        if provinsi_match:
            return "provinsi"
        
        # Check if the input matches a kota
        kota_match = session.query(DataPanen).filter(DataPanen.kabupaten.ilike(f"Kota {input_text}")).first()
        if kota_match:
            return "kota"
        
        # Check if the input matches a kabupaten
        kabupaten_match = session.query(DataPanen).filter(DataPanen.kabupaten.ilike(f"%{input_text}%")).first()
        if kabupaten_match:
            return "kabupaten"

        # Check if the input matches a kecamatan
        kecamatan_match = session.query(DataPanen).filter(DataPanen.kecamatan.ilike(f"%{input_text}%")).first()
        if kecamatan_match:
            return "kecamatan"

        return "not_found"
    finally:
        session.close()


# Core Data Retrieval Functions
def get_data_nasional():
    """Get national level agricultural data."""
    session = SessionLocal()
    try:
        query = session.query(DataPanen).filter(
            DataPanen.kabupaten == "-",
            DataPanen.kecamatan == "-"
        )
        df = pd.read_sql(query.statement, session.bind)
        return df
    finally:
        session.close()


def get_data_by_provinsi(provinsi_name: str):
    """Get agricultural data by province name."""
    session = SessionLocal()
    try:
        query = session.query(DataPanen).filter(
            DataPanen.provinsi.ilike(provinsi_name),
            DataPanen.kecamatan == "-"
        )
        df = pd.read_sql(query.statement, session.bind)
        return df
    finally:
        session.close()


def get_data_by_kabupaten_kota(kabupaten_kota_name: str):
    """Get agricultural data by kabupaten/kota name."""
    session = SessionLocal()
    try:
        query = session.query(DataPanen).filter(DataPanen.kabupaten.ilike(kabupaten_kota_name))
        df = pd.read_sql(query.statement, session.bind)
        return df
    finally:
        session.close()


def get_data_by_kecamatan(kecamatan_name: str):
    """Get agricultural data by kecamatan name."""
    session = SessionLocal()
    try:
        query = session.query(DataPanen).filter(DataPanen.kecamatan.ilike(kecamatan_name))
        df = pd.read_sql(query.statement, session.bind)
        return df
    finally:
        session.close()


def get_parent_data(user_input: str):
    """Get parent data information for a given region input."""
    # Step 1: Normalize input and determine region type
    normalized_input = user_input.lower().strip()
    region_type = determine_region_type(normalized_input)

    # Step 2: If unknown, check in the database
    if region_type == "unknown":
        region_type = check_region_in_database(normalized_input)

    # Step 3: Fetch parent data based on the determined region type
    if region_type == "provinsi":
        prefixes = ["provinsi"]
        
        for prefix in prefixes:
            if normalized_input.startswith(prefix):
                normalized_input = normalized_input[len(prefix):].strip()
                break
        
        return {"provinsi": normalized_input, "parent": "nasional"}
    
    elif region_type == "kota":
        prefixes = ["kota"]
        
        for prefix in prefixes:
            if normalized_input.startswith(prefix):
                normalized_input = normalized_input[len(prefix):].strip()
                break
        
        session = SessionLocal()
        try:
            kota_data = session.query(DataPanen).filter(
                DataPanen.kabupaten.ilike(f"Kota {normalized_input}")
            ).first()
            
            if kota_data:
                return {"kota": f"Kota {normalized_input}", "provinsi": kota_data.provinsi}
            else:
                return None
        finally:
            session.close()
    
    elif region_type == "kabupaten":
        prefixes = ["kabupaten"]
        
        for prefix in prefixes:
            if normalized_input.startswith(prefix):
                normalized_input = normalized_input[len(prefix):].strip()
                break
        
        session = SessionLocal()
        try:
            kabupaten_data = session.query(DataPanen).filter(
                DataPanen.kabupaten.ilike(f"%{normalized_input}%")
            ).first()
            
            if kabupaten_data:
                return {"kabupaten": normalized_input, "provinsi": kabupaten_data.provinsi}
            else:
                return None
        finally:
            session.close()
    
    elif region_type == "kecamatan":
        prefixes = ["kecamatan"]
        
        for prefix in prefixes:
            if normalized_input.startswith(prefix):
                normalized_input = normalized_input[len(prefix):].strip()
                break
        
        session = SessionLocal()
        try:
            kecamatan_data = session.query(DataPanen).filter(
                DataPanen.kecamatan.ilike(f"%{normalized_input}%")
            ).first()
            
            if kecamatan_data:
                return {
                    "kecamatan": normalized_input,
                    "kabupaten": kecamatan_data.kabupaten,
                    "provinsi": kecamatan_data.provinsi
                }
            else:
                return None
        finally:
            session.close()
    
    elif region_type == "nasional":
        return {"nasional": "Indonesia", "parent": None}

    else:
        return None


# Main Analysis Functions
def get_data_panen(user_input: str):
    """Get agricultural data based on user input."""
    parent_data = get_parent_data(user_input)
    
    if not parent_data:
        return None
    
    if 'kecamatan' in parent_data:
        return get_data_by_kecamatan(parent_data["kecamatan"])
    elif ('kota' in parent_data or 'kabupaten' in parent_data) and 'kecamatan' not in parent_data:
        if "kota" in parent_data:
            return get_data_by_kabupaten_kota(parent_data["kota"])
        elif "kabupaten" in parent_data:
            return get_data_by_kabupaten_kota(parent_data["kabupaten"])
    elif 'provinsi' in parent_data and 'kabupaten' not in parent_data and 'kecamatan' not in parent_data:
        return get_data_by_provinsi(parent_data["provinsi"])
    elif 'nasional' in parent_data:
        return get_data_nasional()


def get_total_data_panen(user_input: str):
    """Get total agricultural data based on user input."""
    parent_data = get_parent_data(user_input)
    if 'nasional' in parent_data:
        df = get_data_nasional()
        columns_to_sum = [
            "perkiraan_panen_september", "perkiraan_panen_oktober",
            "alsintan_september", "alsintan_oktober", "bera", "penggenangan",
            "tanam", "vegetatif_1", "vegetatif_2", "max_vegetatif",
            "generatif_1", "generatif_2", "panen", "standing_crop", "luas_baku_sawah"
        ]
        total = df[columns_to_sum].sum()
        total_df = pd.DataFrame([total], columns=columns_to_sum)
        return total_df

    df = get_data_panen(user_input)
    return df.head(1) if df is not None else None


def get_wilayah_panen_tertinggi(user_input: str):
    """Get regions with highest harvest data."""
    data_to_process = get_data_panen(user_input)
    if data_to_process is None or len(data_to_process) <= 1:
        return pd.DataFrame()
    
    data_to_process = data_to_process[1:]

    if (data_to_process['kecamatan'] != '-').any():
        wilayah = data_to_process[['kecamatan', 'panen']].sort_values(by='panen', ascending=False)
    elif (data_to_process['kabupaten'] != '-').any():
        wilayah = data_to_process[['kabupaten', 'panen']].sort_values(by='panen', ascending=False)
    elif (data_to_process['provinsi'] != '-').any():
        wilayah = data_to_process[['provinsi', 'panen']].sort_values(by='panen', ascending=False)
    else:
        return pd.DataFrame()

    return wilayah.head(10)


def get_wilayah_efektifitas_alsintan(user_input: str):
    """Get regions with highest agricultural machinery effectiveness."""
    parent_data = get_parent_data(user_input)
    
    if not parent_data:
        return pd.DataFrame()

    if 'kecamatan' in parent_data:
        df = get_data_panen(user_input)
    elif 'nasional' in parent_data:
        df = get_data_panen(user_input)
    else:
        df = get_data_panen(user_input)
        if df is not None and len(df) > 1:
            df = df[1:]

    if df is None or df.empty:
        return pd.DataFrame()

    # Ensure numeric columns are correct
    numeric_cols = ['alsintan_september', 'alsintan_oktober', 'luas_baku_sawah', 'panen']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Calculate total alsintan
    df['total_alsintan'] = df['alsintan_september'] + df['alsintan_oktober']
    
    # Avoid division by zero
    df['total_alsintan'] = df['total_alsintan'].replace(0, pd.NA)
    
    # Calculate effectiveness
    df['efektivitas_luas'] = (df['luas_baku_sawah'] / df['total_alsintan']).fillna(0)
    df['efektivitas_hasil'] = (df['panen'] / df['total_alsintan']).fillna(0)
    
    # Remove rows with zero or null total_alsintan
    df = df[df['total_alsintan'].notna() & (df['total_alsintan'] > 0)]
    
    # Get top 10 most effective regions
    top10_efektif = (
        df.sort_values(by='efektivitas_hasil', ascending=False)
            [['provinsi', 'kabupaten', 'kecamatan', 'panen', 'total_alsintan', 'efektivitas_hasil']]
            .head(10)
            .reset_index(drop=True)
    )

    return top10_efektif


def get_prompt_ringkasan_data_panen(user_input: str):
    """Generate a summary prompt for agricultural data."""
    # Get total agricultural data
    total_df = get_total_data_panen(user_input)
    if total_df is None or total_df.empty:
        return "Data tidak ditemukan untuk wilayah tersebut."
    
    total_summary = total_df.to_dict(orient='records')[0]

    # Get top 5 regions with highest harvest
    wilayah_tertinggi = get_wilayah_panen_tertinggi(user_input)
    top_wilayah = wilayah_tertinggi.head(5).to_dict(orient='records') if not wilayah_tertinggi.empty else []

    # Get top 5 most effective regions in using agricultural machinery
    efektifitas_df = get_wilayah_efektifitas_alsintan(user_input)
    top_efektif = efektifitas_df.head(5).to_dict(orient='records') if not efektifitas_df.empty else []

    # Build summary narrative
    prompt = f"""
**Analisis Data Panen Wilayah: {user_input.upper()}**

**1. Total Data Panen**
- Panen September: {total_summary.get('perkiraan_panen_september', 0):,} ha
- Panen Oktober: {total_summary.get('perkiraan_panen_oktober', 0):,} ha
- Luas Baku Sawah: {total_summary.get('luas_baku_sawah', 0):,} ha
- Alsintan: {total_summary.get('alsintan_september', 0) + total_summary.get('alsintan_oktober', 0):,} unit
- Total Panen: {total_summary.get('panen', 0):,} ha

**2. Wilayah Panen Tertinggi**
"""
    for i, row in enumerate(top_wilayah, start=1):
        wilayah_nama = row.get('kecamatan') or row.get('kabupaten') or row.get('provinsi')
        prompt += f"   {i}. {wilayah_nama}: {row['panen']:,} ha\n"

    prompt += """
**3. Efektivitas Alsintan**
"""
    for i, row in enumerate(top_efektif, start=1):
        wilayah_nama = row.get('kecamatan') or row.get('kabupaten') or row.get('provinsi')
        prompt += f"   {i}. {wilayah_nama}: Panen {row['panen']:,}, Alsintan {row['total_alsintan']:,}, Efektivitas {row['efektivitas_hasil']:.2f}\n"

    return prompt.strip()


def get_data_iklim(user_input: str, bulan2="September"):
    """Get climate data based on user input."""
    session = SessionLocal()
    parent = get_parent_data(user_input)

    if not parent:
        return pd.DataFrame()

    # Determine the input and state
    if 'provinsi' in parent and parent['provinsi'] != "":
        input_val = parent['provinsi']
        state = "provinsi"
    else:
        input_val = ""
        state = "nasional"

    try:
        query = session.query(Iklim).filter(Iklim.bulan.in_([bulan2]))
        if state == "provinsi":
            query = query.filter(Iklim.provinsi.ilike(f"%{input_val}%"))
        
        df = pd.read_sql(query.statement, session.bind)

        if state == "nasional":
            columns_to_sum = ['curah_hujan', 'suhu', 'kelembaban', 'lama_penyinaran']
            summary_per_province = df.groupby('provinsi')[columns_to_sum].sum().reset_index()
            return summary_per_province
        
        df.drop(columns=['bulan'], inplace=True)
        return df
    
    finally:
        session.close()


def get_data_ksa(user_input: str):
    """Get KSA (agricultural statistics) data based on user input."""
    session = SessionLocal()
    parent = get_parent_data(user_input)

    if not parent:
        return pd.DataFrame()

    try:
        if 'kecamatan' in parent:
            input_val = parent['kabupaten']
            query = session.query(KSA).filter(KSA.kabupaten.ilike(f"%{input_val}%")).filter(KSA.bulan.in_(["September"]))
        elif 'kabupaten' in parent:
            input_val = parent['kabupaten']
            query = session.query(KSA).filter(KSA.kabupaten.ilike(f"%{input_val}%")).filter(KSA.bulan.in_(["September"]))
        elif 'kota' in parent:
            input_val = parent['kota']
            query = session.query(KSA).filter(KSA.kabupaten.ilike(f"%{input_val}%")).filter(KSA.bulan.in_(["September"]))
        elif 'provinsi' in parent:
            input_val = parent['provinsi']
            query = session.query(KSA).filter(KSA.provinsi.ilike(f"%{input_val}%")).filter(KSA.bulan.in_(["September"]))
        else:
            query = session.query(KSA).filter(KSA.bulan.in_(["September"]))
            
        df = pd.read_sql(query.statement, session.bind)
        return df
    finally:
        session.close()


# Chart Functions
def chart_one(user_input: str = "indonesia"):
    """Generate chart data for climate visualization."""
    df = get_data_iklim(user_input)
    
    if df.empty:
        return pd.DataFrame()
    
    if 'stasiun' not in df.columns:
        state = 'provinsi'
    else:
        state = 'stasiun'
    
    df = df[[
        state,
        'curah_hujan',
        'suhu',
        'kelembaban',
        'lama_penyinaran',
    ]].copy()

    df.rename(columns={state: 'tempat'}, inplace=True)

    if state == 'provinsi':
        pulau_mapping = {
            'Aceh': 'Sumatera', 'Sumatera Utara': 'Sumatera', 'Sumatera Barat': 'Sumatera',
            'Riau': 'Sumatera', 'Kepulauan Riau': 'Sumatera', 'Jambi': 'Sumatera',
            'Bengkulu': 'Sumatera', 'Lampung': 'Sumatera', 'Sumatera Selatan': 'Sumatera',
            'Bangka Belitung': 'Sumatera',

            'Banten': 'Jawa', 'DKI Jakarta': 'Jawa', 'Jawa Barat': 'Jawa',
            'Jawa Tengah': 'Jawa', 'DI Yogyakarta': 'Jawa', 'Jawa Timur': 'Jawa',

            'Bali': 'Bali & Nusa Tenggara', 'NTB': 'Bali & Nusa Tenggara', 'NTT': 'Bali & Nusa Tenggara',

            'Kalimantan Barat': 'Kalimantan', 'Kalimantan Tengah': 'Kalimantan',
            'Kalimantan Selatan': 'Kalimantan', 'Kalimantan Timur': 'Kalimantan',
            'Kalimantan Utara': 'Kalimantan',

            'Sulawesi Utara': 'Sulawesi', 'Sulawesi Tengah': 'Sulawesi',
            'Sulawesi Selatan': 'Sulawesi', 'Sulawesi Tenggara': 'Sulawesi',
            'Sulawesi Barat': 'Sulawesi', 'Gorontalo': 'Sulawesi',

            'Maluku': 'Maluku & Papua', 'Maluku Utara': 'Maluku & Papua',
            'Papua': 'Maluku & Papua', 'Papua Barat': 'Maluku & Papua'
        }

        df['pulau'] = df['tempat'].map(pulau_mapping)
        df = df.groupby('pulau', as_index=False).sum()
        df.drop(columns=['tempat'], inplace=True)
        df.rename(columns={'pulau': 'tempat'}, inplace=True)

    return df


def chart_two(user_input: str = "indonesia"):
    """Generate chart data for harvest regions visualization."""
    df = get_wilayah_panen_tertinggi(user_input)

    if df.empty:
        return pd.DataFrame()

    if 'kecamatan' in df.columns and (df['kecamatan'] != '-').any():
        df.loc[:, 'wilayah'] = df['kecamatan']
    elif 'kabupaten' in df.columns and (df['kabupaten'] != '-').any():
        df.loc[:, 'wilayah'] = df['kabupaten']
    elif 'provinsi' in df.columns and (df['provinsi'] != '-').any():
        df.loc[:, 'wilayah'] = df['provinsi']
    else:
        df.loc[:, 'wilayah'] = 'Tidak Diketahui'

    df = df[['wilayah', 'panen']]
    return df


def chart_three(user_input: str = "indonesia"):
    """Generate chart data for harvest vs KSA comparison."""
    df_panen = get_wilayah_panen_tertinggi(user_input)
    df_ksa = get_data_ksa(user_input)

    if not df_ksa.empty:
        df_ksa = df_ksa.sort_values(by='produksi_padi', ascending=False).head(10)

    return df_panen, df_ksa


def chart_four(user_input: str = "indonesia"):
    """Generate chart data for agricultural machinery effectiveness."""
    df = get_wilayah_efektifitas_alsintan(user_input)

    if df.empty:
        return pd.DataFrame()

    if 'kecamatan' in df.columns and (df['kecamatan'] != '-').any():
        state = 'kecamatan'
    elif 'kabupaten' in df.columns and (df['kabupaten'] != '-').any():
        state = 'kabupaten'
    elif 'provinsi' in df.columns and (df['provinsi'] != '-').any():
        state = 'provinsi'
    else:
        return pd.DataFrame()

    df = df[[state, 'efektivitas_hasil']].head(10)
    df.rename(columns={state: 'wilayah'}, inplace=True)
    
    return df


def chart_five(user_input: str = "indonesia"):
    """Generate chart data for general agricultural data."""
    df = get_data_panen(user_input)
    return df if df is not None else pd.DataFrame()