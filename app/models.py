from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    skills = models.CharField(max_length=500, help_text="Comma-separated skills")

    def get_skill_list(self):
        # returns list of skills trimmed lowercase
        return [skill.strip().lower() for skill in self.skills.split(",") if skill.strip()]
    def __str__(self):
        return self.title

class ResumeMatch(models.Model):
    resume_file = models.FileField(upload_to="resumes/")
    extracted_skills = models.TextField()  # JSON string of skills
    matched_jobs = models.ManyToManyField(Job, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
