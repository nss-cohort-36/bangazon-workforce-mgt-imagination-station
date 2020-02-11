from django.db import models

class TrainingProgram(models.Model):
    '''
    description: 
    author: 
    properties:
      
    '''

    title = models.CharField(max_length=55)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    employees = models.ManyToManyField("Employee", through='EmployeeTrainingProgram')

    class Meta:
        verbose_name = ("Training_program")
        verbose_name_plural = ("Training_programs")

    def get_absolute_url(self):
        return reverse("Training_program_detail", kwargs={"pk": self.pk})
