from datetime import datetime

class PartnershipInterests:
    # Constants for form options
    ORGANIZATION_TYPES = [
        "YCP Faculty/Staff",
        "YCP Student",
        "Business/Industry",
        "Educational Institution",
        "Community Organization",
        "Government Agency"
    ]

    PARTNERSHIP_TYPES = [
        "Academic Program",
        "Research Collaboration",
        "Student Opportunities",
        "Community Impact",
        "Resource Sharing",
        "Technology/Innovation"
    ]

    PARTNERSHIP_GOALS = [
        "Cross-disciplinary Research",
        "Student Learning Opportunities",
        "Resource Sharing",
        "Community Impact",
        "Innovation Development",
        "Professional Development",
        "Workforce Development",
        "Cultural Exchange"
    ]

    AVAILABLE_RESOURCES = [
        "Expertise/Knowledge",
        "Facilities/Space",
        "Funding/Grants",
        "Technology/Equipment",
        "Student Opportunities",
        "Data/Research",
        "Community Connections",
        "Industry Networks"
    ]

    TIMELINES = [
        "Immediate",
        "Next 3-6 months",
        "6-12 months",
        "Long-term planning"
    ]

    @staticmethod
    def validate_submission(data):
        """Validate submission data against schema"""
        required_fields = {
            "organization.name": "Organization Name",
            "organization.type": "Organization Type",
            "organization.location": "Location",
            "contact.name": "Contact Name",
            "contact.email": "Contact Email",
            "partnership.type": "Partnership Type",
            "partnership.goals": "Partnership Goals",
            "partnership.description": "Description"
        }

        for field, display_name in required_fields.items():
            parts = field.split('.')
            value = data
            for part in parts:
                value = value.get(part, {})
            if not value:
                return False, f"Missing required field: {display_name}"

        return True, None

    @staticmethod
    def format_submission(data):
        """Format submission data for storage"""
        return {
            "id": data["id"],
            "submission_date": data["submission_date"],
            "status": "New",
            "organization": {
                "name": data["organization"]["name"],
                "type": data["organization"]["type"],
                "website": data["organization"].get("website", ""),
                "location": data["organization"]["location"],
                "department": data["organization"].get("department", "")
            },
            "contact": {
                "name": data["contact"]["name"],
                "title": data["contact"]["title"],
                "email": data["contact"]["email"],
                "phone": data["contact"].get("phone", "")
            },
            "partnership": {
                "type": data["partnership"]["type"],
                "goals": data["partnership"]["goals"],
                "resources": data["partnership"].get("resources", []),
                "description": data["partnership"]["description"],
                "timeline": data["partnership"].get("timeline", ""),
                "funding": data["partnership"].get("funding", "To be discussed"),
                "additional_info": data["partnership"].get("additional_info", "")
            }
        }
