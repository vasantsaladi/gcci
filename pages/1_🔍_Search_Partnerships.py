import streamlit as st
from utils.layout import setup_page
from data.partnerships import PARTNERSHIPS
import pandas as pd

def get_all_partnerships():
    """Get all partnerships with their category"""
    all_partnerships = []
    for category, partnerships in PARTNERSHIPS.items():
        for key, partnership in partnerships.items():
            partnership['category'] = category  # Add category to partnership data
            all_partnerships.append(partnership)
    return all_partnerships

def filter_partnerships(partnerships, filters):
    """Filter partnerships based on selected criteria"""
    filtered = partnerships
    
    if filters.get('type'):
        filtered = [p for p in filtered if p['type'] in filters['type']]
    
    if filters.get('status'):
        filtered = [p for p in filtered if p['status'] in filters['status']]
    
    if filters.get('category'):
        filtered = [p for p in filtered if p['category'] in filters['category']]
    
    if filters.get('search'):
        search = filters['search'].lower()
        filtered = [p for p in filtered if 
                   search in p['name'].lower() or
                   search in p.get('description', '').lower() or
                   any(search in str(v).lower() for v in p.values() if isinstance(v, (str, list)))]
    
    return filtered

def main():
    setup_page("Search Partnerships - York College")
    
    st.title("🔍 Search YCP Partnerships")
    st.markdown("Find and explore York College's partnerships across various sectors")

    # Search bar with YCP styling
    search_query = st.text_input(
        "Search partnerships by keyword", 
        help="Search across partnership names, descriptions, and details"
    )

    # Main filters
    col1, col2 = st.columns(2)
    with col1:
        selected_categories = st.multiselect(
            "Partnership Category",
            list(PARTNERSHIPS.keys()),
            help="Filter by partnership category"
        )
    
    with col2:
        selected_status = st.multiselect(
            "Status",
            ["Active", "In Development", "Completed"],
            help="Filter by current status"
        )

    # Advanced filters
    with st.expander("Advanced Filters"):
        col3, col4 = st.columns(2)
        with col3:
            selected_types = st.multiselect(
                "Partnership Type",
                set(p['type'] for p in get_all_partnerships()),
                help="Filter by specific partnership type"
            )
        
        with col4:
            has_funding = st.checkbox(
                "Has Funding/Benefits", 
                help="Show only partnerships with funding or benefits"
            )

    # Apply filters
    filters = {
        'search': search_query,
        'category': selected_categories,
        'status': selected_status,
        'type': selected_types
    }

    partnerships = get_all_partnerships()
    filtered_partnerships = filter_partnerships(partnerships, filters)

    # Results section
    st.markdown("---")
    st.subheader(f"Found {len(filtered_partnerships)} Partnerships")

    # Display results with YCP styling
    for p in filtered_partnerships:
        with st.expander(f"📋 {p['name']}", expanded=False):
            col1, col2 = st.columns([2,1])
            
            with col1:
                st.markdown(f"**Type:** {p['type']}")
                st.markdown(f"**Category:** {p['category'].title()}")
                st.markdown(f"**Status:** {p['status']}")
                
                if 'focus_areas' in p:
                    st.markdown("**Focus Areas:**")
                    for area in p['focus_areas']:
                        st.markdown(f"- {area}")
                
                if 'programs' in p:
                    st.markdown("**Programs:**")
                    for program in p['programs']:
                        st.markdown(f"- {program}")
                
                if 'benefits' in p:
                    st.markdown("**Benefits:**")
                    if isinstance(p['benefits'], dict):
                        for k, v in p['benefits'].items():
                            st.markdown(f"- **{k.title()}:** {v}")
                    elif isinstance(p['benefits'], list):
                        for benefit in p['benefits']:
                            st.markdown(f"- {benefit}")
            
            with col2:
                if 'contacts' in p:
                    st.markdown("**Contacts:**")
                    for role, contact in p['contacts'].items():
                        st.markdown(f"**{role.title()}:**")
                        st.markdown(f"- {contact['name']}")
                        if 'title' in contact:
                            st.markdown(f"- {contact['title']}")
                        if 'email' in contact:
                            st.markdown(f"- ✉️ {contact['email']}")
                        if 'phone' in contact:
                            st.markdown(f"- 📞 {contact['phone']}")
                
                if 'start_date' in p:
                    st.markdown(f"**Start Date:** {p['start_date']}")
                
                if 'duration' in p:
                    st.markdown(f"**Duration:** {p['duration']}")

    # Export functionality with YCP styling
    st.markdown("---")
    if st.button("Export Results", key="export"):
        df = pd.DataFrame(filtered_partnerships)
        st.download_button(
            "Download as CSV",
            df.to_csv(index=False),
            "ycp_partnerships.csv",
            "text/csv",
            key="download"
        )

    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
        ### How to use the search:
        1. Use the search bar to find partnerships by keyword
        2. Filter by category, status, or type
        3. Use advanced filters for more specific results
        4. Click on any partnership to see full details
        5. Export results for offline use
        
        For additional help, contact the GCCI office at partnerships@ycp.edu
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