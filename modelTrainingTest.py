import spacy

nlp_ner = spacy.load("/spaCyTesting/model-best")

doc = nlp_ner("""
Qualifications
•
Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
•
GPA of 3.0 or greater
Responsibilities
•
Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
•
Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
•
Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
•
Develop software test procedures, software programs, and related documentation
•
Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
•
Participate in peer reviews, identify, track and repair defects
•
Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)
Job description
Description:

Job Description
• Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
• Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
• Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
• Develop software test procedures, software programs, and related documentation
• Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
• Participate in peer reviews, identify, track and repair defects
• Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)

Qualifications:
• Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
• GPA of 3.0 or greater

Preferred Skills:
• One or more of the following: C++, C#, C, Java, Ruby, JEE, HTML5, XML, SQL, Qt, Windows, .NET, Unix, Linux, SOA, RTOS, Real-Time Controls, Wireless, Software Security, Robotics, OOA/OOD, Hadoop, Android, Embedded Systems""")

colors = {"SKILL": "#F67DE3"}
options = {"colors": colors} 

spacy.displacy.render(doc, style="ent", options= options)