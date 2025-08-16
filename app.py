import streamlit as st
from travel_agent import run_multi_agent
from io import BytesIO
from agents.email_agent import send_email_with_attachment  
import re
from reportlab.platypus import ListFlowable, ListItem, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, black, darkblue
from reportlab.platypus import SimpleDocTemplate

def clean_text(text):
    """Remove markdown symbols and excessive whitespace from agent output."""
    if not text:
        return ""
    # Remove *, #, `, >, _ used in markdown for styling
    text = re.sub(r'[*#`>_]+', '', text)
    # Replace multiple newlines with double newline (paragraph break)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Trim whitespace on each line
    lines = [line.strip() for line in text.splitlines()]
    # Remove empty lines
    lines = [line for line in lines if line]
    return "\n".join(lines)

def generate_pdf(summary, agent_outputs):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('TitleStyle', parent=styles['Title'], alignment=TA_CENTER,
                              fontSize=28, leading=34, spaceAfter=30,
                              textColor=darkblue, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=18,
                              leading=22, spaceBefore=24, spaceAfter=14,
                              textColor=HexColor("#004080"),
                              fontName='Helvetica-Bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle('BodyTextStyle', parent=styles['Normal'], fontSize=12,
                              leading=18, spaceAfter=8, textColor=black,
                              alignment=TA_LEFT))

    elements = []
    
    # Title
    elements.append(Paragraph("🌍 TripTacticx – Your Travel Plan", styles['TitleStyle']))
    
    # Intro / Summary (cleaned)
    intro_lines = clean_text(summary).split("\n")
    for line in intro_lines:
        if line.strip():
            elements.append(Paragraph(line.strip(), styles['BodyTextStyle']))
    elements.append(Spacer(1, 16))

    # Section headings map
    section_titles = {
        "Booking Suggestions": "🛫 Booking Suggestions",
        "Stay Options": "🏨 Stay Options",
        "Experiences": "🎨 Experiences",
        "Local Food & Dining": "🍽️ Local Food & Dining",
        "Travel Logistics": "🚗 Travel Logistics",
        "Budget Planning": "💰 Budget Planning"
    }

    def parse_content_to_flowables(text):
        """Convert multi-line agent output into PDF-friendly flowables (lists or paragraphs)."""
        flowables = []
        cleaned_text = clean_text(text)
        # Split into blocks separated by blank lines
        blocks = [b.strip() for b in cleaned_text.split('\n\n') if b.strip()]
        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            # Detect bullet points by dash or star at start
            if all(line.startswith(('- ', '* ')) for line in lines):
                items = [line[2:].strip() for line in lines]
                list_flowable = ListFlowable(
                    [ListItem(Paragraph(item, styles['BodyTextStyle']), bulletColor=darkblue) for item in items],
                    bulletType='bullet',
                    leftIndent=20,
                    bulletFontName='Helvetica',
                    bulletFontSize=8,
                    bulletColor=darkblue,
                    start='circle',
                    spaceBefore=4,
                    spaceAfter=8,
                )
                flowables.append(list_flowable)
            else:
                # Keep line breaks within paragraphs
                paragraph_text = "<br/>".join(lines)
                flowables.append(Paragraph(paragraph_text, styles['BodyTextStyle']))
            flowables.append(Spacer(1, 6))
        return flowables

    # Add each agent's section
    for key, content in agent_outputs.items():
        section_title = section_titles.get(key, key)
        elements.append(Paragraph(section_title, styles['SectionHeader']))
        if content:
            elements.extend(parse_content_to_flowables(content))
        else:
            elements.append(Paragraph("No details available.", styles['BodyTextStyle']))
            elements.append(Spacer(1, 8))

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# Streamlit styling and UI (unchanged, just keep what you had)

st.set_page_config("TripTacticx", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Your CSS here */
</style>
""", unsafe_allow_html=True)

st.title("🧳 TripTacticx – Multi-Agent Travel Planner")

with st.form("travel_form"):
    name = st.text_input("📝 Your Name", placeholder="e.g., Luqmaan")
    email = st.text_input("📧 Your Email Address", placeholder="e.g., yourname@example.com")
    destination = st.text_input("🌐 Destination", placeholder="e.g., Paris, Tokyo, Kerala")
    days = st.number_input("🗓️ Trip Duration (days)", min_value=1, max_value=365, value=5)
    group_size = st.number_input("👥 Group Size", min_value=1, max_value=100, value=2)
    trip_type = st.selectbox("🎯 Trip Type", ["Leisure", "Adventure", "Honeymoon", "Solo", "Business"])
    budget = st.text_input("💰 Budget per person", placeholder="e.g., $1000, ₹50000")
    preferences = st.text_area("💡 Special Interests / Preferences", placeholder="e.g., Cultural experiences, local food, hiking")
    source_location = st.text_input("🚉 Your Current Location", placeholder="e.g., Bangalore, New York")
    submit = st.form_submit_button("Plan My Trip")

if submit:
    if not name.strip():
        st.error("⚠ Please enter your name.")
    elif not email or "@" not in email or "." not in email:
        st.error("⚠ Please enter a valid email address.")
    elif not destination or not budget or not source_location:
        st.error("⚠ Please fill in all required fields (Destination, Budget, Source Location).")
    else:
        try:
            budget_value = float(''.join([c for c in budget if c.isdigit() or c == '.']))
        except:
            st.error("⚠ Please enter a valid budget (e.g., $1000 or 50000).")
            st.stop()

        with st.spinner("🧠 Agents are coordinating your perfect getaway..."):
            summary, agent_outputs = run_multi_agent(
                destination=destination,
                days=int(days),
                group_size=int(group_size),
                budget=budget_value,
                trip_type=trip_type,
                preferences=preferences,
                source_location=source_location
            )

        st.success("🎉 Here's your personalized travel plan!")

        for section_title, content in agent_outputs.items():
            with st.expander(section_title):
                st.markdown(f"<div class='section-card'>{content}</div>", unsafe_allow_html=True)

        pdf_data = generate_pdf(summary, agent_outputs)

        success = send_email_with_attachment(name, email, pdf_data, "Your TripTacticx Itinerary.pdf")

        if success:
            st.success(f"✉️ Thanks {name}! Your travel plan was sent to {email}.")
        else:
            st.error("⚠ Sorry, we couldn't send the email. Please try again later.")

        st.download_button(
            label="📄 Download Travel Plan as PDF",
            data=pdf_data,
            file_name="triptacticx_plan.pdf",
            mime="application/pdf"
        )
