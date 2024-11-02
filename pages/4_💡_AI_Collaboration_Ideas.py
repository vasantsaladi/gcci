import streamlit as st
from openai import OpenAI
from data.partnerships import PARTNERSHIPS
import json
from utils.layout import setup_page

# Initialize OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_partnership_categories():
    """Get unique partnership categories and types from existing data"""
    categories = set()
    types = set()
    for category, partnerships in PARTNERSHIPS.items():
        categories.add(category)
        for partnership in partnerships.values():
            types.add(partnership.get('type', ''))
    return sorted(categories), sorted(types)

def prepare_context_for_ai():
    """Prepare existing partnerships data as context for AI"""
    context = []
    for category, partnerships in PARTNERSHIPS.items():
        for partner_id, partner in partnerships.items():
            summary = {
                "category": category,
                "name": partner["name"],
                "type": partner["type"],
                "focus_areas": partner.get("focus_areas", []),
                "programs": partner.get("programs", []),
                "benefits": partner.get("benefits", {})
            }
            context.append(summary)
    return context

def main():
    setup_page("AI Innovation Ideas - York College")
    
    st.title("💡 AI Partnership Innovation Ideas")
    st.markdown("""
    ### Discover Creative Collaboration Opportunities
    Our AI will analyze existing successful partnerships and generate innovative ideas 
    for collaboration based on your interests and goals.
    """)

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        # Get categories and types
        categories, partnership_types = get_partnership_categories()

        # Category Selection
        selected_category = st.selectbox(
            "Select Partnership Category*",
            ["All"] + list(categories),
            help="Filter by partnership category to get more relevant suggestions"
        )

    with col2:
        # Interest Areas
        interests = st.multiselect(
            "Select Areas of Interest*",
            [
                "Student Learning", "Research", "Innovation", 
                "Community Impact", "Resource Sharing", "Economic Development",
                "Healthcare", "Technology", "Education", "Sustainability"
            ],
            help="Choose areas that align with your collaboration goals"
        )

    # Additional context (optional)
    with st.expander("Additional Context (Optional)"):
        specific_goals = st.text_area(
            "Specific Goals or Requirements",
            help="Add any specific goals or requirements for the collaboration"
        )
        resources = st.text_area(
            "Available Resources",
            help="Describe any resources you can bring to the partnership"
        )

    if st.button("Generate Collaboration Ideas", type="primary"):
        if not interests:
            st.error("Please select at least one area of interest")
        else:
            with st.spinner("Generating innovative collaboration ideas..."):
                partnership_context = prepare_context_for_ai()
                
                prompt = f"""
                Based on the following context of existing York College partnerships:
                {json.dumps(partnership_context, indent=2)}

                Generate innovative collaboration ideas for new partnerships in the following areas:
                Category: {selected_category if selected_category != "All" else "Any category"}
                Interest Areas: {", ".join(interests)}
                {"Additional Goals: " + specific_goals if specific_goals else ""}
                {"Available Resources: " + resources if resources else ""}

                Please provide:
                1. 3-4 specific collaboration ideas
                2. For each idea:
                   - Detailed description
                   - Potential benefits for all parties
                   - Required resources
                   - Expected outcomes
                   - Similar successful examples from existing partnerships
                3. Implementation suggestions

                Format the response in markdown with clear sections and bullet points.
                Focus on practical, innovative ideas that create mutual value and benefit the York community.
                """

                try:
                    response = client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=[
                            {"role": "system", "content": "You are an expert in academic-industry-community partnerships with deep knowledge of York College's existing partnerships."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )

                    # Display generated ideas in a clean format
                    st.markdown("---")
                    st.markdown("## 🌟 Generated Collaboration Ideas")
                    st.markdown(response.choices[0].message.content)

                    # Action buttons in columns
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save Ideas", key="save"):
                            st.session_state['saved_ideas'] = response.choices[0].message.content
                            st.success("Ideas saved successfully!")
                    with col2:
                        if st.button("📋 Download as PDF", key="pdf"):
                            st.info("PDF download feature coming soon!")

                except Exception as e:
                    st.error(f"Error generating ideas: {str(e)}")

    # Display saved ideas if they exist
    if 'saved_ideas' in st.session_state:
        with st.expander("Previously Generated Ideas"):
            st.markdown(st.session_state['saved_ideas'])

    # Help section with YCP styling
    st.markdown("---")
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        ### How to Get the Most Useful Ideas:
        1. **Select Relevant Categories**: Choose categories that align with your organization's focus
        2. **Be Specific**: Select multiple interest areas to get more targeted suggestions
        3. **Consider Resources**: Think about what resources you can bring to a partnership
        4. **Look for Synergies**: Consider how your goals align with existing successful partnerships
        5. **Think Long-term**: Consider both immediate and long-term collaboration opportunities
        
        ### Need Assistance?
        - 📧 Email: partnerships@ycp.edu
        - 📞 Phone: 717.846.7788
        - 📍 Location: Graham Center for Collaborative Innovation
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