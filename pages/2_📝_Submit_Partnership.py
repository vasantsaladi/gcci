import streamlit as st
from datetime import datetime
from utils.layout import setup_page
from data.partnership_interests import PartnershipInterests

def main():
    setup_page("Submit Partnership - York College")
    
    st.title("Submit New Partnership Interest")
    st.markdown("Partner with York College to create opportunities and drive innovation")

    # Information panel
    st.info("""
    ### Who can submit:
    - YCP Faculty/Staff
    - YCP Students
    - Businesses
    - Other Colleges
    - Community Organizations
    """)

    # Basic Information
    st.subheader("Contact Information")
    col1, col2 = st.columns(2)
    
    with col1:
        organization = st.text_input("Organization Name*")
        contact_name = st.text_input("Contact Name*")
        email = st.text_input("Email*")
    
    with col2:
        org_type = st.selectbox(
            "Type*", 
            PartnershipInterests.ORGANIZATION_TYPES
        )
        phone = st.text_input("Phone Number")

    # Partnership Details
    st.markdown("---")
    st.subheader("Partnership Details")
    
    partnership_type = st.selectbox(
        "Type of Partnership*", 
        PartnershipInterests.PARTNERSHIP_TYPES
    )

    goals = st.text_area(
        "What are your goals for this partnership?*",
        help="Please describe your vision for this partnership and expected outcomes"
    )
    
    timeline = st.selectbox(
        "When would you like to start?", 
        PartnershipInterests.TIMELINES
    )

    # Additional Information
    with st.expander("Additional Information (Optional)"):
        resources = st.text_area("What resources can you contribute to this partnership?")
        expectations = st.text_area("What are your expectations from York College?")

    # Submit button with validation
    st.markdown("---")
    if st.button("Submit Partnership Interest", type="primary"):
        if not all([organization, contact_name, email, goals]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Display success message without saving
            st.success("""
            Thank you for your interest in partnering with York College! 
            
            This is currently a demonstration form. When the system is fully implemented, 
            your submission will be processed and stored securely.
            """)
            st.balloons()

    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
        ### Contact Us
        For assistance with your partnership submission:
        - 📧 Email: partnerships@ycp.edu
        - 📞 Phone: 717.846.7788
        - 📍 Location: Graham Center for Collaborative Innovation
        
        ### Processing Time
        We typically review submissions within 3-5 business days.
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <small>
            © 2024 York College of Pennsylvania<br>
            Graham Center for Collaborative Innovation<br>
            441 Country Club Rd, York, PA 17403-3651
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()