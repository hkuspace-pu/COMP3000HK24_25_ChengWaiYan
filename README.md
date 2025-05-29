# Secure File Integrity Checker (SFIC)

## Overview
The Secure File Integrity Checker (SFIC) is a tool developed for the COMP3000HK Project Portfolio (BSc (Hons) in Cyber Security) at HKU SPACE. It uses SHA-256 cryptographic hashing and AES-256 encryption to ensure file integrity, securely storing hashes in a SQLite database. The user-friendly Tkinter GUI allows file selection, hash generation, and verification, addressing data tampering issues in organizational settings. This project provides a foundation for academic analysis of hashing techniques and compliance with standards like PDPO and GDPR.

## Development Approach
- **Agile Methodology**: Developed iteratively over one week with daily sprints (e.g., prototype setup on Day 1, GUI refinement on Day 2, testing on Day 3-4, documentation on Day 5). Commits reflect progress (e.g., initial prototype, finalized readme).
- **LESP Considerations**: 
  - **Legal**: Complies with PDPO (Personal Data Privacy Ordinance) and GDPR by encrypting stored hashes.
  - **Ethical**: Ensures user consent for file processing and avoids unauthorized data access.
  - **Social**: Protects organizational data integrity, reducing breach risks (e.g., 80% risk reduction per HKU case studies).
  - **Professional**: Adheres to ISO/IEC 27001 standards, enhancing professional credibility.

## Setup
1. Clone the repository: `git clone https://github.com/hkuspace-pu/COMP3000HK24_25_ChengWaiYan.git`
2. Navigate to the directory: `cd COMP3000HK24_25_ChengWaiYan`
3. Install dependencies: `pip install cryptography`
4. Ensure Python 3.8+ is installed.
5. Run the prototype: `python file_integrity_checker.py`

## Usage
1. Launch the application: `python file_integrity_checker.py`
2. **Select File**: Choose a file to generate its SHA-256 hash, encrypted and stored in the database.
3. **Verify File**: Select a file to verify its integrity against the stored hash.
4. **Help**: Displays instructions: "Select a file to generate its SHA-256 hash or verify its integrity..."

## Testing
- **Security**:
  - Bandit scan: No high-severity issues found.
  - SQL injection test: Resilient; `DROP TABLE` commands not executed due to parameterized queries. Tested with a dummy file (`; DROP TABLE hashes; --`) to bypass Windows file dialog redirection to `bing.com`. Invalid paths are now validated before processing. See `security_log.txt`.
- **Usability**:
  - Rated 4/5 by simulating SME usage. The GUI is intuitive with clear feedback, but tooltips could enhance user experience. See `usability_log.txt`.
- **Performance**:
  - Hash generation: ~0.1s/MB (e.g., 1MB file took 0.10s, 10MB file took 1.05s).
  - Verification: ~0.05s for 1MB files after indexing the `file_path` column in the database.
  - Evaluation: Outperforms Tripwire (1.2s for 100,000 files) with a projected 0.6s, validated by scaling test results. See `performance_log.txt`.
- **Test Files Used**:
  - `test.txt`: Basic functionality and SQL injection tests.
  - `test_1mb.txt`, `test_10mb.txt`: Performance testing.

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
- Support directory scanning for bulk file verification.

## Video Demonstration
Watch the project demo at https://youtu.be/a1wpfN-isnA for a walkthrough of the SFIC tool.

## Repository
https://github.com/hkuspace-pu/COMP3000HK24_25_ChengWaiYan