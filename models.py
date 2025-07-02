from django.db import models
from django.utils import timezone
from django.db import models

from django.db import models

class CriminalRecord(models.Model):
    name = models.CharField(max_length=200)
    case_number = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.case_number}"
    



class CriminalRecord(models.Model):
    # Choices for sex field
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    ]
    
    # Choices for race field
    RACE_CHOICES = [
        ('WHITE', 'White'),
        ('BLACK', 'Black/African American'),
        ('HISPANIC', 'Hispanic/Latino'),
        ('ASIAN', 'Asian'),
        ('NATIVE', 'Native American'),
        ('PACIFIC', 'Pacific Islander'),
        ('OTHER', 'Other'),
        ('UNKNOWN', 'Unknown'),
    ]
    
    # Main fields
    defendant_name = models.CharField(max_length=200, help_text="Full name of the defendant")
    birth_date = models.DateField(null=True, blank=True, help_text="Date of birth")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='U')
    race = models.CharField(max_length=20, choices=RACE_CHOICES, default='UNKNOWN')
    
    # Case information
    case_number = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Unique case identifier"
    )
    date_filed = models.DateField(null=True, blank=True, help_text="Date case was filed")
    charges = models.TextField(help_text="Multiple charges separated by semicolons or newlines")
    arrest_citation_date = models.DateField(null=True, blank=True, help_text="Date of arrest or citation")
    parish = models.CharField(max_length=100, help_text="Parish where case was filed")
    
    # System fields
    alert_available = models.BooleanField(default=False, help_text="Whether alert is available")
    scraped_timestamp = models.DateTimeField(default=timezone.now, help_text="When this record was scraped")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'criminal_records'
        ordering = ['-scraped_timestamp']
        verbose_name = 'Criminal Record'
        verbose_name_plural = 'Criminal Records'
        indexes = [
            models.Index(fields=['case_number']),
            models.Index(fields=['defendant_name']),
            models.Index(fields=['parish']),
            models.Index(fields=['scraped_timestamp']),
        ]
    
    def __str__(self):
        return f"{self.defendant_name} - {self.case_number}"
    
    def get_charges_list(self):
        """Return charges as a list, split by semicolons or newlines"""
        if self.charges:
            # Split by semicolon first, then by newlines
            charges = self.charges.replace('\n', ';').split(';')
            return [charge.strip() for charge in charges if charge.strip()]
        return []
    
    def get_age_at_filing(self):
        """Calculate age at time of filing if both dates are available"""
        if self.birth_date and self.date_filed:
            return self.date_filed.year - self.birth_date.year - (
                (self.date_filed.month, self.date_filed.day) < 
                (self.birth_date.month, self.birth_date.day)
            )
      
        return None