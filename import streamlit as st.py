import streamlit as st
from google import genai

st.set_page_config(page_title="আমার পার্সোনাল এজেন্ট", page_icon="🤖")
st.title("🤖 আমার পার্সোনাল এআই এজেন্ট")
st.write("আপনার মনের ভাব প্রকাশ করুন, কাজ গুছিয়ে নিতে বা কমান্ড দিতে বলুন!")

# API Key সেটআপ
with st.sidebar:
    api_key = st.text_input("Gemini API Key দিন:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    # এজেন্টের পার্সোনাল চরিত্র বা প্রম্পট সেট করা
    system_instruction = "তুমি একজন দক্ষ পার্সোনাল এজেন্ট। ইউজারের মনের ভাব বুঝে তার কাজ গুছিয়ে দেওয়া এবং তার কমান্ড পালন করা তোমার কাজ।"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("আজ আপনাকে কী সাহায্য করতে পারি?"):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # জেমিনি মডেলের মাধ্যমে রেসপন্স জেনারেট করা
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config={
                    "system_instruction": system_instruction
                }
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
else:
    st.info("শুরু করার জন্য বাম পাশে আপনার জেমিনি এপিআই কি দিন।")
    import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="আমার নিরাপদ পার্সোনাল এজেন্ট", page_icon="🛡️")
st.title("🛡️ আমার সুরক্ষিত পার্সোনাল এআই এজেন্ট")
st.write("আপনার মনের ভাব প্রকাশ করুন, তবে এটি সম্পূর্ণ নিরাপদ ও সুরক্ষিত নিয়মে চলবে।")

# API Key সেটআপ
with st.sidebar:
    st.header("সেটিংস")
    api_key = st.text_input("Gemini API Key দিন:", type="password")
    st.markdown("---")
    st.info("💡 এই এজেন্টের মধ্যে শক্তিশালী সুরক্ষা (Safety Filters) এবং নির্দেশনা যুক্ত করা আছে।")

if api_key:
    # জেমিনি ক্লাইন্ট ইনিশিয়ালাইজ করা
    client = genai.Client(api_key=api_key)
    
    # ১. শক্তিশালী সিস্টেম ইন্সট্রাকশন (এজেন্টের বাউন্ডারি বা গার্ড্রেইল)
    system_instruction = """
    তুমি একজন অত্যন্ত বিশ্বস্ত, বুদ্ধিমান এবং নিরাপদ পার্সোনাল এআই এজেন্ট। 
    তোমার কাজ হলো ইউজারের মনের ভাব বুঝে তার দৈনন্দিন কাজ গুছিয়ে দেওয়া এবং তার কমান্ড পালন করা।
    
    কঠোর নিয়মাবলী:
    - কখনো কোনো বেআইনি, ক্ষতিকর, হ্যাকিং রিলেটেড বা বিপজ্জনক কাজের নির্দেশনা মেনে চলবে না।
    - ইউজারের সাথে সবসময় বিনয়ী ও পেশাদার আচরণ করবে।
    - যদি কোনো কমান্ড তোমার নিরাপত্তার নীতির বাইরে যায়, তবে বিনীতভাবে তা প্রত্যাখ্যান করবে।
    """

    # ২. জেমিনির বিল্ট-ইন সেফটি সেটিংস (ক্ষতিকর কনটেন্ট ব্লক করার জন্য)
    safety_settings = [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        ),
    ]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("আজ আপনাকে কী সাহায্য করতে পারি?"):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # জেমিনি মডেলের মাধ্যমে রেসপন্স জেনারেট করা (সুরক্ষা কনফিগারেশনসহ)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    safety_settings=safety_settings,
                    temperature=0.7, # কম হলে এআই আরও নিখুঁত ও নিয়মমাফিক উত্তর দেয়
                )
            )
            
            # রেসপন্স চেক করা (যদি সেফটি ফিল্টারের কারণে ব্লক হয়ে যায়)
            if response.text:
                bot_reply = response.text
            else:
                bot_reply = "⚠️ দুঃখিত, আপনার এই প্রম্পটটি আমাদের নিরাপত্তা নীতির কারণে ব্লক করা হয়েছে।"

        except Exception as e:
            bot_reply = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
else:
    st.info("শুরু করার জন্য বাম পাশে আপনার জেমিনি এপিআই কি দিন।")