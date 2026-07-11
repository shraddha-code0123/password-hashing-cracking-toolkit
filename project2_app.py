import streamlit as st
import hashlib
import os
import itertools
import string
import time

st.set_page_config(page_title="Password Hashing & Cracking", page_icon="🔑", layout="centered")

st.title("🔑 Password Cracking & Hashing Toolkit")
st.caption("Internship Project #2 — Salting · Dictionary Attack · Brute Force | Built with Python & Streamlit")
st.markdown("---")
st.warning("**Ethics notice:** Every attack here only targets hashes generated inside this app itself. Never use cracking tools on accounts or systems you don't own.", icon="⚠️")

WORDLIST = [
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "letmein", "welcome", "monkey",
    "admin", "anime", "sunshine", "princess", "football",
    "dragon", "master", "hello", "freedom", "whatever",
    "trustno1", "shadow", "michael", "jennifer", "superman",
    "batman", "password123", "Password123", "test123", "cybersecurity"
]

tab1, tab2, tab3 = st.tabs(["🧂 Salted vs Unsalted", "📋 Dictionary Attack", "💥 Brute Force"])

# ── TAB 1: SALTING ───────────────────────────────────────────────────────────
with tab1:
    st.header("Salted vs Unsalted Password Hashing")
   
    password = st.text_input("Enter a password to compare:", value="Password123")

    if password:
        h1 = hashlib.sha256(password.encode()).hexdigest()
        h2 = hashlib.sha256(password.encode()).hexdigest()
        salt_a, salt_b = os.urandom(16), os.urandom(16)
        sh1 = hashlib.sha256(salt_a + password.encode()).hexdigest()
        sh2 = hashlib.sha256(salt_b + password.encode()).hexdigest()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ❌ Without Salt")
            st.code(f"User A:\n{h1[:40]}...")
            st.code(f"User B:\n{h2[:40]}...")
            st.error("Identical hashes! One lookup cracks both accounts.")
        with col2:
            st.markdown("### ✅ With Salt")
            st.code(f"User A:\n{sh1[:40]}...")
            st.code(f"User B:\n{sh2[:40]}...")
            st.success("Completely different! Safe even if the database leaks.")

        st.markdown("#### How salted verification works at login")
        st.code(
            "1. User registers → server generates random salt\n"
            "2. Server stores: salt + hash(salt + password)\n"
            "3. User logs in → server re-runs: hash(stored_salt + typed_password)\n"
            "4. If hashes match → login success. Plain password is never stored.",
            language="text"
        )

# ── TAB 2: DICTIONARY ATTACK ─────────────────────────────────────────────────
with tab2:
    st.header("Dictionary Attack Demo")
    
    target_pw = st.selectbox("Choose a password to 'leak' (we'll hash it, then try to crack it):", WORDLIST[:12])
    algo = st.radio("Hash algorithm:", ["sha256", "sha1", "md5"], horizontal=True)

    if st.button("▶️ Run Dictionary Attack", use_container_width=True):
        target_hash = hashlib.new(algo, target_pw.encode()).hexdigest()
        st.code(f"Target hash ({algo}): {target_hash}", language="text")
        st.markdown("Trying every password in the wordlist...")

        progress_bar = st.progress(0, text="Starting...")
        found, attempts = None, 0

        for i, word in enumerate(WORDLIST):
            attempts += 1
            progress_bar.progress((i + 1) / len(WORDLIST), text=f"Trying: `{word}`")
            time.sleep(0.05)
            if hashlib.new(algo, word.encode()).hexdigest() == target_hash:
                found = word
                break

        progress_bar.empty()

        if found:
            st.success(f"🎉 Password cracked: **'{found}'** — found in {attempts} attempt(s)!")
          

# ── TAB 3: BRUTE FORCE ───────────────────────────────────────────────────────
with tab3:
    st.header("Brute Force Attack Demo")
   
    charset = string.ascii_lowercase + string.digits
    target_pw = st.text_input("Target password (2-3 characters only):", value="b7")
    max_len = st.slider("Max length to search up to:", 1, 4, 3)

    st.markdown("#### Search space — why length matters so much")
    chart_data = {str(l): len(charset) ** l for l in range(1, 9)}
    st.bar_chart(chart_data, use_container_width=True)
    for l in range(1, 6):
        st.caption(f"Length {l}: {len(charset)**l:,} possible passwords")

    if st.button("💥 Run Brute Force", use_container_width=True):
        if len(target_pw) > max_len:
            st.error(f"Password is longer than max search length ({max_len}). Increase the slider or shorten the password.")
        else:
            target_hash = hashlib.sha256(target_pw.encode()).hexdigest()
            with st.spinner("Brute-forcing..."):
                start = time.time()
                found, attempts = None, 0
                for length in range(1, max_len + 1):
                    for combo in itertools.product(charset, repeat=length):
                        attempts += 1
                        if hashlib.sha256("".join(combo).encode()).hexdigest() == target_hash:
                            found = "".join(combo)
                            break
                    if found:
                        break
                elapsed = time.time() - start

            if found:
                st.success(f"🎉 Cracked: **'{found}'** in {attempts:,} attempts ({elapsed:.3f}s)")
                st.metric("Speed", f"{int(attempts/elapsed):,} attempts/second")
            else:
                st.error(f"Not found within length {max_len}. Tried {attempts:,} combinations.")

st.markdown("---")
st.caption("Codect Technologies Cybersecurity Internship | Project 7: Password Cracking and Hashing Algorithms")
