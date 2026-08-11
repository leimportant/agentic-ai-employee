
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Memuat variabel lingkungan dari file .env
# Ini harus dilakukan di awal untuk memastikan GOOGLE_API_KEY tersedia.
load_dotenv()

class BackendEngineerAgent:
    """
    BackendEngineerAgent bertanggung jawab untuk merancang dan menghasilkan solusi backend
    yang berfokus pada FastAPI, PostgreSQL, SQLAlchemy, REST API, dan Authentication.

    Agent ini bertindak sebagai Senior Backend Engineer yang menyediakan panduan,
    desain, dan contoh kode yang production-ready.
    """

    def __init__(self):
        """
        Menginisialisasi BackendEngineerAgent.

        Memastikan bahwa GOOGLE_API_KEY telah dimuat dari variabel lingkungan.
        Mengatur model bahasa ChatGoogleGenerativeAI dengan "gemini-2.5-flash"
        dan mengonfigurasi prompt template yang memandu perilaku agent.
        """
        # Memeriksa ketersediaan GOOGLE_API_KEY
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY tidak ditemukan di variabel lingkungan. "
                "Pastikan file .env sudah terload atau variabel diatur."
            )

        # Inisialisasi model LLM dengan suhu yang seimbang untuk kreativitas dan konsistensi
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        
        # Inisialisasi parser output untuk memastikan respons berupa string
        self.output_parser = StrOutputParser()

        # Template prompt sistem yang mendefinisikan persona dan tanggung jawab agent
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", 
                 """Anda adalah seorang Senior Backend Engineer yang sangat berpengalaman dan ahli.
                 Tugas utama Anda adalah merancang, mengembangkan, dan menyediakan solusi backend
                 yang production-ready, aman, dan skalabel.
                 
                 Fokus keahlian Anda meliputi:
                 -   **Framework Web**: FastAPI (termasuk Pydantic untuk validasi data)
                 -   **Database**: PostgreSQL
                 -   **Object-Relational Mapper (ORM)**: SQLAlchemy (dengan Alembic untuk migrasi database)
                 -   **Arsitektur API**: REST API (desain endpoint, status HTTP, dll.)
                 -   **Keamanan**: Authentication (misalnya JWT, OAuth2 dengan FastAPI Security, hashing password)
                 
                 Saat memberikan solusi, pastikan untuk:
                 1.  **Struktur Proyek**: Sarankan struktur proyek yang bersih, modular, dan mudah dikelola.
                 2.  **Praktik Terbaik**: Terapkan praktik terbaik dan pola desain yang teruji (misalnya, Dependency Injection).
                 3.  **Contoh Kode**: Berikan contoh kode Python yang fungsional, jelas, dan siap pakai jika relevan.
                 4.  **Keamanan**: Sertakan pertimbangan keamanan penting (misalnya, hashing password, validasi input, CORS).
                 5.  **Database**: Sertakan skema database (model SQLAlchemy) dengan tipe data yang tepat dan relasi.
                 6.  **Migrasi**: Sebutkan pentingnya dan penggunaan Alembic untuk manajemen migrasi database.
                 7.  **Penanganan Kesalahan**: Sertakan strategi penanganan kesalahan yang robust.
                 8.  **Skalabilitas**: Pertimbangkan aspek skalabilitas dalam desain.
                 9.  **Penjelasan**: Berikan penjelasan yang jelas, ringkas, dan komprehensif.
                 10. **Lingkungan**: Hindari hardcoding nilai sensitif; sarankan penggunaan variabel lingkungan.

                 Tanggapi setiap pertanyaan atau permintaan dengan solusi yang mendalam dan praktis,
                 seolah-olah Anda sedang memberikan panduan kepada tim developer.
                 """
                ),
                ("human", "{input}")
            ]
        )
        
        # Membuat LangChain Expression Language (LCEL) chain
        self.chain = self.prompt_template | self.llm | self.output_parser

    def run(self, input: str) -> str:
        """
        Menjalankan agent untuk menghasilkan solusi atau desain backend
        berdasarkan pertanyaan atau permintaan yang diberikan.

        Args:
            input (str): Pertanyaan atau deskripsi tugas terkait pengembangan backend.
                         Contoh: "Desain sistem autentikasi pengguna dengan JWT di FastAPI",
                         "Buat model SQLAlchemy untuk sistem e-commerce",
                         "Bagaimana cara mengimplementasikan pagination pada endpoint REST API?".

        Returns:
            str: Solusi, desain, atau contoh kode backend yang dihasilkan oleh agent.
                 Jika terjadi kesalahan, akan mengembalikan pesan error.
        """
        print(f"[BackendEngineerAgent] Menerima permintaan: '{input}'")
        try:
            # Memanggil chain untuk mendapatkan respons dari LLM
            response = self.chain.invoke({"input": input})
            print("[BackendEngineerAgent] Berhasil menghasilkan respons.")
            return response
        except Exception as e:
            # Menangani kesalahan yang mungkin terjadi selama interaksi dengan LLM
            print(f"[BackendEngineerAgent] Terjadi kesalahan saat menjalankan agent: {e}")
            return f"Error: Gagal menghasilkan respons dari LLM. Detail: {e}"

# Contoh penggunaan (untuk pengujian independen)
if __name__ == "__main__":
    # Pastikan GOOGLE_API_KEY diatur di file .env Anda atau sebagai variabel lingkungan
    # Contoh isi file .env:
    # GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

    try:
        # Inisialisasi agent
        backend_agent = BackendEngineerAgent()

        print("\n--- Skenario 1: Merancang sistem autentikasi pengguna ---")
        question1 = (
            "Desain sistem autentikasi pengguna yang lengkap untuk aplikasi FastAPI. "
            "Sertakan skema database (user, role) menggunakan SQLAlchemy, "
            "endpoint API untuk registrasi, login, dan refresh token, "
            "serta implementasi JWT (JSON Web Token) untuk otentikasi."
        )
        response1 = backend_agent.run(question1)
        print("\nRespons Agent:")
        print(response1)

        print("\n--- Skenario 2: Membuat model database untuk produk ---")
        question2 = (
            "Buat model SQLAlchemy untuk entitas 'Product' dalam sistem e-commerce. "
            "Model harus memiliki atribut seperti `id`, `name`, `description`, `price`, "
            "`stock_quantity`, dan `category_id` (foreign key ke tabel 'Category'). "
            "Sertakan juga model untuk 'Category'."
        )
        response2 = backend_agent.run(question2)
        print("\nRespons Agent:")
        print(response2)

        print("\n--- Skenario 3: Implementasi endpoint CRUD sederhana ---")
        question3 = (
            "Bagaimana cara mengimplementasikan endpoint RESTful (GET all, GET by ID, POST, PUT, DELETE) "
            "di FastAPI untuk mengelola sumber daya 'Task'? Asumsikan sudah ada model SQLAlchemy untuk Task "
            "dengan atribut `id`, `title`, `description`, `completed`."
        )
        response3 = backend_agent.run(question3)
        print("\nRespons Agent:")
        print(response3)

    except ValueError as e:
        print(f"\n[ERROR FATAL]: {e}")
        print("Pastikan GOOGLE_API_KEY telah diatur di file .env atau variabel lingkungan Anda.")
    except Exception as e:
        print(f"\n[ERROR TIDAK TERDUGA]: Terjadi kesalahan saat menjalankan contoh: {e}")
