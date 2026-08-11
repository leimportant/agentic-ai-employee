
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.output_parsers import StrOutputParser

class ArchitectAgent:
    """
    ArchitectAgent bertanggung jawab untuk mendesain arsitektur sistem,
    arsitektur multi-tenancy, skema PostgreSQL, dan menyarankan praktik terbaik
    untuk platform SaaS Agentic AI.

    Agent ini menggunakan model ChatGoogleGenerativeAI "gemini-2.5-flash"
    untuk menghasilkan respons berdasarkan pertanyaan yang diberikan.
    """

    def __init__(self):
        """
        Menginisialisasi ArchitectAgent, memuat variabel lingkungan,
        mengatur model LLM, dan mendefinisikan rantai pemrosesan.
        """
        # Memuat variabel lingkungan dari file .env
        load_dotenv()

        # Memastikan GOOGLE_API_KEY tersedia
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY tidak ditemukan di variabel lingkungan. Pastikan file .env ada dan berisi GOOGLE_API_KEY Anda.")

        # Menginisialisasi model LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

        # Mendefinisikan template prompt untuk agent arsitek
        # Prompt ini menginstruksikan LLM tentang perannya dan format output yang diharapkan.
        self.prompt_template = PromptTemplate(
            template="""
            Anda adalah Senior Software Architect yang sangat berpengalaman khusus dalam mendesain platform SaaS Agentic AI.
            Tugas Anda adalah menyediakan desain arsitektur yang komprehensif, mempertimbangkan skalabilitas, keamanan, dan efisiensi.
            Berikan respons Anda dalam format terstruktur berikut, fokus pada kejelasan dan detail teknis.

            Pertanyaan/Kebutuhan: {question}

            ---
            Harap berikan output Anda dalam struktur berikut:

            ## 1. Ringkasan Arsitektur Sistem
            Jelaskan komponen utama, interaksi, dan teknologi yang disarankan untuk platform SaaS Agentic AI.
            Sertakan pertimbangan untuk:
            - Komponen Frontend (misalnya, Next.js, React)
            - Komponen Backend (misalnya, Python FastAPI, Go Gin)
            - Layanan AI/Agen (misalnya, LangChain, LlamaIndex, custom agents)
            - Antrian Pesan (misalnya, Kafka, RabbitMQ, SQS)
            - Penyimpanan Cache (misalnya, Redis)
            - Observability (Logging, Monitoring, Tracing - misalnya, ELK Stack, Prometheus/Grafana, OpenTelemetry)
            - CI/CD (misalnya, GitHub Actions, GitLab CI)
            - Cloud Provider (misalnya, AWS, GCP, Azure)

            ## 2. Detail Arsitektur Multi-Tenancy
            Jelaskan strategi multi-tenancy yang disarankan (misalnya, database terpisah, skema terpisah, tabel bersama dengan kolom tenant_id).
            Diskusikan pro dan kontra dari strategi yang dipilih dan bagaimana data tenant akan diisolasi dan dikelola.
            Pertimbangkan:
            - Isolasi Data
            - Keamanan
            - Skalabilitas
            - Biaya

            ## 3. Desain Skema PostgreSQL (DDL)
            Buatlah contoh DDL (Data Definition Language) PostgreSQL untuk tabel-tabel penting yang mencerminkan arsitektur multi-tenancy.
            Sertakan tabel untuk:
            - Tenants
            - Users (terkait dengan tenant)
            - Agents (terkait dengan tenant)
            - AgentRuns (log eksekusi agen, terkait dengan agen)
            Pastikan kunci primer, kunci asing, indeks, dan batasan lainnya didefinisikan dengan benar.

            sql
            -- Contoh DDL PostgreSQL
            -- CREATE TABLE ...
            

            ## 4. Praktik Terbaik yang Disarankan
            Sertakan daftar praktik terbaik yang relevan untuk pengembangan, penyebaran, dan operasi platform SaaS Agentic AI ini.
            Pertimbangkan aspek-aspek seperti:
            - Keamanan (misalnya, otentikasi, otorisasi, enkripsi)
            - Skalabilitas (misalnya, desain tanpa status, sharding, replikasi)
            - Keandalan (misalnya, penanganan kesalahan, idempotensi, backup)
            - Kinerja (misalnya, optimasi kueri, caching)
            - Manajemen Agen (misalnya, versioning, sandboxing, monitoring)
            - Manajemen Prompt (misalnya, versioning, evaluasi, guardrails)
            """,
            input_variables=["question"]
        )

        # Membuat rantai pemrosesan LangChain
        # Ini menggabungkan prompt, LLM, dan parser output menjadi satu alur kerja.
        self.chain: RunnableSequence = (
            {"question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

    def run(self, question: str) -> str:
        """
        Menjalankan agent arsitek untuk menghasilkan desain arsitektur
        berdasarkan pertanyaan atau kebutuhan yang diberikan.

        Args:
            question (str): Pertanyaan atau deskripsi kebutuhan arsitektur.

        Returns:
            str: Desain arsitektur yang dihasilkan, termasuk ringkasan sistem,
                 detail multi-tenancy, skema PostgreSQL, dan praktik terbaik.
        """
        print(f"ArchitectAgent: Menganalisis pertanyaan: '{question}'...")
        try:
            # Memanggil rantai LangChain untuk mendapatkan respons dari LLM
            response = self.chain.invoke(question)
            print("ArchitectAgent: Desain arsitektur berhasil dihasilkan.")
            return response
        except Exception as e:
            print(f"ArchitectAgent: Terjadi kesalahan saat menjalankan agent: {e}")
            return f"Error: Gagal menghasilkan desain arsitektur. Detail: {e}"

# Contoh penggunaan (opsional, untuk pengujian mandiri)
if __name__ == "__main__":
    # Pastikan file .env ada di direktori yang sama dengan GOOGLE_API_KEY=your_api_key
    # Jika tidak, inisialisasi akan gagal.

    architect_agent = ArchitectAgent()

    # Contoh pertanyaan 1: Desain dasar untuk platform agen AI
    question_1 = "Desain arsitektur awal untuk platform SaaS Agentic AI yang memungkinkan pengguna membuat dan menjalankan agen AI kustom."
    print("\n" + "="*80)
    print("Menjalankan ArchitectAgent dengan pertanyaan 1...")
    architecture_design_1 = architect_agent.run(question_1)
    print("\n--- Desain Arsitektur Dihasilkan (Pertanyaan 1) ---")
    print(architecture_design_1)
    print("="*80 + "\n")

    # Contoh pertanyaan 2: Kebutuhan spesifik dengan skalabilitas tinggi
    question_2 = "Saya membutuhkan arsitektur untuk platform agen AI yang sangat skalabel, mendukung jutaan agen, dan memprioritaskan keamanan data tenant. Fokus pada AWS."
    print("\n" + "="*80)
    print("Menjalankan ArchitectAgent dengan pertanyaan 2...")
    architecture_design_2 = architect_agent.run(question_2)
    print("\n--- Desain Arsitektur Dihasilkan (Pertanyaan 2) ---")
    print(architecture_design_2)
    print("="*80 + "\n")
