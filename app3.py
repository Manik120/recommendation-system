import streamlit as st
import pickle
import numpy as np

# Load preprocessed data
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Recommendation function
def recommend(book_name, top_n=4):
    if book_name not in pt.index:
        return ["Book not found in dataset."]
    
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]
    
    return [pt.index[i[0]] for i in similar_items]

# --- UI Styling ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #e3f2fd, #ffffff);
        }
        .main-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
            max-width: 700px;
            margin: auto;
        }
        .title {
            text-align: center;
            color: #2c3e50;
        }
        .recommendation {
            background-color: #f1f8e9;
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">📚 Book Recommendation System</h1>', unsafe_allow_html=True)
st.markdown('<h4 class="title">Find books similar to your favorite reads</h4><hr>', unsafe_allow_html=True)

# Book list
book_list = list(pt.index.values)

# --- Session State Init ---
if "selected_book" not in st.session_state:
    st.session_state.selected_book = book_list[0]
if "show_recs" not in st.session_state:
    st.session_state.show_recs = False

# Get valid selected index
try:
    selected_index = book_list.index(st.session_state.selected_book)
except ValueError:
    selected_index = 0

# Selectbox
selected_book = st.selectbox("📖 Choose a book:", book_list, index=int(selected_index))
st.session_state.selected_book = selected_book

# Manual recommend button
if st.button("🔍 Recommend Similar Books"):
    st.session_state.show_recs = True

# If flag is True, show recommendations
if st.session_state.show_recs:
    recommendations = recommend(st.session_state.selected_book)
    if "Book not found" in recommendations[0]:
        st.warning(recommendations[0])
    else:
        st.subheader("✨ You might also enjoy:")
        for rec in recommendations:
            if st.button(f"✅ {rec}"):
                # When a recommendation is clicked, update selection and rerun
                st.session_state.selected_book = rec
                st.session_state.show_recs = True
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


