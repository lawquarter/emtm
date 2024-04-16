import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO

def generate_pdf(urgent_important, urgent_not_important, not_urgent_important, not_urgent_not_important):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    task_style = styles['Normal']

    # Draw quadrant borders
    p.line(300, 100, 300, 700)
    p.line(0, 400, 600, 400)

    # Add quadrant labels
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 650, "Urgent & Important")
    p.drawString(350, 650, "Not Urgent & Important")
    p.drawString(100, 350, "Urgent & Not Important")
    p.drawString(350, 350, "Not Urgent & Not Important")

    # Add tasks to each quadrant
    y = 600
    for task in urgent_important:
        task_para = Paragraph(f"- {task}", task_style)
        task_para.wrapOn(p, 250, 20)
        task_para.drawOn(p, 50, y)
        y -= 20

    y = 600
    for task in not_urgent_important:
        task_para = Paragraph(f"- {task}", task_style)
        task_para.wrapOn(p, 250, 20)
        task_para.drawOn(p, 350, y)
        y -= 20

    y = 300
    for task in urgent_not_important:
        task_para = Paragraph(f"- {task}", task_style)
        task_para.wrapOn(p, 250, 20)
        task_para.drawOn(p, 50, y)
        y -= 20

    y = 300
    for task in not_urgent_not_important:
        task_para = Paragraph(f"- {task}", task_style)
        task_para.wrapOn(p, 250, 20)
        task_para.drawOn(p, 350, y)
        y -= 20

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def main():
    st.title("Eisenhower Matrix Task Manager")
    st.write("The Eisenhower Matrix is a productivity tool that helps you prioritize tasks based on their urgency and importance. This app allows you to enter tasks, categorize them into quadrants, and download a PDF of your Eisenhower Matrix.")

    tasks = st.text_area("Enter tasks (one per line)", help="Enter each task on a separate line. Press Enter to add multiple tasks.")
    task_list = tasks.split("\n")

    # Create quadrants using columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Urgent")
        urgent_important = st.multiselect("Important", task_list, key="urgent_important", help="Tasks that are urgent and important. Focus on completing these tasks first.")
        urgent_not_important = st.multiselect("Not Important", [task for task in task_list if task not in urgent_important], key="urgent_not_important", help="Tasks that are urgent but not important. Delegate these tasks if possible.")
    with col2:
        st.subheader("Not Urgent")
        not_urgent_important = st.multiselect("Important", [task for task in task_list if task not in urgent_important and task not in urgent_not_important], key="not_urgent_important", help="Tasks that are important but not urgent. Schedule time to work on these tasks.")
        not_urgent_not_important = st.multiselect("Not Important", [task for task in task_list if task not in urgent_important and task not in urgent_not_important and task not in not_urgent_important], key="not_urgent_not_important", help="Tasks that are neither urgent nor important. Consider eliminating these tasks.")

    if st.button("Generate PDF"):
        pdf = generate_pdf(urgent_important, urgent_not_important, not_urgent_important, not_urgent_not_important)
        st.download_button(
            label="Download PDF",
            data=pdf,
            file_name="eisenhower_matrix.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
