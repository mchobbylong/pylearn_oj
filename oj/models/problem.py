from django.db import models

from .tag import Tag

class Problem(models.Model):
	pid = models.AutoField(primary_key=True)
	level = models.SmallIntegerField()
	title = models.CharField(max_length=64, db_index=True)
	description = models.TextField()
	visible = models.BooleanField(default=True)

	testset = models.ForeignKey(
		'TestSet',
		models.SET_NULL,
		related_name='+',
		null=True,
		blank=True,
	)

	tags = models.ManyToManyField(Tag, related_name='problems', blank=True)

	class Meta:
		ordering = ['pid']

	def __str__(self):
		return '%d. %s' % (self.pid, self.title)

	@property
	def ac_rate(self):
		valid_submissions = self.submissions.exclude(result='')
		total = valid_submissions.count()
		ac = valid_submissions.filter(score__isnull=False, score=models.F('full_score')).count()
		return ac / total if total > 0 else 0
