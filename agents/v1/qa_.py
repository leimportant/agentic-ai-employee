
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

class QAAgent:
    """
    QAAgent bertanggung jawab untuk meninjau kode, menemukan bug, dan menulis tes.
    Berperan sebagai Senior Software Architect dalam platform SaaS Agentic AI.

    Kelas ini mengintegrasikan LangChain dengan model Google Gemini untuk melakukan
    analisis kode otomatis dan menghasilkan rekomendasi perbaikan serta test case.
    """

    def __init__(self):
        """
        Menginisialisasi QAAgent.

        Memuat variabel lingkungan dari file .env (misalnya, GOOGLE_API_KEY).
        Menginisialisasi model ChatGoogleGenerativeAI dan mendefinisikan prompt
        sistem untuk memandu perilaku agen.
        """
        load_dotenv()
        google_api_key = os.getenv("GOOGLE_API_KEY")

        if not google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY tidak ditemukan di variabel lingkungan. "
                "Pastikan Anda telah mengatur kunci API di file .env Anda."
            )

        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

        # Prompt sistem yang mendefinisikan peran dan tugas QAAgent
        self.system_prompt_template = """
        Anda adalah QAAgent, seorang Senior Software Architect yang berdedikasi untuk memastikan kualitas kode tertinggi.
        Tugas Anda adalah:
        1.  **Meninjau Kode**: Lakukan tinjauan kode menyeluruh berdasarkan praktik terbaik, pola desain, dan standar arsitektur.
        2.  **Menemukan Bug**: Identifikasi potensi bug, kerentanan, inefisiensi, atau masalah logika dalam kode yang diberikan.
        3.  **Menulis Tes**: Sarankan dan tuliskan test case yang relevan (unit, integrasi, edge cases) untuk memastikan fungsionalitas dan ketahanan kode.

        Berikan respons Anda dalam format Markdown yang terstruktur dengan baik, menggunakan heading untuk setiap bagian.
        Pastikan test case disajikan dalam blok kode Python yang siap dieksekusi, menggunakan framework seperti `pytest` atau `unittest`.

        Format output yang diharapkan:

        ### Ringkasan Tinjauan Kode
        [Ringkasan umum tentang kualitas kode, kepatuhan terhadap standar, dan area untuk perbaikan.]

        ### Bug dan Potensi Masalah
        [Daftar poin-poin bug spesifik, kerentanan, atau masalah inefisiensi yang ditemukan, dengan penjelasan dan saran perbaikan.]

        ### Saran Perbaikan dan Refaktor
        [Daftar saran untuk meningkatkan kualitas kode, performa, atau desain.]

        ### Test Case yang Disarankan
        
        # Tuliskan kode Python untuk test case di sini (misalnya, menggunakan pytest atau unittest).
        # Sertakan unit test, integrasi test (jika relevan), dan edge case.
        # Pastikan test case mencakup fungsionalitas inti dan skenario abnormal.
        
        """

        # Membuat ChatPromptTemplate dari pesan sistem dan pesan pengguna yang dinamis
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt_template),
                HumanMessage(content="Tinjau kode Python berikut:\n\n{code_to_review}\n")
            ]
        )

    def run(self, code_to_review: str) -> str:
        """
        Menjalankan proses tinjauan kode, pencarian bug, dan pembuatan tes untuk kode yang diberikan.

        Args:
            code_to_review (str): Kode Python yang akan ditinjau.

        Returns:
            str: Hasil tinjauan kode, daftar bug, dan test case yang disarankan
                 dalam format Markdown yang terstruktur.
        """
        if not code_to_review or not isinstance(code_to_review, str):
            return "Error: Input 'code_to_review' harus berupa string non-kosong yang berisi kode Python."

        try:
            # Membuat rantai pemrosesan: prompt -> LLM
            chain = self.prompt_template | self.llm
            
            # Memanggil model dengan kode yang akan ditinjau
            response = chain.invoke({"code_to_review": code_to_review})
            
            # Mengembalikan konten respons dari model
            return response.content
        except Exception as e:
            # Menangkap dan melaporkan kesalahan yang mungkin terjadi selama interaksi LLM
            # Dalam lingkungan produksi, log kesalahan ini ke sistem logging.
            print(f"Error saat memproses tinjauan kode: {e}")
            return f"Terjadi kesalahan internal saat memproses tinjauan kode: {e}"

# Contoh penggunaan (opsional, hanya untuk demonstrasi bagaimana agen dapat diinstansiasi dan dijalankan)
if __name__ == "__main__":
    # Pastikan GOOGLE_API_KEY diatur di file .env atau sebagai variabel lingkungan
    # Contoh isi file .env:
    # GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

    qa_agent = QAAgent()

    sample_code_1 = """
import os

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    if len(numbers) > 0:
        return total / len(numbers)
    else:
        return 0

def get_config_value(key):
    # Ini adalah fungsi yang mengambil nilai dari variabel lingkungan
    value = os.getenv(key)
    if value:
        return value
    else:
        return "default"

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        processed = [x * 2 for x in self.data]
        return processed

    def get_first_element(self):
        return self.data[0]
"""

    sample_code_2 = """
def divide(a, b):
    return a / b

def multiply(x, y):
    return x * y
"""

    print("--- Menjalankan QAAgent untuk Kode Contoh 1 ---")
    review_result_1 = qa_agent.run(sample_code_1)
    print(review_result_1)
    print("\n" + "="*80 + "\n")

    print("--- Menjalankan QAAgent untuk Kode Contoh 2 ---")
    review_result_2 = qa_agent.run(sample_code_2)
    print(review_result_2)
    print("\n" + "="*80 + "\n")

    print("--- Menjalankan QAAgent dengan Input Kosong ---")
    error_result = qa_agent.run("")
    print(error_result)
