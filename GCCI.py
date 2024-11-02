import streamlit as st
from utils.layout import setup_page
from data.partnerships import PARTNERSHIPS
from pathlib import Path

def get_metrics():
    return {
        "economic_impact": sum([p.get("economic_impact", 0) for cat in PARTNERSHIPS.values() for p in cat.values()]),
        "total_partners": len([p for cat in PARTNERSHIPS.values() for p in cat.values()]),
        "active_projects": len([p for cat in PARTNERSHIPS.values() for p in cat.values() if p["status"] == "Active"])
    }

def main():
    setup_page("GCCI Partnership Hub")
    
    st.title("Graham Center for Collaborative Innovation")
    st.subheader("Where Innovation Meets Community Impact")

    # Key Innovation Hubs section
    st.markdown("""
    ### Key Innovation Hubs

    🏢 **Knowledge Park**
    - $64 million economic value to York area
    - State-of-the-art facilities for business partners
    - Student internships and research opportunities
    - Industry-academic collaboration space

    🤝 **Urban Collaborative**
    - Project-based community research
    - Safe and affordable housing initiatives
    - Faculty-student engagement
    - Community partnership development
    """)

    # Updated Metrics with YCP styling
    st.markdown("---")
    metrics = get_metrics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Economic Impact", f"${metrics['economic_impact']}M+")
    with col2:
        st.metric("Community Partners", metrics['total_partners'])
    with col3:
        st.metric("Student Projects", metrics['active_projects'])
    with col4:
        st.metric("Business Partners", "40+")

    # Partnership Initiatives
    st.markdown("---")
    st.subheader("Partnership Initiatives")

    tab1, tab2, tab3 = st.tabs(["Academic Partnerships", "Business Collaborations", "Community Engagement"])

    with tab1:
        st.markdown("""
        - **Commonwealth of PA Partnership**
            - 15% tuition discount for state employees
            - 20+ online graduate programs
            - Professional certificates
        
        - **International Education**
            - Lighthouse Learning India collaboration
            - Student exchange programs
            - Global learning initiatives
        """)

    with tab2:
        st.markdown("""
        - **Knowledge Park Opportunities**
            - Office space for industry partners
            - Collaborative shared spaces
            - Faculty consulting
            - Student internships
        
        - **Corporate Partnerships**
            - HP Inc. Global Entrepreneurship Program
            - Dataforma Software Training
            - UPMC Exercise Science Lab
        """)

    with tab3:
        st.markdown("""
        - **Urban Collaborative**
            - Community-based research
            - Neighborhood development
            - Student engagement projects
            - Faculty-led initiatives
        
        - **Center for Community Engagement**
            - Spartan Volunteer Network
            - Arts Fellowship Programs
            - Public Policy Institute
        """)

    # Contact Information
    st.markdown("---")
    st.subheader("Connect With Us")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Knowledge Park Inquiries:**  
        📍 441 Country Club Rd  
        York, PA 17403-3651  
        📞 717.846.7788
        """)

    with col2:
        st.markdown("""
        **Urban Collaborative:**  
        Contact: Dominic DelliCarpini  
        Dean, Center for Community Engagement  
        ✉️ dcarpini@ycp.edu
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <small>
            © 2024 York College of Pennsylvania  
            Graham Center for Collaborative Innovation  
            441 Country Club Rd, York, PA 17403-3651  
            717.846.7788
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()