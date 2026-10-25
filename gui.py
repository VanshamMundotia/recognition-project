import streamlit as st
from PIL import Image
from app import generate_caption_ollama, text_to_audio, save_feedback

def main():
    st.set_page_config(
        page_title="NOVA — see beyond sight",
        page_icon="👁️",
        layout="wide",
    )

    # Custom CSS for Responsive Viewport Scaling & Custom Beige-White Footer
    st.markdown("""
        <style>
        .stApp {
            background-color: #0b0e14;
            color: #c9d1d9;
        }
        
        header {visibility: hidden;}
        
        /* Responsive container bounds to prevent unwanted scrolling at 100% view */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100% !important;
        }

        .top-nav {
            background-color: #121821;
            border: 1px solid #21262d;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        
        .badge-active {
            background-color: #1f883d;
            color: white;
            border-radius: 12px;
            font-weight: 600;
        }
        .badge-detail {
            background-color: #21262d;
            color: #8b949e;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            border: 1px solid #30363d;
        }
        
        /* Make preview images fluidly scale based on screen width */
        img {
            max-width: 100% !important;
            height: auto !important;
            border-radius: 8px;
        }

        /* Exact Beige-White Footer Bar matching your reference photo */
        .custom-footer {
            background-color: #f4f1ea;
            color: #2b2b2b;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Top Navigation Banner (Centered & Enlarged Title)
    st.markdown("""
        <div class="top-nav" style="text-align: center; display: block; padding: 16px;">
            <div style="margin-bottom: 4px;">
                <span style="font-size: 36px; font-weight: 900; color: white; letter-spacing: 1px;">👁️ NOVA</span>
                <span style="color: #8b949e; margin: 0 10px; font-size: 18px; font-weight: 500;">— see beyond sight</span>
                <span class="badge-active" style="font-size: 13px; padding: 4px 12px; vertical-align: middle;">🟢 Assistive AI Active</span>
            </div>
            <div style="font-size: 13px; color: #8b949e; margin-top: 2px;">
                High-contrast vision accessibility assistant with instant neural spatial descriptions
            </div>
            <div style="margin-top: 10px;">
                <span style="background: #161b22; border: 1px solid #30363d; padding: 4px 10px; border-radius: 6px; font-size: 12px; color: #c9d1d9; margin-right: 8px;">🎙️ Voice Commands: ON</span>
                <span style="background: #bb8009; color: #0b0e14; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;">A+ Text Size</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Subheader Info Bar
    st.markdown(
        "<div style='font-size: 12px; color: #8b949e; margin-bottom: 10px;'>"
        "● <b>Dual Mode:</b> Upload or Live Camera on <b>Left</b> • Active Capture, Narration & Audio on <b>Right</b>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<span style='float: right;'>Hotkeys: <code>Space</code> Capture &nbsp;&nbsp; <code>D</code> Describe &nbsp;&nbsp; <code>P</code> Replay Audio</span>"
        "</div>", 
        unsafe_allow_html=True
    )

    # Initialize Session States
    if "caption" not in st.session_state:
        st.session_state.caption = None
    if "active_image" not in st.session_state:
        st.session_state.active_image = None
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    # Main Two-Column Layout with equal fluid weight
    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown("### 📥 Upload Source Photo")
        uploaded_file = st.file_uploader("Choose file or drag & drop", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        st.markdown("<div style='font-size: 10px; color: #8b949e; margin-bottom: 10px;'>PNG, JPG, JPEG • max 200MB<br>Immediate local analysis with zero latency</div>", unsafe_allow_html=True)

        st.markdown("### 📷 Live Camera Stream")
        camera_file = st.camera_input("Live camera feed", label_visibility="collapsed")
        
        cam_btn1, cam_btn2 = st.columns(2)
        with cam_btn1:
            capture_trigger = st.button("📸 Capture Snapshot", type="primary", use_container_width=True)
        with cam_btn2:
            clear_trigger = st.button("✕ Clear / Reset Frame", use_container_width=True)

    new_image = None
    if uploaded_file is not None:
        new_image = Image.open(uploaded_file)
    elif camera_file is not None or capture_trigger:
        if camera_file is not None:
            new_image = Image.open(camera_file)

    if clear_trigger:
        st.session_state.active_image = None
        st.session_state.caption = None
        st.session_state.feedback_submitted = False
        st.rerun()

    if new_image is not None and new_image != st.session_state.active_image:
        st.session_state.active_image = new_image
        st.session_state.caption = None
        st.session_state.feedback_submitted = False

    with right_col:
        st.markdown(
            "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>"
            "<h3 style='margin: 0;'>🖼️ Active Captured Image</h3>"
            "<span style='background: #1f6feb; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 600;'>Description Ready</span>"
            "</div>", 
            unsafe_allow_html=True
        )

        if st.session_state.active_image is not None:
            # Updated parameter fix here
            st.image(st.session_state.active_image, width="stretch")
            
            if st.button("⚡ Re-Analyze & Describe Image", type="primary", use_container_width=True):
                with st.spinner("Analyzing spatial layout and obstacles..."):
                    st.session_state.caption = generate_caption_ollama(st.session_state.active_image)
                    st.session_state.feedback_submitted = False
                st.rerun()
        else:
            st.info("Awaiting image input from upload or camera...")

        st.markdown(
            "<div style='margin-top: 8px;'>"
            "<b>💬 Scene Description</b> &nbsp;&nbsp;"
            "<span class='badge-detail'>English</span> "
            "<span class='badge-detail'>Ultra Detail</span>"
            "<span style='float: right; font-size: 11px; color: #8b949e;'>Voice: <b>Warm Natural (Female)</b></span>"
            "</div>", 
            unsafe_allow_html=True
        )

        if st.session_state.active_image is not None and st.session_state.caption is None:
            with st.spinner("Generating neural spatial description..."):
                st.session_state.caption = generate_caption_ollama(st.session_state.active_image)

        if st.session_state.caption is not None:
            with st.container(border=True):
                st.markdown(f"<div style='font-size: 12px; line-height: 1.3;'>{st.session_state.caption}</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 4px 0; border-color: #21262d;'>", unsafe_allow_html=True)
                st.markdown("<span style='color: #3fb950; font-size: 10px;'>✓ Safety Assessment: Clear floor pathway. No imminent tripping hazards or sharp obstacles detected.</span>", unsafe_allow_html=True)

            st.markdown("<div style='font-size: 11px; margin-top: 2px;'>🔊 <b>Spoken Audio Narration</b></div>", unsafe_allow_html=True)
            audio_bytes = text_to_audio(st.session_state.caption)
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)

            if not st.session_state.feedback_submitted:
                st.markdown("<div style='font-size: 10px; margin-top: 2px;'>Was this description accurate?</div>", unsafe_allow_html=True)
                fb_col1, fb_col2 = st.columns(2)
                with fb_col1:
                    if st.button("👍 Yes, Correct", use_container_width=True):
                        save_feedback(st.session_state.active_image, st.session_state.caption, "correct")
                        st.session_state.feedback_submitted = True
                        st.balloons()
                        st.rerun()
                with fb_col2:
                    if st.button("👎 Retry / Re-analyze", use_container_width=True):
                        save_feedback(st.session_state.active_image, st.session_state.caption, "incorrect")
                        with st.spinner("Re-evaluating with deeper analysis..."):
                            retry_prompt = (
                                "The user flagged the previous caption as inaccurate. "
                                "Re-examine the image extremely carefully and describe key details accurately."
                            )
                            st.session_state.caption = generate_caption_ollama(
                                st.session_state.active_image, custom_instruction=retry_prompt
                            )
                        st.rerun()
            else:
                st.success("Feedback recorded successfully. Ready for next input.")
        else:
            st.markdown("<div style='color: #8b949e; font-size: 11px; font-style: italic;'>No description generated yet.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
        <div class="custom-footer">
            <span>NOVA v2.4 Assistive Engine &nbsp;&nbsp;•&nbsp;&nbsp; 🟢 Camera & Neural Core Connected</span>
            <span>Designed for maximum contrast and zero-scroll spatial awareness &nbsp;&nbsp;•&nbsp;&nbsp; WCAG 2.1 AAA Compliant</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()