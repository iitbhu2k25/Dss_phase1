from django.db import models

class PopulationData(models.Model):
    state_code = models.IntegerField()
    district_code = models.IntegerField()
    subdistrict_code = models.IntegerField()
    village_code = models.IntegerField()
    region_name = models.CharField(max_length=255)
    population_2011 = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'population_data'

    def __str__(self):
        return self.region_name

class PopulationDataYear(models.Model):
    state_code = models.IntegerField()
    district_code = models.IntegerField()
    subdistrict_code = models.IntegerField()
    region_name = models.CharField(max_length=255)
    population_1951 = models.IntegerField()
    population_1961 = models.IntegerField()
    population_1971 = models.IntegerField()
    population_1981 = models.IntegerField()
    population_1991 = models.IntegerField()
    population_2001 = models.IntegerField()
    population_2011 = models.IntegerField()

    class Meta:
        db_table = 'population_data_year'

class FloatingData(models.Model):
    state_code = models.IntegerField()
    district_code = models.IntegerField()
    region_name = models.CharField(max_length=255)
    enumeration_code = models.CharField(max_length=10)
    floating_pop = models.IntegerField()
    subdistrict_code = models.IntegerField()
    village_code = models.IntegerField()

    class Meta:
        db_table = 'floating_data'