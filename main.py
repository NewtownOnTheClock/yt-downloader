import streamlit as st
import subprocess
import tempfile
import os
import re
import sys

tempfile.NamedTemporaryFile()
video_path = tempfile.gettempdir() + "/"


def check_info():
    # Access the URL from session_state
    url = st.session_state.url_input
    # Make sure to handle cases where url might be empty or not valid
    if url:
        title_print = subprocess.run(['sh', 'yt-dlp', '--print', "%(title)s", url], check=True, capture_output=True, text=True)
        title_clean = title_print.stdout.split("\n")
        title_compliled = [i for i in title_clean]
        result = subprocess.run(["sh", 'yt-dlp', '-F', url], check=True, capture_output=True, text=True)
        lines = result.stdout.split("\n")
        pattern = re.compile(r'^(\d+)\s+(\w+)\s+(\d+x\d+|\w+)\s+(.+)$')

        formats = []
        for line in lines:
            match = pattern.match(line)
            if match:
                format_code, extension, resolution, note = match.groups()
                formats.append(f'{format_code}: {extension} {resolution}')

        st.session_state.data_lst = formats
        st.session_state.title = title_compliled[0]
        return


def download_file(format_number, file_title, extention_type):
    url = st.session_state.url_input
    if url:
        output_path = f'{video_path}{file_title}.%(ext)s'
        output_path_ext = f'{video_path}{file_title}.{extention_type}'
        subprocess.run(['yt-dlp', '-f', format_number, url, '-o', output_path], check=True)

        return output_path_ext

def remove_file(file_path):
    print(f"{file_path} got removed")
    return os.remove(file_path)

st.title("YouTube Downloader")
if 'url_input' not in st.session_state:
    st.session_state.url_input = ""

if 'data_lst' not in st.session_state:
    st.session_state.data_lst = ""

if 'title' not in st.session_state:
    st.session_state.title = ""

if 'downloaded_file_path' not in st.session_state:
    st.session_state.downloaded_file_path = ""

# Use session_state to manage the input and trigger check_info without directly passing the url

url_input = st.text_input("Input the URL from Youtube", value=st.session_state.url_input, placeholder="url...", key='url_input', on_change=check_info)
col1, col2 = st.columns([0.65, 0.35])

if st.session_state.data_lst:
    format_selected = col2.selectbox("Select the wanted format", st.session_state.data_lst)
    format_number = str(format_selected).split(":")[0]
    extension_text = str(format_selected).split(" ")[1]


    output_name = col1.text_input("Input the desired output name", value=st.session_state.title)

    cola, colb, colc = st.columns([0.2, 0.6, 0.2])

    if colb.button("Download", use_container_width=True, type="primary"):
        try:
            st.session_state.downloaded_file_path = download_file(format_number, output_name, extension_text)
            with open(st.session_state.downloaded_file_path, "rb") as f:
                file_basename = os.path.basename(st.session_state.downloaded_file_path)
                st.download_button(label="Download File", data=f, file_name=file_basename, mime="application/octet-stream", on_click=remove_file(st.session_state.downloaded_file_path))


        except Exception as e:
            print(e)
            st.error("Download Failed.")



