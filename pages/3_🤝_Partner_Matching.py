import streamlit as st
from openai import OpenAI
from data.partnerships import PARTNERSHIPS
import json
from utils.layout import setup_page

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def prepare_partnerships_context():
    """Convert partnerships data into a searchable context"""
    context = []
    for category, partnerships in PARTNERSHIPS.items():
        for partner_id, partner in partnerships.items():
            summary = {
                "category": category,
                "name": partner["name"],
                "type": partner["type"],
                "focus_areas": partner.get("focus_areas", []),
                "programs": partner.get("programs", []),
                "benefits": partner.get("benefits", {}),
            }
            context.append(summary)
    return context

def get_matching_partners(user_input: dict, context: list) -> list:
    """Use OpenAI to find matching partners based on user input"""
    system_prompt = """
    You are a partnership matching expert for York College. Using the provided partnership data,
    suggest potential partnerships based on the user's interests and goals.
    Focus on finding complementary partnerships that could create mutual value.
    Explain why each match would be beneficial.
    """
    
    user_prompt = f"""
    User Interest:
    - Organization Type: {user_input['org_type']}
    - Interest Areas: {', '.join(user_input['interests'])}
    - Resources Available: {', '.join(user_input['resources'])}
    - Goals: {user_input['goals']}
    
    Current Partnerships Data:
    {json.dumps(context, indent=2)}
    
    Please suggest 2-3 potential partnerships and explain why they would be good matches.
    Format your response in JSON with the following structure:
    {{
        "matches": [
            {{
                "partner_name": "Name",
                "match_score": 0-100,
                "reasons": ["reason1", "reason2"],
                "potential_collaboration": "description"
            }}
        ]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def main():
    setup_page("Partner Matching - York College")
    
    st.title("🤝 Partner Matching")
    st.markdown("""
    Find potential partnerships based on your interests and goals. 
    Our AI will analyze existing partnerships to suggest the best matches for collaboration.
    """)

    # User Input Form with YCP styling
    with st.form("matching_form"):
        st.subheader("Tell Us About Your Organization")
        
        col1, col2 = st.columns(2)
        with col1:
            org_type = st.selectbox(
                "Organization Type*",
                ["Business/Industry", "Educational Institution", "Community Organization", 
                 "Government Agency", "Research Institution", "Non-Profit"]
            )
            
            interests = st.multiselect(
                "Areas of Interest*",
                ["Technology", "Education", "Healthcare", "Community Development",
                 "Research", "Innovation", "Workforce Development", "Arts & Culture",
                 "Environmental", "Economic Development"]
            )
        
        with col2:
            resources = st.multiselect(
                "Available Resources*",
                ["Funding", "Expertise", "Facilities", "Technology",
                 "Industry Connections", "Research Capabilities", "Student Opportunities",
                 "Community Access"]
            )
            
            goals = st.text_area(
                "Partnership Goals*",
                help="Describe what you hope to achieve through collaboration"
            )
        
        submitted = st.form_submit_button("Find Matching Partners", type="primary")

    # Process matching when form is submitted
    if submitted:
        if not all([org_type, interests, resources, goals]):
            st.error("Please fill in all required fields marked with *")
        else:
            with st.spinner("Analyzing potential partnerships..."):
                user_input = {
                    "org_type": org_type,
                    "interests": interests,
                    "resources": resources,
                    "goals": goals
                }
                context = prepare_partnerships_context()
                matches = get_matching_partners(user_input, context)
                
                # Display results with YCP styling
                st.markdown("---")
                st.subheader("Recommended Partnerships")
                
                for match in matches["matches"]:
                    with st.expander(f"🤝 {match['partner_name']}", expanded=True):
                        st.markdown(f"**Match Score:** {match['match_score']}%")
                        
                        st.markdown("### Why this is a good match:")
                        for reason in match["reasons"]:
                            st.markdown(f"- {reason}")
                        
                        st.markdown("### Potential Collaboration:")
                        st.info(match["potential_collaboration"])
                        
                        # Partner details
                        for category in PARTNERSHIPS.values():
                            for partner in category.values():
                                if partner["name"] == match["partner_name"]:
                                    st.markdown("### Current Partnership Details:")
                                    if "focus_areas" in partner:
                                        st.markdown("**Focus Areas:**")
                                        for area in partner["focus_areas"]:
                                            st.markdown(f"- {area}")
                                    if "programs" in partner:
                                        st.markdown("**Current Programs:**")
                                        for program in partner["programs"]:
                                            st.markdown(f"- {program}")

    # Help section with YCP styling
    st.markdown("---")
    with st.expander("Need Help?"):
        st.markdown("""
        ### Tips for Better Matches:
        1. Be specific about your interests and goals
        2. Consider multiple areas of collaboration
        3. Think about unique resources you can offer
        4. Focus on mutual benefits
        5. Consider both short and long-term opportunities
        
        For additional assistance, contact:
        - 📧 partnerships@ycp.edu
        - 📞 717.846.7788
        - 📍 Graham Center for Collaborative Innovation
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