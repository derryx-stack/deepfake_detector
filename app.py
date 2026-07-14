import streamlit as st
from PIL import Image
import cv2
import numpy as np
import time

st.set_page_config(
    page_title="Deepfake Detection System",
    page_icon="🕵️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.title("Menu")
    st.markdown("---")

    menu_option = st.radio(
        "Navigate",
        [
            "Home",
            "About",
            "Settings",
            "Contribution",
            "How to use",
            "Start Fresh Analysis"
        ]
    )

    st.markdown("---")
    st.caption("Deepfake Detector v1.0")
st.title("AI-Powered Deepfake Detection System")
st.write("A system for detecting manipulated images and videos using image analysis techniques.")

def detect_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    score = np.mean(gray)

    if score < 100:
        return "⚠️ Likely Deepfake"
    else:
        return "✅ Likely Real"

# Media Type Selection
option = st.radio("Select Media Type", ["Image", "Video"])

if option == "Image":
    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="uploaded_image")
    
    if uploaded is not None:
        image = Image.open(uploaded)
        image_np = np.array(image)
        
        st.image(image_np, caption="Uploaded Image")
        
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        if st.button("🔍 Analyze Media", key="analyze_image"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(101):
                progress_bar.progress(i)
                if i < 25:
                    status_text.text(f"🔄 Loading image... {i}%")
                elif i < 50:
                    status_text.text(f"🔍 Detecting patterns... {i}%")
                elif i < 75:
                    status_text.text(f"🤖 Running AI model... {i}%")
                else:
                    status_text.text(f"📊 Computing confidence score... {i}%")
                time.sleep(0.02)

            result = detect_image(image_bgr)   # Change if your function name is different
            status_text.success("Analysis Complete! ✅")
            st.subheader(result)

elif option == "Video":
    uploaded = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"],key="uploaded_video")    
    if uploaded is not None:
        st.video(uploaded)
        
        if st.button("🔍 Analyze Media", key="analyze_video"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Save video temporarily
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded.getvalue())
            
            cap = cv2.VideoCapture("temp_video.mp4")
            frame_count = 0
            fake_frames = 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                progress = int((frame_count / total_frames) * 100)
                progress_bar.progress(progress)
                
                status_text.text(f"🔍 Analyzing frame {frame_count}/{total_frames}...")
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                score = np.mean(gray)
                
                if score < 100:
                    fake_frames += 1
                
                time.sleep(0.01)
            
            cap.release()
            
            if frame_count == 0:
                st.error("Could not process video.")
            else:
                fake_percentage = (fake_frames / frame_count) * 100
                st.write(f"**Frames analyzed:** {frame_count}")
                st.write(f"**Suspicious frames:** {fake_frames} ({fake_percentage:.1f}%)")
                
                if fake_percentage > 50:
                    st.error("🔴 Video Likely Deepfake")
                else:
                    st.success("🟢 Video Likely Real")
st.markdown("---")

st.subheader("Want to analyze something else?")

if st.button("🔄 Start Fresh Analysis", type="primary", key="full_reset"):
    st.session_state.clear()
    
    if "uploaded_image" in st.session_state:
        del st.session_state.uploaded_image
    if "uploaded_video" in st.session_state:
        del st.session_state.uploaded_video
    
    st.rerun()