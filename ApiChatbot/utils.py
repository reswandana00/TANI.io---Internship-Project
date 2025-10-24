import os
from typing import Annotated, Literal, List, Optional
from dotenv import load_dotenv
import aiohttp
import asyncio

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, RunContext, UsageLimits
from typing_extensions import TypedDict

from IPython.display import Image, display

load_dotenv()

# Configuration
base_url = os.getenv("API_TOOL_URL", "http://tool-api-container:8011")

import nest_asyncio
nest_asyncio.apply()

# Test API connection
async def test_api_connection():
    """Test if the tool API is accessible"""
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    return True
                else:
                    print(f"API health check failed: HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"API connection test failed: {e}")
        return False

# TOOLS
from datetime import datetime
import dateparser

def parse_time(user_input: str) -> str:
    parsed_date = dateparser.parse(user_input, settings={'PREFER_DATES_FROM': 'future'})
    if parsed_date:
        return parsed_date.strftime("%B %Y")
    return None

def cek_date(user_input: str):
    time = parse_time(user_input)
    if time:
        return time
    return datetime.now().strftime("%B %Y")

# CLASSES

class Intent(BaseModel):
    needs: Literal[
        'analyze_data_panen',
        'analyze_chart',
        'normal_mode'
    ] = Field(
        ...,
        description='''
        kebutuhan user untuk diproses ke agent yang spesifik
        - analyze_data_panen untuk kebutuhan user yang ingin mendapatkan data panen dalam bentuk tabel jika user spesifik minta penjelasan **Data Panen**
        - analyze_chart untuk kebutuhan user yang ingin mendapatkan analisis tentang yang ditampilkan jika user spesifik minta penjelasan **Chart**
        - normal_mode untuk kebutuhan user yang hanya ingin bertanya sedikit tentang analisis kecil untuk panen atau chart atau hanya test
        ''',
    )
    location: None | List[str] = Field(
        ...,
        description='jika terdapat lokasi spesifik dari inputan user',
    )
    date: None | List[str] = Field(
        ...,
        description='jika terdapat waktu spesifik dari inputan user jika tahun tidak sebut berarti tahun sekarang',
    )
    chart: None | Literal[1, 2, 3, 4, 5] = Field(
        None,
        description="jika terdapat chart spesifik, jika tidak sesuai None",
    )
    information: str = Field(description='penjelasan singkat dari kebutuhan user')

    @field_validator('chart', mode='before')
    def convert_chart_str_to_int(cls, v):
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v


class AnalyzeDataPanenState(TypedDict):
    data: Intent
    result: str

class State(TypedDict):
    input: Annotated[list, add_messages]
    
    route: str
    target_information: str
    target_location: str | None
    target_date: str | None
    target_chart: int | None
    
    output: str

state_intent_agent = Agent(
    'google-gla:gemini-2.0-flash-lite', 
    model_settings={'temperature': 0.05,"max_tokens": 100},
    output_type=Intent, 
    system_prompt=(
       "parsing kemauan user sebagai intent untuk memanggil agent yang spesifik",
       "jika ada daerah, masukkan ke location",
       "jika ada waktu, masukkan ke time",
       "berikan penjelasan singkat tentang kemauan user"
    ),
    tools=[cek_date]
)

sumarizer_agent = Agent(
    'google-gla:gemini-2.0-flash-lite', 
    model_settings={'temperature': 1.1,"max_tokens": 1000, 'verbosity': 'low'},
    system_prompt=(
       "Simpulkan informasi yang didapatkan menjadi kesimpulan komprehensif, mudah dimengerti, dan singkat",
       "Jika ada hubungan antara data, jelaskan hubungannya terutama kaitan dengan hasil padi dan iklim",
       "Buat dalam format MD yang terstruktur dengan mudah dibaca maximal 300 kata",
    ),
)

chart_explainer_agent = Agent(
    'google-gla:gemini-2.0-flash-lite', 
    model_settings={'temperature': 1.2,"max_tokens": 1000, 'verbosity': 'low'},
    system_prompt=(
       "Baca data yang digunakan untuk menampilkan chart spesifik",
       "Analisis data chart tersebut dan jelaskan secara komprehensif, mudah dimengerti, dan singkat untuk menjelaskan apa yang digambarkan pada chart tersebut",
       "Buat dalam format MD yang terstruktur dengan mudah dibaca maximal 300 kata",
    ),
)

import aiohttp
import asyncio

async def get_data_panen_prompt_summary(location: Optional[str] = None):
    endpoint = "/api/data/ringkasan"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {}).get("summary", "No summary available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"


async def get_data_total_panen(location: Optional[str] = None):
    endpoint = "/api/data/total-panen"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

async def get_data_wilayah_panen_tertinggi(location: Optional[str] = None):
    endpoint = "/api/data/wilayah-panen-tertinggi"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_data_wilayah_efektif_alsintan(location: Optional[str] = None):
    endpoint = "/api/data/efektifitas-alsintan"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_parent_data(location: Optional[str] = None):
    endpoint = "/api/data/parent"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_data_panen(location: Optional[str] = None):
    endpoint = "/api/data/panen"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

async def get_data_iklim(location: Optional[str] = None):
    endpoint = "/api/data/iklim"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_data_ksa(location: Optional[str] = None):
    endpoint = "/api/data/ksa"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_chart_one(location: Optional[str] = None):
    endpoint = "/api/charts/climate"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_chart_two(location: Optional[str] = None):
    endpoint = "/api/charts/harvest-regions"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_chart_three(location: Optional[str] = None):
    endpoint = "/api/charts/harvest-vs-ksa"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
async def get_chart_four(location: Optional[str] = None):
    endpoint = "/api/charts/machinery-effectiveness"
    data = {"region": location if location else "indonesia"}

    url = f"{base_url}{endpoint}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data.get("data", "No data available")
                else:
                    return f"API error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Request timeout - API tidak merespons"
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
    
# CALLING TOOLS

def tool_cek_daerah(user_input: str):
    return cek_date(user_input)

def tool_get_iklim(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_iklim(location))
    except Exception as e:
        return f"Error getting climate data: {str(e)}"

def tool_get_ksa(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_ksa(location))
    except Exception as e:
        return f"Error getting KSA data: {str(e)}"

def tool_get_data_panen(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_panen(location))
    except Exception as e:
        return f"Error getting harvest data: {str(e)}"

def tool_get_data_panen_prompt_summary(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_panen_prompt_summary(location))
    except Exception as e:
        return f"Error getting harvest summary: {str(e)}"

def tool_get_wilayah_panen_tertinggi(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_wilayah_panen_tertinggi(location))
    except Exception as e:
        return f"Error getting top harvest regions: {str(e)}"

def tool_get_wilayah_efektif_alsintan(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_wilayah_efektif_alsintan(location))
    except Exception as e:
        return f"Error getting machinery effectiveness data: {str(e)}"

def tool_get_total_panen(location: Optional[str] = None):
    try:
        return asyncio.run(get_data_total_panen(location))
    except Exception as e:
        return f"Error getting total harvest data: {str(e)}"

def tool_get_daerah(location: Optional[str] = None):
    try:
        return asyncio.run(get_parent_data(location))
    except Exception as e:
        return f"Error getting region data: {str(e)}"

def tool_get_chart_one(location: Optional[str] = None):
    try:
        return asyncio.run(get_chart_one(location))
    except Exception as e:
        return f"Error getting chart 1 data: {str(e)}"

def tool_get_chart_two(location: Optional[str] = None):
    try:
        return asyncio.run(get_chart_two(location))
    except Exception as e:
        return f"Error getting chart 2 data: {str(e)}"

def tool_get_chart_three(location: Optional[str] = None):
    try:
        return asyncio.run(get_chart_three(location))
    except Exception as e:
        return f"Error getting chart 3 data: {str(e)}"

def tool_get_chart_four(location: Optional[str] = None):
    try:
        return asyncio.run(get_chart_four(location))
    except Exception as e:
        return f"Error getting chart 4 data: {str(e)}"

normal_mode_agent = Agent(
    'google-gla:gemini-2.0-flash-lite',
    model_settings={'temperature': 1,"max_tokens": 500, 'verbosity': 'low'},
    system_prompt=(
       "Anda adalah asisten AI yang membantu analisis data pertanian dan iklim",
       "Gunakan tools yang tersedia untuk menjawab pertanyaan tentang:",
       "- Data iklim (curah hujan, suhu, kelembaban)",
       "- Data panen padi (wilayah terbaik, total panen)",
       "- Data KSA dan efektivitas alsintan",
       "- Chart dan visualisasi data",
       "Untuk pertanyaan tentang curah hujan tertinggi, gunakan tool_find_highest_rainfall",
       "Untuk pertanyaan tentang curah hujan atau iklim, gunakan tool_get_iklim",
       "Untuk pertanyaan tentang wilayah panen, gunakan tool_get_wilayah_panen_tertinggi", 
       "Analisis data dan berikan jawaban yang informatif",
       "Jika perlu data lokasi spesifik, gunakan tool_get_daerah terlebih dahulu",
       "Buat jawaban dalam format markdown yang mudah dibaca"
    ),
    tools=[
        tool_cek_daerah,
        tool_get_iklim,
        tool_get_ksa,
        tool_get_data_panen,
        tool_get_data_panen_prompt_summary,
        tool_get_wilayah_panen_tertinggi,
        tool_get_wilayah_efektif_alsintan,
        tool_get_total_panen,
        tool_get_daerah,
        tool_get_chart_one,
        tool_get_chart_two,
        tool_get_chart_three,
        tool_get_chart_four,
    ]
)

def sum_tabular(location: str = None) -> str:
    data_panen_total = asyncio.run(get_data_total_panen(location))
    data_wilayah_panen_tertinggi = asyncio.run(get_data_wilayah_panen_tertinggi(location))
    data_wilayah_efektif_alsintan = asyncio.run(get_data_wilayah_efektif_alsintan(location))
    data_summary = asyncio.run(get_data_panen_prompt_summary(location))

    data_panen_prompt = f'''
    Data panen ini dari SIMOTANDI data yang diambil dari proses citra satelit
    Total Panen: {data_panen_total}
    Wilayah Panen Tertinggi: {data_wilayah_panen_tertinggi}
    Wilayah Efektifitas Alsintan: {data_wilayah_efektif_alsintan}
    Ringkasan Data Panen:
    {data_summary}
    '''

    return data_panen_prompt

def sum_ksa(location: str = None) -> str:
    data_ksa_total = asyncio.run(get_data_ksa(location))

    data_ksa_prompt = f'''
    KSA (Kerangka Sampling Area) adalah data yang didapatkan dari Badan Pusat Statistik (BPS) sebagai perbandingan dari data panen SIMOTANDI
    Data KSA: {data_ksa_total}
    '''
    return data_ksa_prompt

def sum_iklim(location: str = None) -> str:
    data_iklim = asyncio.run(get_data_iklim(location))

    data_iklim_prompt = f'''
    Data iklim digunakan untuk melihat kemungkinan kenapa terjadi perubahan hasil panen padi
    Data Iklim: {data_iklim}
    '''
    return data_iklim_prompt

import asyncio

def get_chart_data(chart_number: int, location: str = None):
    match chart_number:
        case 1:
            ascii_data = f"Chart dalam bentuk radar tentang cuaca pada tiap daerah {asyncio.run(get_chart_one(location))}"
        case 2:
            ascii_data = f"Chart dalam bentuk batang tentang top 10 wilayah terbaik {asyncio.run(get_chart_two(location))}"
        case 3:
            ascii_data = f"Chart dalam bentuk garis tentang perbandingan data panen dari simotandi dan KSA {asyncio.run(get_chart_three(location))}"
        case 4:
            ascii_data = f"Chart dalam bentuk pie tentang wilayah yang terbaik {asyncio.run(get_chart_four(location))}"
        case 5:
            ascii_data = f"Data panen dalam tabel {asyncio.run(get_data_panen(location))}"
        case _:
            return f"Data untuk chart {chart_number} tidak ditemukan."
    
    return f"Data untuk chart {chart_number}: {ascii_data}"


def summarize_agent(location: str = None, information: str = None) -> str:
    data_tabular = sum_tabular(location)
    data_ksa = sum_ksa(location)
    data_iklim = sum_iklim(location)

    combined_info = (
        f"{information}\n"
        f"{data_tabular}\n"
        f"{data_ksa}\n"
        f"{data_iklim}\n"
    )

    summary = sumarizer_agent.run_sync(combined_info)
    return summary.output

def explain_chart_agent(chart_number: int, information: str = None, location: str = None) -> str:
    chart_data = get_chart_data(chart_number, location)
    prompt = f'''
    {information}
    Jelaskan pada data yang digunakan pada chart
    {chart_data}
    '''

    explanation = chart_explainer_agent.run_sync(prompt)
    return explanation.output

def get_intent(state: State) -> State:
    user_input = state["input"][-1].content
    result = state_intent_agent.run_sync(user_input)
    
    state['route'] = result.output.needs
    state['target_information'] = result.output.information
    state['target_location'] = result.output.location
    state['target_date'] = result.output.date
    state['target_chart'] = result.output.chart

    return state

def router(state: State):
    if state['route'] == 'analyze_data_panen':
        return 'analyze_data_panen'
    elif state['route'] == 'analyze_chart':
        return 'analyze_chart'
    else:
        return 'normal_mode'
    
def analyze_data_panen_agent(state: State):
    location_list = state.get('target_location')
    # Handle location - convert list to string or use first item
    location_to_analyze = None
    if location_list and isinstance(location_list, list) and len(location_list) > 0:
        location_to_analyze = location_list[0]
    elif isinstance(location_list, str):
        location_to_analyze = location_list
    
    information = state.get('target_information')
    
    summary = summarize_agent(location_to_analyze, information)
    state['output'] = summary
    return state

def analyze_chart_agent(state: State):
    chart_number = state.get('target_chart')
    information = state.get('target_information')
    location_list = state.get('target_location')
    
    # Handle location - convert list to string or use first item
    location_to_analyze = None
    if location_list and isinstance(location_list, list) and len(location_list) > 0:
        location_to_analyze = location_list[0]
    elif isinstance(location_list, str):
        location_to_analyze = location_list

    summary = explain_chart_agent(chart_number, information, location_to_analyze)

    state["output"] = summary
    return state

def normal_chat_agent(state: State) -> State:
    query = state['input'][-1].content
    
    # Run the normal mode agent directly
    answer = normal_mode_agent.run_sync(query)

    state['output'] = answer.output
    return state


router_builder = StateGraph(State)

router_builder.add_node(
    "intent_node",
    get_intent,
)
router_builder.add_node(
    "analyze_data_panen_node",
    analyze_data_panen_agent,
)
router_builder.add_node(
    "analyze_chart_node",
    analyze_chart_agent,
)

router_builder.add_node(
    "normal_chat_agent",
    normal_chat_agent,
)

router_builder.add_edge(
    START,
    "intent_node",
)

router_builder.add_conditional_edges(
    "intent_node",
    router,
    {
        'analyze_data_panen': 'analyze_data_panen_node',
        'analyze_chart': 'analyze_chart_node',
        'normal_mode': 'normal_chat_agent',
    }
)

router_builder.add_edge(
    "analyze_data_panen_node",
    END,
)
router_builder.add_edge(
    "analyze_chart_node",
    END,
)
router_builder.add_edge(
    "normal_chat_agent",
    END,
)

router_workflow = router_builder.compile()

# API WRAPPER FUNCTION
def get_chat_response(message: str) -> str:
    """
    Function wrapper untuk dipanggil dari API
    Args:
        message: User input message
    Returns:
        Bot response as string
    """
    try:
        if not message or message.strip() == "":
            return "Silakan berikan pertanyaan yang ingin Anda tanyakan."
        
        result = router_workflow.invoke({
            "input": [HumanMessage(content=message.strip())],
        })
        
        response = result.get('output', 'Maaf, tidak ada respons yang dihasilkan.')
        return response if response else "Maaf, tidak ada respons yang dihasilkan."
        
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return "Maaf, sistem sedang sibuk. Silakan coba lagi dalam beberapa saat."
        elif "connection" in error_msg.lower():
            return "Maaf, terjadi masalah koneksi. Pastikan layanan API sedang berjalan."
        else:
            return f"Maaf, terjadi kesalahan: {error_msg[:100]}..."