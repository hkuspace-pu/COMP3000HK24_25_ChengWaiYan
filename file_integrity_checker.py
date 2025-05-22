import hashlib
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import logging
import os

class FileIntegrityChecker:
    def __init__(self):
        # Initialize logging
        logging.basicConfig(filename='integrity.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.conn = sqlite3.connect('hashes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hashes
                            (file_path TEXT PRIMARY KEY, hash_value TEXT)''')
        self.conn.commit()
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.root = tk.Tk()
        self.root.title("Secure File Integrity Checker")
        tk.Button(self.root, text="Select File", command=self.generate_hash).pack(pady=10)
        tk.Button(self.root, text="Verify File", command=self.verify_hash).pack(pady=10)
        tk.Button(self.root, text="Help", command=self.show_help).pack(pady=10)
        self.label = tk.Label(self.root, text="Ready to select a file")
        self.label.pack(pady=10)

    def show_help(self):
        messagebox.showinfo("Help", "Select a file to generate its SHA-256 hash or verify its integrity. Hashes are stored securely with AES-256 encryption.")
        logging.info("Help button clicked")

    def generate_hash(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label.config(text=f"Selected: {os.path.basename(file_path)}")
            try:
                with open(file_path, 'rb') as f:
                    hasher = hashlib.sha256()
                    for chunk in iter(lambda: f.read(65536), b""):
                        hasher.update(chunk)
                    hash_value = hasher.hexdigest()
                encrypted_hash = self.cipher.encrypt(hash_value.encode()).decode()
                self.cursor.execute("INSERT OR REPLACE INTO hashes (file_path, hash_value) VALUES (?, ?)",
                                  (file_path, encrypted_hash))
                self.conn.commit()
                self.label.config(text=f"Hash generated for {os.path.basename(file_path)}")
                logging.info(f"Hash generated for {file_path}")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found")
                logging.error(f"File not found: {file_path}")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")
                logging.error(f"Database error for {file_path}: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate hash: {e}")
                logging.error(f"Hash generation failed for {file_path}: {e}")

    def verify_hash(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label.config(text=f"Selected: {os.path.basename(file_path)}")
            try:
                with open(file_path, 'rb') as f:
                    hasher = hashlib.sha256()
                    for chunk in iter(lambda: f.read(65536), b""):
                        hasher.update(chunk)
                    current_hash = hasher.hexdigest()
                self.cursor.execute("SELECT hash_value FROM hashes WHERE file_path = ?", (file_path,))
                result = self.cursor.fetchone()
                if result:
                    stored_hash = self.cipher.decrypt(result[0].encode()).decode()
                    if current_hash == stored_hash:
                        messagebox.showinfo("Success", "File is unchanged")
                        self.label.config(text="File is unchanged")
                        logging.info(f"Verification successful for {file_path}: unchanged")
                    else:
                        messagebox.showwarning("Warning", "File has been modified")
                        self.label.config(text="File has been modified")
                        logging.warning(f"Verification failed for {file_path}: modified")
                else:
                    messagebox.showerror("Error", "No hash found for this file")
                    self.label.config(text="No hash found")
                    logging.error(f"No hash found for {file_path}")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found")
                logging.error(f"File not found: {file_path}")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")
                logging.error(f"Database error for {file_path}: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Verification failed: {e}")
                logging.error(f"Verification failed for {file_path}: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileIntegrityChecker()
    app.run()