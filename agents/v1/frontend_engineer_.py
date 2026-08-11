
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class FrontendEngineerAgent:
    """
    Agen Insinyur Frontend yang bertanggung jawab untuk menghasilkan kode Next.js, React,
    TailwindCSS, dan shadcn/ui. Agen ini dirancang untuk beroperasi secara independen
    dan menghasilkan kode yang siap produksi berdasarkan permintaan.
    """

    def __init__(self, temperature: float = 0.7):
        """
        Menginisialisasi FrontendEngineerAgent dengan model bahasa dan konfigurasi tertentu.

        Memuat variabel lingkungan dari file .env untuk mengakses GOOGLE_API_KEY.
        Memastikan GOOGLE_API_KEY tersedia sebelum menginisialisasi model.

        Args:
            temperature (float): Parameter kreativitas model (0.0-1.0).
                                 Nilai yang lebih tinggi menghasilkan keluaran yang lebih kreatif.
        Raises:
            ValueError: Jika GOOGLE_API_KEY tidak ditemukan di variabel lingkungan.
        """
        # Memuat variabel lingkungan dari file .env
        load_dotenv()

        # Memastikan GOOGLE_API_KEY tersedia
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY tidak ditemukan di variabel lingkungan. "
                "Pastikan Anda telah menyetelnya di file .env atau lingkungan sistem Anda."
            )

        # Inisialisasi model ChatGoogleGenerativeAI
        # Menggunakan model "gemini-2.5-flash" untuk keseimbangan antara kecepatan dan kualitas.
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature)

        # Template prompt untuk agen Frontend Engineer.
        # Prompt ini dengan jelas mendefinisikan peran agen, teknologi yang digunakan,
        # dan format keluaran yang diharapkan (hanya kode).
        self.prompt_template = PromptTemplate(
            input_variables=["question"],
            template=(
                "Anda adalah seorang Senior Frontend Engineer yang sangat ahli dalam mengembangkan aplikasi web modern.\n"
                "Anda bekerja dengan teknologi inti berikut: Next.js, React, TailwindCSS, dan shadcn/ui.\n"
                "Tugas Anda adalah menghasilkan kode yang bersih, modular, dan siap produksi sesuai dengan permintaan.\n"
                "Berikan HANYA kode yang diminta, tanpa penjelasan tambahan, pengantar, atau markdown di luar blok kode "
                "(misalnya, jangan sertakan javascript atau typescript).\n"
                "Jika Anda perlu memberikan beberapa file, pisahkan dengan komentar seperti // --- FILE: components/Button.tsx ---\n\n"
                "Berikut adalah permintaan:\n"
                "'{question}'"
            )
        )

        # Membuat rantai LLM. Ini mengikat model LLM dengan template prompt yang telah ditentukan,
        # memungkinkan eksekusi yang lebih terstruktur.
        self.chain = self.prompt_template | self.llm

    def run(self, question: str) -> str:
        """
        Menjalankan agen untuk menghasilkan kode frontend berdasarkan pertanyaan yang diberikan.

        Metode ini mengambil pertanyaan dalam Bahasa Indonesia, memprosesnya menggunakan
        model AI yang dikonfigurasi, dan mengembalikan string yang berisi kode frontend
        yang dihasilkan.

        Args:
            question (str): Pertanyaan atau instruksi dalam Bahasa Indonesia untuk pembuatan kode frontend.
                            Contoh: "Buatkan saya komponen React untuk tombol 'Login'..."

        Returns:
            str: Kode frontend yang dihasilkan dalam format string. Jika terjadi kesalahan,
                 mengembalikan pesan kesalahan yang informatif.
        """
        print(f"FrontendEngineerAgent: Menerima pertanyaan: '{question}'")
        try:
            # Menjalankan rantai LLM dengan pertanyaan yang diberikan.
            # Rantai ini akan memformat pertanyaan menggunakan prompt_template
            # dan mendapatkan respons dari model Gemini.
            response = self.chain.run(question)
            print("FrontendEngineerAgent: Kode berhasil dihasilkan.")
            return response
        except Exception as e:
            # Menangani potensi kesalahan selama interaksi dengan LLM.
            print(f"FrontendEngineerAgent: Terjadi kesalahan saat menjalankan agen: {e}")
            return f"Error: Gagal menghasilkan kode frontend. Detail: {e}"

# Contoh penggunaan agen secara independen
if __name__ == "__main__":
    # Memastikan variabel lingkungan dimuat untuk skrip mandiri.
    # Ini penting agar GOOGLE_API_KEY tersedia saat agen diinisialisasi.
    load_dotenv()

    try:
        # Menginisialisasi agen Frontend Engineer dengan suhu kreativitas sedang.
        frontend_engineer = FrontendEngineerAgent(temperature=0.5)

        # Contoh pertanyaan untuk agen: membuat komponen tombol React.
        example_question_1 = (
            "Buatkan saya komponen React TypeScript untuk tombol 'Login' yang menggunakan komponen Button dari shadcn/ui. "
            "Tombol ini harus memiliki teks 'Login' di dalamnya, dan menggunakan TailwindCSS untuk styling: "
            "warna latar belakang biru (`bg-blue-600`), teks putih (`text-white`), padding horizontal `px-4`, "
            "padding vertikal `py-2`, dan sudut membulat (`rounded-md`). "
            "Sertakan juga fungsi `onClick` yang mencetak 'Login clicked!' ke konsol. "
            "Pastikan impor yang diperlukan untuk React dan shadcn/ui disertakan. "
            "Berikan hanya kode untuk komponen, tanpa penggunaan atau import diluar komponen."
        )

        # Menjalankan agen dengan pertanyaan pertama dan menampilkan hasilnya.
        print("\n--- Meminta Kode Komponen Tombol 'Login' ---")
        generated_code_1 = frontend_engineer.run(example_question_1)
        print("\n--- KODE FRONTEND YANG DIHASILKAN (Komponen Tombol) ---")
        print(generated_code_1)
        print("------------------------------------------------------\n")

        # Contoh pertanyaan lain: membuat halaman Next.js dengan daftar item.
        example_question_2 = (
            "Buatkan saya halaman Next.js (`app/page.tsx`) yang menampilkan daftar 3 item. "
            "Gunakan komponen Card dari shadcn/ui untuk setiap item. Setiap Card harus memiliki judul dan deskripsi. "
            "Gunakan TailwindCSS untuk menata tata letak halaman agar daftar ditampilkan dalam grid 3 kolom pada layar besar. "
            "Berikan hanya kode untuk `page.tsx`."
        )

        # Menjalankan agen dengan pertanyaan kedua dan menampilkan hasilnya.
        print("\n--- Meminta Kode Halaman Next.js dengan Card ---")
        generated_code_2 = frontend_engineer.run(example_question_2)
        print("\n--- KODE FRONTEND YANG DIHASILKAN (Halaman Next.js) ---")
        print(generated_code_2)
        print("------------------------------------------------------\n")

    except ValueError as ve:
        # Menangkap kesalahan konfigurasi, seperti GOOGLE_API_KEY yang hilang.
        print(f"Error konfigurasi: {ve}")
    except Exception as e:
        # Menangkap kesalahan umum lainnya yang mungkin terjadi.
        print(f"Terjadi kesalahan tak terduga: {e}")

