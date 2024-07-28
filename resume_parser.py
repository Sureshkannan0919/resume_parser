
import pdfminer
import re
from pdfminer.high_level import extract_text
import spacy
nlp = spacy.load('en_core_web_sm')
class reume_parser:
    def __init__(self, resume_path):
        self.text = extract_text(resume_path)

    def extract_name_from_resume(self):
      name = None
      pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
      match = re.search(pattern,self.text)
      if match:
        name = match.group()
      return name


    def extract_contact_number_from_resume(self):
      contact_number = None

    # Use regex pattern to find a potential contact number
      pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
      match = re.search(pattern, self.text)
      if match:
        contact_number = match.group()
      return contact_number


    def extract_email_from_resume(self):
      email = None

      # Use regex pattern to find a potential email address
      pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
      match = re.search(pattern, self.text)
      if match:
        email = match.group()
      return email



    def extract_skills_from_resume(self):
      skills_list =skill_keywords = [
        # Programming languages
        'Python', 'Java', 'C\\+\\+', 'JavaScript', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Go', 'Rust',
        # Web technologies
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Django', 'Flask',
        # Databases
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis', 'Cassandra',
        # Cloud platforms
        'AWS', 'Azure', 'Google Cloud', 'Heroku', 'Docker', 'Kubernetes',
        # Data science and ML
        'Machine Learning', 'Deep Learning', 'NLP', 'Data Analysis', 'Pandas', 'NumPy', 'SciPy', 'TensorFlow', 'PyTorch',
        # Version control
        'Git', 'SVN', 'Mercurial',
        # Project management
        'Agile', 'Scrum', 'Kanban', 'JIRA', 'Trello',
        # Design
        'Photoshop', 'Illustrator', 'Sketch', 'Figma', 'InDesign',
        # Office tools
        'Microsoft Office', 'Excel', 'PowerPoint', 'Word', 'Google Workspace',
        # Soft skills
        'Leadership', 'Communication', 'Teamwork', 'Problem Solving', 'Critical Thinking',
        # Additional technical skills
        'RESTful API', 'GraphQL', 'DevOps', 'CI/CD', 'Unit Testing', 'Selenium', 'Blockchain'
    ]
      skills = []

      # Search for skills in the resume text
      for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            skills.append(skill)

      return skills

    def extract_education_from_resume(self):
      education = []

      # Use regex pattern to find education information
      pattern = r"(?i)(?:(?:Bachelor|B\.Tech|B\.E|B\.S\.|B\.A\.|Master|M\.S\.|M\.A\.|Ph\.D\.)\s(?:[A-Za-z]+\s)*[A-Za-z]+)"
      matches = re.findall(pattern, self.text,re.IGNORECASE)
      for match in matches:
        education.append(match.strip())

      return education

    #Extracting specific skill
    def extract_data_science_education(self):
      doc = nlp(self.text)
      education = []
      for ent in doc.ents:
        if ent.label_ == 'ORG' and 'Data Science' in ent.self.text:
            education.append(ent.self.text)

      return education


    def extract_college_name(self):
      lines = self.text.split('\n')
      college_pattern =  r'\b(?:University|College|Institute|School|Academy)\s+(?:of|for|at)?\s+[\w\s&,]+\b|\b[\w\s&,]+(?:University|College|Institute|School|Academy)\b'
      for line in lines:
        if re.match(college_pattern, line,re.IGNORECASE):
          return line.strip()
      return None
def get_pdf_path():
    while True:
        file_path = input("Please enter the path to your PDF file: ").strip()

        # Check if the file path ends with .pdf
        if not file_path.lower().endswith('.pdf'):
            print("The file must have a .pdf extension. Please try again.")
            continue

        # Check if the file exists
        import os
        if not os.path.isfile(file_path):
            print("The specified file does not exist. Please check the path and try again.")
            continue

        # If we've made it here, the file exists and has a .pdf extension
        return file_path

if __name__ == '__main__':
    resume_path = get_pdf_path()
    resume_parser = reume_parser(resume_path)
    name=resume_parser.extract_name_from_resume()
    if name:
      print("Name:", name)
    else:
      print("Name not found")
    email=resume_parser.extract_email_from_resume()
    if email:
      print("Email:", email)
    else:
      print("Email not found")
    phone_number=resume_parser.extract_contact_number_from_resume()
    if phone_number:
      print("Phone Number:", phone_number)
    else:
      print("Phone Number not found")
    skill=resume_parser.extract_skills_from_resume()
    if skill:
      print("Skills:", skill)
    else:
      print("Skills not found")
    education=resume_parser.extract_education_from_resume()
    if education:
      print("Education:", education)
    else:
      print("Education not found")
    college_name=resume_parser.extract_college_name()
    if college_name:
      print("College Name:", college_name)
    else:
      print("College Name not found")

