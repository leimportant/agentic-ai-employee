
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional

class DocumentationAgent:
    """
    DocumentationAgent bertanggung jawab untuk menghasilkan berbagai jenis dokumen teknis,
    termasuk README, dokumentasi API, dan dokumen Markdown umum.
    Agent ini bertindak sebagai Senior Software Architect yang memastikan dokumentasi
    yang dihasilkan akurat, komprehensif, dan siap produksi untuk platform SaaS Agentic AI.
    """

    def __init__(self):
        """
        Menginisialisasi DocumentationAgent.
        Memuat variabel lingkungan dan menginisialisasi model ChatGoogleGenerativeAI.
        Memastikan GOOGLE_API_KEY tersedia sebelum melanjutkan.
        """
        load_dotenv()
        # Memastikan GOOGLE_API_KEY tersedia di variabel lingkungan
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY tidak ditemukan di variabel lingkungan. "
                "Pastikan Anda telah menyetelnya di file .env atau sebagai variabel sistem."
            )

        # Inisialisasi model ChatGoogleGenerativeAI dengan model yang ditentukan
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

        # Mendefinisikan ChatPromptTemplate untuk konsistensi dalam interaksi LLM
        # SystemMessage menetapkan persona dan instruksi umum
        # HumanMessage menyediakan input dinamis dari pengguna
        self.doc_prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "Anda adalah seorang Senior Software Architect yang ahli dalam membuat dokumentasi teknis "
                        "yang jelas, ringkas, dan komprehensif. Tugas Anda adalah membuat {doc_type} berdasarkan "
                        "konteks yang diberikan. Dokumentasi harus profesional, akurat, mudah dipahami, dan "
                        "mengikuti praktik terbaik industri. Gunakan format Markdown yang sesuai untuk "
                        "jenis dokumen yang diminta. Sertakan contoh kode, struktur, atau penggunaan jika "
                        "relevan dan memungkinkan."
                    )
                ),
                HumanMessage(
                    content=(
                        "Buatkan {doc_type} untuk hal berikut: {context}. "
                        "Fokus pada poin-poin penting, persyaratan, cara penggunaan, "
                        "instalasi, konfigurasi, dan contoh jika relevan."
                    )
                ),
            ]
        )

    def _generate_documentation(self, doc_type: str, context: str) -> str:
        """
        Metode internal untuk menghasilkan dokumentasi menggunakan model LLM yang telah diinisialisasi.
        Metode ini mengikat prompt template dengan LLM dan memanggilnya untuk mendapatkan respons.

        Args:
            doc_type (str): Jenis dokumentasi yang akan dibuat (misalnya, "README", "API documentation", "Markdown document").
            context (str): Konteks atau informasi yang menjadi dasar pembuatan dokumen.

        Returns:
            str: String berisi dokumentasi yang dihasilkan oleh LLM.
        """
        try:
            # Membuat chain LangChain Expression Language (LCEL) dari prompt dan LLM
            chain = self.doc_prompt_template | self.llm
            response = chain.invoke({"doc_type": doc_type, "context": context})
            return response.content
        except Exception as e:
            # Menangani kesalahan yang mungkin terjadi selama interaksi dengan LLM
            error_message = f"Terjadi kesalahan saat menghasilkan dokumentasi untuk '{doc_type}' dengan konteks '{context}': {e}"
            print(f"ERROR: {error_message}")
            return error_message

    def run(self, question: str) -> str:
        """
        Menjalankan DocumentationAgent untuk menghasilkan dokumentasi berdasarkan pertanyaan yang diberikan.
        Agent ini akan menganalisis pertanyaan untuk mengidentifikasi jenis dokumen yang diminta
        dan konteksnya, kemudian memanggil metode internal untuk menghasilkan dokumentasi.

        Args:
            question (str): Pertanyaan atau permintaan untuk membuat dokumentasi.
                            Contoh:
                            - "Buatkan README untuk modul otentikasi pengguna yang menggunakan OAuth2 dan JWT."
                            - "Buatkan dokumentasi API untuk endpoint `/api/v1/users/{id}` yang mengelola data pengguna (CRUD)."
                            - "Buatkan dokumen Markdown tentang arsitektur mikroservis platform kita, termasuk pola komunikasi."
                            - "Jelaskan konsep Observability dalam konteks aplikasi cloud-native."

        Returns:
            str: Dokumentasi yang dihasilkan dalam format Markdown.
        """
        lower_question = question.lower()
        doc_type: str = "Markdown document" # Tipe dokumen default
        context: str = question # Konteks default adalah seluruh pertanyaan

        # Logika sederhana untuk mengidentifikasi jenis dokumen dari pertanyaan
        if "readme" in lower_question:
            doc_type = "README"
            # Mencoba mengekstrak konteks setelah frasa "readme untuk"
            if "readme untuk" in lower_question:
                context = question.split("readme untuk", 1)[1].strip()
        elif "dokumentasi api" in lower_question or "api docs" in lower_question:
            doc_type = "API documentation"
            # Mencoba mengekstrak konteks setelah frasa "dokumentasi api untuk"
            if "dokumentasi api untuk" in lower_question:
                context = question.split("dokumentasi api untuk", 1)[1].strip()
            elif "api docs untuk" in lower_question:
                context = question.split("api docs untuk", 1)[1].strip()
        elif "dokumen markdown" in lower_question or "markdown document" in lower_question:
            doc_type = "Markdown document"
            # Mencoba mengekstrak konteks setelah frasa "dokumen markdown tentang"
            if "dokumen markdown tentang" in lower_question:
                context = question.split("dokumen markdown tentang", 1)[1].strip()
            elif "markdown document tentang" in lower_question:
                context = question.split("markdown document tentang", 1)[1].strip()
        # Jika tidak ada kata kunci spesifik yang cocok, seluruh pertanyaan dianggap sebagai konteks
        # dan tipe dokumen tetap default ("Markdown document")

        # Jika konteks masih sama dengan pertanyaan asli setelah penggantian, itu berarti
        # frasa kunci tidak ditemukan, jadi kita gunakan seluruh pertanyaan sebagai konteks.
        # Ini penting untuk pertanyaan yang lebih umum seperti "Jelaskan konsep X".
        if not context or context.lower() == question.lower():
            context = question

        print(f"DEBUG: Menganalisis permintaan: Tipe Dokumen='{doc_type}', Konteks='{context}'")
        return self._generate_documentation(doc_type, context)

# Bagian ini hanya untuk pengujian lokal dan tidak akan menjadi bagian dari deployment produksi sebagai library.
# Namun, disertakan untuk menunjukkan cara penggunaan agen ini secara mandiri.
if __name__ == "__main__":
    # Pastikan Anda memiliki file .env di direktori yang sama dengan kode ini,
    # dan di dalamnya terdapat baris seperti:
    # GOOGLE_API_KEY="AIzaSy...your_gemini_api_key_here..."

    try:
        # Menginisialisasi DocumentationAgent
        documentation_agent = DocumentationAgent()

        print("\n--- Contoh 1: Membuat README untuk modul autentikasi ---")
        readme_request = "Buatkan README untuk modul otentikasi pengguna di platform SaaS Agentic AI yang menggunakan FastAPI dan PostgreSQL."
        readme_output = documentation_agent.run(readme_request)
        print(f"Permintaan:\n{readme_request}\n")
        print(f"Output:\n{readme_output}")
        print("\n" + "="*80 + "\n")

        print("\n--- Contoh 2: Membuat Dokumentasi API untuk endpoint produk ---")
        api_docs_request = "Buatkan dokumentasi API untuk endpoint REST `/api/v1/products` yang mendukung operasi GET (semua, by ID), POST, PUT, dan DELETE."
        api_docs_output = documentation_agent.run(api_docs_request)
        print(f"Permintaan:\n{api_docs_request}\n")
        print(f"Output:\n{api_docs_output}")
        print("\n" + "="*80 + "\n")

        print("\n--- Contoh 3: Membuat Dokumen Markdown tentang arsitektur mikroservis ---")
        markdown_doc_request = "Buatkan dokumen Markdown tentang pola arsitektur mikroservis Event-Driven untuk sistem pemrosesan pesanan."
        markdown_doc_output = documentation_agent.run(markdown_doc_request)
        print(f"Permintaan:\n{markdown_doc_request}\n")
        print(f"Output:\n{markdown_doc_output}")
        print("\n" + "="*80 + "\n")

        print("\n--- Contoh 4: Pertanyaan umum (akan dianggap sebagai Markdown document) ---")
        general_request = "Jelaskan perbedaan antara monolithic dan microservices architecture dalam pengembangan SaaS."
        general_output = documentation_agent.run(general_request)
        print(f"Permintaan:\n{general_request}\n")
        print(f"Output:\n{general_output}")
        print("\n" + "="*80 + "\n")

    except ValueError as e:
        print(f"Error saat menjalankan DocumentationAgent: {e}")
        print("Pastikan GOOGLE_API_KEY Anda telah disetel dengan benar di file .env.")
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga: {e}")
