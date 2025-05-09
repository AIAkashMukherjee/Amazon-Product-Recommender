import os,sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from dotenv import load_dotenv
from src.rag.recommender import recommend_products


# Load environment variables
load_dotenv()

# Initialize API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Groq API Key not found! Please check your .env file.")
    st.stop()

st.sidebar.header("Configuration")
st.sidebar.success("✅ Using Groq Llama-3 model")

# App Title with custom styling
st.markdown("<h1 style='text-align: center; color: #FF5722;'>🛒 Amazon Product Recommender</h1>", unsafe_allow_html=True)

# Instructions Section
st.markdown("""
    <h3 style='text-align: center;'>Tell me what you're looking for, and I'll help you find the best products on Amazon!</h3>
    <p style='text-align: center; color: #888;'>For example, you can say: "I want a budget laptop with good battery life."</p>
""", unsafe_allow_html=True)

# User Input for Product Query
user_query = st.text_input("What do you need?", placeholder="e.g., 'Budget laptop with good battery'", label_visibility="collapsed")

# Button to Trigger Product Recommendations
if st.button("Get Recommendations") and user_query:
    with st.spinner("🔍 Searching for best products..."):
        try:
            result = recommend_products(user_query, top_k=5)

            # Display Retrieved Products
            st.subheader("🔎 Retrieved Products")
            if result["retrieved_products"]:
                for prod in result["retrieved_products"]:
                    st.markdown(f"""
                        **{prod.get('title', 'No title')}**  
                        💰 Price: ₹{prod.get('price', 'N/A')}  
                        ⭐ Rating: {prod.get('rating', 'N/A')}/5  
                     
                        ---  
                    """)
            else:
                st.warning("No products found for your query. Please try a different search.")

            # Display AI Generated Recommendations
            st.subheader("🤖 AI Recommendation")
            if result["recommendation"]:
                st.markdown(f"**{result['recommendation']}**")
             
            else:
                st.warning("No AI recommendations found.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer Section
st.markdown("---")
st.markdown("<footer style='text-align: center; color: #888;'>Powered by AI and Amazon Product Data</footer>", unsafe_allow_html=True)

