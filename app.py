import google.generativeai as genai
import requests
import streamlit as st
from PIL import Image

# Gemini APIを使用して画像のタイトルを取得する関数
def get_image_title(img):
    """
    Gemini APIを使用して画像のタイトルを取得する関数
    """
    try:
        # Gemini APIの設定
        genai.configure(api_key=API_KEY)
        # モデルを選択
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 画像を送信してタイトルを取得
        response = model.generate_content([
            "画像にふさわしいタイトルだけを出力してください。#出力例：画像のタイトル", 
            img
        ], 
        generation_config=genai.types.GenerationConfig(
            # 温度パラメータの設定
            temperature=temperature
        ), 
        stream=True)
        response.resolve()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"エラーが発生しました: {e}"

# カスタムCSSを適用する関数
def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


st.markdown('<h1 style="color: #022563">画像タイトル生成アプリ</h1>', unsafe_allow_html=True)
st.write("Gemini APIを使用して、アップロードされた画像のタイトルを生成します。")

# CSSを読み込む
load_css("styles.css")

# サイドバー
with st.sidebar.container():
    ### Gemini APIキーの入力
    API_KEY = st.text_input('APIキー', placeholder='APIキーを入力してください', type="password")
    ### Tempperature
    temperature = st.slider('Temperature', 0.0, 2.0, 1.0)
    st.divider()
    # タイトル
    st.title("画像をアップロードしてください")
    # 画像アップロード
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", width=400)

    # タイトルの初回生成（セッションに保存）
    if st.button("タイトル生成"):
        with st.spinner("タイトルを生成中..."):
            st.session_state.title = get_image_title(image)
        # タイトルを表示
        st.subheader("生成されたタイトル")
        st.success(st.session_state.title)