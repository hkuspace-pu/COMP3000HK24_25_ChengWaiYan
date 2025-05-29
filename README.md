# Secure File Integrity Checker

## Overview
A tool to generate and verify SHA-256 hashes of files, with AES-256 encryption for stored hashes, built for the COMP3000HK Project Portfolio (BSc (Hons) in Cyber Security). The project ensures file integrity by generating cryptographic hashes and securely storing them in a SQLite database, with a user-friendly Tkinter GUI for interaction.

## Setup
1. Clone the repository: `git clone https://github.com/yanhk1215/COMP3000HK24_25.git`
2. Navigate to the directory: `cd COMP3000HK24_25`
3. Install dependencies: `pip install cryptography`
4. Ensure Python 3.8+ is installed.
5. Run the prototype: `python file_integrity_checker.py`

## Usage
1. Launch the application: `python file_integrity_checker.py`
2. **Select File:** Choose a file to generate its SHA-256 hash, which is encrypted and stored in the database.
3. **Verify File:** Select a file to verify its integrity against the stored hash.
4. **Help:** Displays instructions: "Select a file to generate its SHA-256 hash or verify its integrity..."

## Testing
- **Security:**
  - Bandit scan: No high-severity issues found.
  - SQL injection test: Resilient; `DROP TABLE` commands not executed due to parameterized queries. Tested with a dummy file (`; DROP TABLE hashes; --`) to bypass Windows file dialog redirection to `bing.com`. Invalid paths are now validated before processing. See `security_log.txt`.
- **Usability:**
  - Rated 4/5 by simulating SME usage. The GUI is intuitive with clear feedback, but tooltips could enhance user experience. See `usability_log.txt`.
- **Performance:**
  - Hash generation: Achieved ~0.1s/MB (e.g., 1MB file took 0.10s, 10MB file took 1.05s).
  - Verification: Improved to ~0.05s for 1MB files after adding an index on the `file_path` column in the database. See `performance_log.txt`.
- **Test Files Used:**
  - `test.txt`: For basic functionality and SQL injection tests.
  - `test_1mb.txt`, `test_10mb.txt`: For performance testing.

## Logs
- `integrity.log`: Logs prototype events (e.g., hash generation, verification, errors).
- `security_log.txt`: Security test results (Bandit, SQL injection).
- `usability_log.txt`: Usability test results.
- `performance_log.txt`: Performance test results.
- `test_log.txt`: General test results (e.g., database checks).

## Known Issues
- On Windows 11, entering invalid file paths (e.g., `'; DROP TABLE hashes; --`) in the Tkinter file dialog may redirect to `bing.com` due to OS-level search behavior. Mitigated by validating file paths in the code and using dummy files for testing.

## Future Improvements
- Add tooltips to the GUI for better usability.
- Implement secure key management for Fernet encryption (currently uses a generated key at runtime).
- Enhance error handling for edge cases in file selection.