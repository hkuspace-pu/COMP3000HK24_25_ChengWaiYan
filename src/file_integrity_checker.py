import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os
import time
import logging
from cryptography.fernet import Fernet
import sqlite3

# Configure logging
logging.basicConfig(filename='integrity.log', level=logging.INFO)

class FileIntegrityChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Integrity Checker")
        self.label = tk.Label(self.root, text="No file selected")
        self.label.pack()
        # Generate a Fernet key (for demonstration; in production, save and load securely)
        key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.conn = sqlite3.connect('hashes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hashes
                             (file_path TEXT PRIMARY KEY, hash_value TEXT)''')
        self.conn.commit()
        tk.Button(self.root, text="Select File", command=self.generate_hash).pack(pady=10)
        tk.Button(self.root, text="Verify File", command=self.verify_hash).pack(pady=10)
        tk.Button(self.root, text="Help", command=self.show_help).pack(pady=10)
        self.root.mainloop()

    def generate_hash(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if not os.path.isfile(file_path):
                messagebox.showerror("Error", "Invalid file path")
                logging.error(f"Invalid file path: {file_path}")
                return
            self.label.config(text=f"Selected: {os.path.basename(file_path)}")
            try:
                with open(file_path, 'rb') as f:
                    hasher = hashlib.sha256()
                    start_time = time.time()
                    for chunk in iter(lambda: f.read(65536), b""):
                        hasher.update(chunk)
                    hash_value = hasher.hexdigest()
                    elapsed_time = time.time() - start_time
                    logging.info(f"Hashing {file_path} took {elapsed_time:.2f} seconds")
                encrypted_hash = self.cipher.encrypt(hash_value.encode()).decode()
                self.cursor.execute("INSERT OR REPLACE INTO hashes (file_path, hash_value) VALUES (?, ?)",
                                  (file_path, encrypted_hash))
                self.conn.commit()
                self.label.config(text=f"Hash generated for {os.path.basename(file_path)}")
                logging.info(f"Hash generated for {file_path}")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found")
                logging.error(f"File not found: {file_path}")
                return
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")
                logging.error(f"Database error for {file_path}: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate hash: {e}")
                logging.error(f"Hash generation failed for {file_path}: {e}")

    def verify_hash(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if not os.path.isfile(file_path):
                messagebox.showerror("Error", "Invalid file path")
                logging.error(f"Invalid file path: {file_path}")
                return
            self.label.config(text=f"Verifying: {os.path.basename(file_path)}")
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
                        messagebox.showinfo("Verification", f"{os.path.basename(file_path)} is unchanged")
                        logging.info(f"Verification successful for {file_path}: unchanged")
                    else:
                        messagebox.showwarning("Verification", f"{os.path.basename(file_path)} has been modified")
                        logging.warning(f"Verification failed for {file_path}: modified")
                else:
                    messagebox.showwarning("Verification", f"No hash stored for {os.path.basename(file_path)}")
                    logging.warning(f"No hash found for {file_path}")
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found")
                logging.error(f"File not found: {file_path}")
                return
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")
                logging.error(f"Database error for {file_path}: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to verify hash: {e}")
                logging.error(f"Hash verification failed for {file_path}: {e}")
            self.label.config(text="Verification complete")

    def show_help(self):
        messagebox.showinfo("Help", "Select a file to generate its SHA-256 hash or verify its integrity...")

if __name__ == "__main__":
    app = FileIntegrityChecker()