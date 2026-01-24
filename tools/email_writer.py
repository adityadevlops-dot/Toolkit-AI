"""
Email Writer Tool - Generate professional emails.
"""

from .base_tool import BaseTool


class EmailWriterTool(BaseTool):
    """Generate professional emails for various purposes."""
    
    def __init__(self):
        super().__init__()
        self.name = "email_writer"
        self.description = "Generate professional emails for various purposes including business, follow-up, thank you, apology, request, and more."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "email_type": {
                    "type": "string",
                    "enum": ["business", "follow_up", "thank_you", "apology", "request", "introduction", "meeting", "complaint", "resignation", "cover_letter", "cold_outreach", "reminder", "congratulations", "rejection", "acceptance"],
                    "description": "Type of email to generate",
                    "default": "business"
                },
                "recipient_name": {
                    "type": "string",
                    "description": "Name of the recipient"
                },
                "sender_name": {
                    "type": "string",
                    "description": "Name of the sender"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject or topic"
                },
                "key_points": {
                    "type": "string",
                    "description": "Key points to include (comma-separated)"
                },
                "tone": {
                    "type": "string",
                    "enum": ["formal", "professional", "friendly", "casual"],
                    "description": "Tone of the email",
                    "default": "professional"
                },
                "company": {
                    "type": "string",
                    "description": "Company name if applicable"
                }
            },
            "required": ["email_type"]
        }
        
        self._greetings = {
            "formal": ["Dear", "Respected"],
            "professional": ["Dear", "Hello"],
            "friendly": ["Hi", "Hello"],
            "casual": ["Hi", "Hey"]
        }
        
        self._closings = {
            "formal": ["Sincerely", "Respectfully", "Yours faithfully"],
            "professional": ["Best regards", "Kind regards", "Regards"],
            "friendly": ["Best", "Warm regards", "Thanks"],
            "casual": ["Cheers", "Thanks", "Best"]
        }
    
    def execute(self, email_type="business", recipient_name=None, sender_name=None, subject=None, key_points=None, tone="professional", company=None):
        try:
            recipient = recipient_name if recipient_name else "[Recipient Name]"
            sender = sender_name if sender_name else "[Your Name]"
            topic = subject if subject else "[Subject]"
            comp = company if company else "[Company]"
            
            points = []
            if key_points:
                points = [p.strip() for p in key_points.split(",")]
            
            if email_type == "business":
                return self._business_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "follow_up":
                return self._follow_up_email(recipient, sender, topic, points, tone)
            elif email_type == "thank_you":
                return self._thank_you_email(recipient, sender, topic, points, tone)
            elif email_type == "apology":
                return self._apology_email(recipient, sender, topic, points, tone)
            elif email_type == "request":
                return self._request_email(recipient, sender, topic, points, tone)
            elif email_type == "introduction":
                return self._introduction_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "meeting":
                return self._meeting_email(recipient, sender, topic, points, tone)
            elif email_type == "complaint":
                return self._complaint_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "resignation":
                return self._resignation_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "cover_letter":
                return self._cover_letter_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "cold_outreach":
                return self._cold_outreach_email(recipient, sender, topic, points, tone, comp)
            elif email_type == "reminder":
                return self._reminder_email(recipient, sender, topic, points, tone)
            elif email_type == "congratulations":
                return self._congratulations_email(recipient, sender, topic, points, tone)
            elif email_type == "rejection":
                return self._rejection_email(recipient, sender, topic, points, tone)
            elif email_type == "acceptance":
                return self._acceptance_email(recipient, sender, topic, points, tone, comp)
            else:
                return self._business_email(recipient, sender, topic, points, tone, comp)
                
        except Exception as e:
            return "Email generation error: " + str(e)
    
    def _get_greeting(self, tone, name):
        greetings = self._greetings.get(tone, self._greetings["professional"])
        return greetings[0] + " " + name + ","
    
    def _get_closing(self, tone):
        closings = self._closings.get(tone, self._closings["professional"])
        return closings[0] + ","
    
    def _format_email(self, subject, body, sender, tone):
        result = "EMAIL TEMPLATE\n"
        result += "=" * 50 + "\n\n"
        
        result += "Subject: " + subject + "\n"
        result += "-" * 50 + "\n\n"
        result += body + "\n\n"
        result += self._get_closing(tone) + "\n"
        result += sender + "\n"
        
        result += "\n" + "=" * 50 + "\n"
        result += "Tone: " + tone.capitalize() + "\n"
        
        return result
    
    def _business_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope this email finds you well. I am writing to discuss " + subject + ".\n\n"
        
        if points:
            body += "I would like to address the following points:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I believe this matter is of significant importance and would appreciate the opportunity to discuss it further at your earliest convenience.\n\n"
        body += "Please let me know if you have any questions or require additional information. I am available to discuss this at a time that works best for you."
        
        return self._format_email(subject, body, sender, tone)
    
    def _follow_up_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope you are doing well. I wanted to follow up on our previous conversation regarding " + subject + ".\n\n"
        
        if points:
            body += "As discussed, here are the key points:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I understand you have a busy schedule, but I would greatly appreciate an update when you have a moment.\n\n"
        body += "Please don't hesitate to reach out if you need any clarification or additional information from my end."
        
        subj = "Follow Up: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _thank_you_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I wanted to take a moment to express my sincere gratitude for " + subject + ".\n\n"
        
        if points:
            body += "I particularly appreciated:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "Your support and assistance have been invaluable, and I truly appreciate the time and effort you dedicated to this.\n\n"
        body += "Thank you once again. I look forward to the opportunity to work together in the future."
        
        subj = "Thank You - " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _apology_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I am writing to sincerely apologize for " + subject + ".\n\n"
        body += "I understand that this situation may have caused inconvenience, and I take full responsibility for what occurred.\n\n"
        
        if points:
            body += "To address this situation, I am taking the following steps:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I value our relationship and am committed to ensuring this does not happen again. Please let me know if there is anything else I can do to make this right.\n\n"
        body += "Thank you for your understanding and patience."
        
        subj = "Apology: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _request_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope this email finds you well. I am writing to request " + subject + ".\n\n"
        
        if points:
            body += "Specifically, I am looking for assistance with:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I understand you may have a busy schedule, and I would be grateful for any time you can spare.\n\n"
        body += "Please let me know if you need any additional information from my end. I am flexible and happy to accommodate your availability."
        
        subj = "Request: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _introduction_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope this email finds you well. My name is " + sender + ", and I am reaching out to introduce myself"
        if company != "[Company]":
            body += " as a representative of " + company
        body += ".\n\n"
        
        body += "I am contacting you regarding " + subject + ".\n\n"
        
        if points:
            body += "A bit about my background:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I would love the opportunity to connect and explore how we might work together. Would you be available for a brief call or meeting in the coming weeks?\n\n"
        body += "Thank you for your time, and I look forward to hearing from you."
        
        subj = "Introduction: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _meeting_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope you are doing well. I would like to schedule a meeting to discuss " + subject + ".\n\n"
        
        if points:
            body += "The agenda for the meeting would include:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "Please let me know your availability for the following times:\n\n"
        body += "- [Option 1: Date and Time]\n"
        body += "- [Option 2: Date and Time]\n"
        body += "- [Option 3: Date and Time]\n\n"
        body += "If none of these work for you, please suggest alternative times that would be more convenient.\n\n"
        body += "I look forward to our discussion."
        
        subj = "Meeting Request: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _complaint_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting("formal", recipient)
        
        body = greeting + "\n\n"
        body += "I am writing to formally express my dissatisfaction regarding " + subject + ".\n\n"
        
        if points:
            body += "The specific issues I encountered are as follows:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "This situation has caused significant inconvenience, and I believe it falls short of the standards I expected from " + company + ".\n\n"
        body += "I would appreciate a prompt resolution to this matter. Please contact me at your earliest convenience to discuss how this can be addressed.\n\n"
        body += "I trust that you will take this complaint seriously and look forward to your response."
        
        subj = "Formal Complaint: " + subject
        return self._format_email(subj, body, sender, "formal")
    
    def _resignation_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting("formal", recipient)
        
        body = greeting + "\n\n"
        body += "I am writing to formally notify you of my resignation from my position at " + company + ", effective [Last Working Day].\n\n"
        
        body += "After careful consideration, I have decided to pursue " + subject + ".\n\n"
        
        if points:
            body += "I want to express my gratitude for:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I am committed to ensuring a smooth transition and am willing to assist in training my replacement during my notice period.\n\n"
        body += "Thank you for the opportunities for professional growth that you have provided me during my time at " + company + ". I wish the company continued success."
        
        subj = "Resignation - " + sender
        return self._format_email(subj, body, sender, "formal")
    
    def _cover_letter_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting("formal", recipient)
        
        body = greeting + "\n\n"
        body += "I am writing to express my strong interest in the " + subject + " position at " + company + ".\n\n"
        
        if points:
            body += "I believe I am an excellent candidate for this role because:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I am excited about the opportunity to bring my skills and experience to " + company + " and contribute to the team's success.\n\n"
        body += "I have attached my resume for your review. I would welcome the opportunity to discuss how my background and skills would be a good fit for this position.\n\n"
        body += "Thank you for considering my application. I look forward to hearing from you."
        
        subj = "Application for " + subject + " Position"
        return self._format_email(subj, body, sender, "formal")
    
    def _cold_outreach_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope this email finds you well. I came across " + company + " and was impressed by " + subject + ".\n\n"
        
        body += "I am reaching out because I believe there may be an opportunity for us to collaborate.\n\n"
        
        if points:
            body += "Specifically, I can help with:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I would love the chance to learn more about your current challenges and explore if there's a fit.\n\n"
        body += "Would you be open to a brief 15-minute call this week? I am flexible on timing and happy to work around your schedule."
        
        subj = subject + " - Quick Introduction"
        return self._format_email(subj, body, sender, tone)
    
    def _reminder_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I hope you are doing well. I wanted to send a friendly reminder about " + subject + ".\n\n"
        
        if points:
            body += "Key details:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "Please let me know if you have any questions or if there is anything I can assist with.\n\n"
        body += "Thank you for your attention to this matter."
        
        subj = "Reminder: " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _congratulations_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I just heard the wonderful news about " + subject + ", and I wanted to reach out to offer my heartfelt congratulations!\n\n"
        
        if points:
            body += "This achievement is truly remarkable because:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "Your hard work and dedication have clearly paid off, and this success is well-deserved.\n\n"
        body += "Wishing you continued success in all your future endeavors!"
        
        subj = "Congratulations on " + subject
        return self._format_email(subj, body, sender, tone)
    
    def _rejection_email(self, recipient, sender, subject, points, tone):
        greeting = self._get_greeting("professional", recipient)
        
        body = greeting + "\n\n"
        body += "Thank you for your interest in " + subject + ". After careful consideration, we regret to inform you that we will not be moving forward at this time.\n\n"
        
        if points:
            body += "While we were impressed by many aspects of your application, we have decided to:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "This decision was not easy, as we received many qualified applications. We encourage you to apply for future opportunities that match your skills and experience.\n\n"
        body += "We wish you the best in your future endeavors and thank you again for your time and interest."
        
        subj = "Regarding Your Application - " + subject
        return self._format_email(subj, body, sender, "professional")
    
    def _acceptance_email(self, recipient, sender, subject, points, tone, company):
        greeting = self._get_greeting(tone, recipient)
        
        body = greeting + "\n\n"
        body += "I am thrilled to accept " + subject + ". Thank you for this wonderful opportunity!\n\n"
        
        if points:
            body += "I am particularly excited about:\n\n"
            for point in points:
                body += "- " + point + "\n"
            body += "\n"
        
        body += "I am looking forward to joining " + company + " and contributing to the team. Please let me know the next steps and any documentation or information you need from me.\n\n"
        body += "Thank you again for your confidence in me. I am eager to get started!"
        
        subj = "Acceptance: " + subject
        return self._format_email(subj, body, sender, tone)