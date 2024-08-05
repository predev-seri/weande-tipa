import streamlit as st
import requests
import lxml
from bs4 import BeautifulSoup
from cummon import request_chat_completion, print_streaming_response

def crawl_naver_science(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("div", class_="newsct_article").text.strip()
    return article

prompt_template = """
최신 과학/IT 뉴스 기사가 주어집니다.
뉴스 기사를 참고해서 요약해주세요.
객관적인 정보를 담아서 작성해주세요.
명사로 끝나는 말투로 작성해주세요. (예시- 기대된다. -> 기대됨)

아래 포맷으로 작성해주세요.
**기사의 주제를 잘 드러낼 수 있는 제목**\n
-기사 내용 요약\n
-기사 내용 요약\n
-기사 내용 요약\n
-기사 내용 요약\n
...
---
뉴스기사: {article}
---
""".strip()

st.set_page_config(
    page_title="동아리 플젝",
    page_icon="👩‍💼"
)

st.title("🔬💻 과학/IT 뉴스 요약본 생성기")
st.subheader("📝 기사 URL을 입력하면, AI가 요약본을 생성해요.")
example_url = "https://n.news.naver.com/mnews/article/018/0005802755"
auto_complete = st.checkbox("예시 보기")
with st.form("form"):
    url = st.text_input(
        "기사 URL",
        value=example_url if auto_complete else ""
    )
    submit = st.form_submit_button("제출하기")
if submit:
    if not url:
        st.error("❌ 기사 URL을 입력해 주세요.")
    if not url.startswith("https://n.news.naver.com/"):
        st.error("❌ 처리할 수 없는 URL이에요.")
    else:
        article = crawl_naver_science(url)
        prompt = prompt_template.format(article=article)
        system_role = "당신은 요약 전문 AI입니다."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)