import streamlit as st
import os
from encryption import load_key, encrypt_file, decrypt_file

UPLOAD_FOLDER = "uploads"
DECRYPT_FOLDER = "decrypted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPT_FOLDER, exist_ok=True)

st.title("🔐 Secure File Manager (Fernet)")

menu = st.sidebar.selectbox("Choose Action", ["Upload File", "Download File"])
key = load_key()

if menu == "Upload File":
    uploaded_file = st.file_uploader("Select a file to encrypt & upload", type=None)
    if uploaded_file:
        file_bytes = uploaded_file.read()
        encrypted_data = encrypt_file(file_bytes, key)
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name + ".enc")
        with open(save_path, "wb") as f:
            f.write(encrypted_data)
        st.success(f"✅ File encrypted and saved as {uploaded_file.name}.enc")

elif menu == "Download File":
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".enc")]
    if files:
        selected_file = st.selectbox("Select encrypted file to decrypt", files)
        if st.button("Decrypt and Download"):
            enc_path = os.path.join(UPLOAD_FOLDER, selected_file)
            with open(enc_path, "rb") as f:
                encrypted_data = f.read()
            try:
                decrypted_data = decrypt_file(encrypted_data, key)
                st.download_button("📥 Download Decrypted File",
                                   decrypted_data,
                                   file_name=selected_file.replace(".enc", ""),
                                   mime="application/octet-stream")
            except Exception as e:
                st.error("❌ Decryption failed. Possibly wrong key or corrupted file.")
    else:
        st.info("📂 No encrypted files available.")
