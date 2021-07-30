from django.db import models

class Computation(models.Model):
    matrix_1 = models.CharField(max_length=200)
    matrix_2 = models.CharField(max_length=200)
    result = models.CharField(max_length=200)

class Operation(models.Model):
    computation = models.ForeignKey(Computation, on_delete=models.CASCADE)
    op_text = models.CharField(max_length=200)
    def __str__(self):
        return self.op_text