
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate



class ProductManagerAgent:
    """
    ProductManagerAgent bertanggung jawab untuk menghasilkan dokumen-dokumen produk esensial
    seperti Product Requirements Document (PRD), roadmap produk, user stories, dan prioritisasi fitur.
    Agent ini bertindak sebagai Product Manager Senior untuk platform SaaS Agentic AI.
    """

    def __init__(self):
        """
        Menginisialisasi ProductManagerAgent.
        Memuat variabel lingkungan, menyiapkan model LLM, dan mendefinisikan prompt template
        untuk berbagai tugas manajemen produk.
        """
        load_dotenv()
        
        # Memastikan GOOGLE_API_KEY tersedia
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY tidak ditemukan di environment variables.")

        # Inisialisasi model ChatGoogleGenerativeAI
        # Menggunakan model "gemini-2.5-flash" sesuai instruksi
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

        # Prompt template untuk Product Manager Agent
        # Prompt ini dirancang untuk memandu LLM dalam menghasilkan output yang terstruktur
        # untuk PRD, roadmap, user stories, dan prioritisasi fitur berdasarkan satu input.
        self.prompt_template = PromptTemplate(
            input_variables=["input"],
            template="""
            Anda adalah Product Manager Senior yang sangat berpengalaman untuk platform SaaS Agentic AI.
            Tugas Anda adalah menganalisis ide produk atau masalah yang diberikan dan menyusun dokumen-dokumen produk esensial.

            Berdasarkan masukan pengguna berikut, buatlah output terstruktur yang komprehensif yang mencakup:
            1.  **Product Requirements Document (PRD):**
                -   Judul Produk
                -   Visi: Apa tujuan jangka panjang produk ini?
                -   Tujuan Bisnis: Apa yang ingin dicapai produk ini bagi bisnis? (SMART goals jika memungkinkan)
                -   Target Pengguna: Siapa pengguna utama produk ini?
                -   Lingkup Fungsionalitas Utama: Daftar fitur-fitur inti dan fungsionalitas yang akan dimiliki produk.
                -   Asumsi & Kendala: Apa saja asumsi yang mendasari dan potensi kendala?
                -   Metrik Sukses: Bagaimana kita akan mengukur keberhasilan produk ini?

            2.  **Roadmap Produk (Garis Besar):**
                -   Garis besar fase-fase pengembangan (misalnya, Fase 1: MVP, Fase 2: Peningkatan, Fase 3: Ekspansi)
                -   Fitur-fitur utama yang direncanakan untuk setiap fase.
                -   Estimasi garis waktu (misalnya, Q1, Q2, Q3) atau prioritas relatif.

            3.  **User Stories:**
                -   Buat setidaknya 3-5 user story yang mewakili fungsionalitas inti dari sudut pandang pengguna.
                -   Gunakan format standar: "Sebagai [tipe pengguna], saya ingin [tujuan], sehingga [manfaat]."

            4.  **Prioritasi Fitur:**
                -   Prioritaskan fitur-fitur yang diusulkan dari PRD atau roadmap.
                -   Gunakan metode sederhana seperti High/Medium/Low atau MoSCoW (Must-have, Should-have, Could-have, Won't-have).
                -   Berikan alasan singkat untuk setiap prioritas.

            ---
            Masukan Pengguna (Ide Produk/Masalah):
            {input}
            ---

            Output Anda harus dalam format Markdown yang jelas dan mudah dibaca, dengan judul dan sub-judul yang sesuai untuk setiap bagian.
            """
        )

        # Membuat LLMChain untuk menggabungkan prompt dan model LLM
        self.chain = self.prompt_template | self.llm

    def run(self, input: str) -> str:
        """
        Menjalankan ProductManagerAgent untuk menghasilkan dokumen produk berdasarkan masukan.

        Args:
            input (str): Deskripsi ide produk atau masalah yang perlu dianalisis.

        Returns:
            str: Output yang dihasilkan oleh LLM, berisi PRD, roadmap, user stories, dan prioritisasi fitur
                 dalam format Markdown.
        """
        print(f"ProductManagerAgent: Menganalisis masukan untuk membuat dokumen produk...")
        try:
            # Memanggil LLMChain untuk mendapatkan respons
            response = self.chain.invoke({"input": input})
            # Mengembalikan konten dari respons
            return response['text']
        except Exception as e:
            print(f"ProductManagerAgent: Terjadi kesalahan saat menjalankan agent: {e}")
            return f"Error: Gagal menghasilkan dokumen produk. Detail: {e}"

# Contoh penggunaan (opsional, untuk pengujian mandiri)
if __name__ == "__main__":
    # Pastikan file .env ada di direktori yang sama atau di lokasi yang dapat diakses
    # dan berisi GOOGLE_API_KEY="YOUR_API_KEY"

    product_manager = ProductManagerAgent()

    product_idea = """
    Kami ingin membangun sebuah fitur baru untuk platform AI Agentic SaaS kami yang memungkinkan
    pengguna untuk secara otomatis menghasilkan laporan kinerja mingguan dari agen AI mereka.
    Laporan harus mencakup metrik utama seperti jumlah tugas yang diselesaikan, tingkat keberhasilan,
    waktu rata-rata per tugas, dan tren kinerja dari waktu ke waktu. Pengguna harus dapat
    mengkonfigurasi frekuensi laporan (harian/mingguan) dan penerima email.
    """

    print("\n--- Menjalankan ProductManagerAgent dengan ide produk ---")
    output_document = product_manager.run(product_idea)
    print("\n--- Output Dokumen Produk ---")
    print(output_document)

    # Contoh lain
    another_idea = """
    Platform kami perlu fitur 'Smart Task Routing' di mana tugas-tugas yang masuk secara otomatis
    dialihkan ke agen AI yang paling cocok berdasarkan keahlian, beban kerja saat ini, dan prioritas tugas.
    Sistem harus belajar dari penugasan sebelumnya dan umpan balik pengguna.
    """
    print("\n--- Menjalankan ProductManagerAgent dengan ide lain ---")
    output_document_2 = product_manager.run(another_idea)
    print("\n--- Output Dokumen Produk 2 ---")
    print(output_document_2)
