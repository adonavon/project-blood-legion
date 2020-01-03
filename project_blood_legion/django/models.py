from django.db import models
from django.conf import settings
from django.contrib import admin

class Character(models.Model):
	DRUID = 'DR'
	HUNTER = 'HU'
	MAGE = 'MA'
	PALADIN = 'PA'
	PRIEST = 'PR'
	ROGUE = 'RO'
	SHAMAN = 'SH'
	WARLOCK = 'WL'
	WARRIOR = 'WR'
	CLS_CHOICES = [
		(DRUID, 'Druid'),
		(HUNTER, 'Hunter'),
		(MAGE, 'Mage'),
		(PALADIN, 'Paladin'),
		(PRIEST, 'Priest'),
		(ROGUE, 'Rogue'),
		(SHAMAN, 'Shaman'),
		(WARLOCK, 'Warlock'),
		(WARRIOR, 'Warrior'),
	]

	DWARF = 'DW'
	GNOME = 'GN'
	HUMAN = 'HU'
	NIGHT_ELF = 'NE'
	ORC = 'OR'
	TAUREN = 'TA'
	TROLL = 'TR'
	UNDEAD = 'UD'
	RACE_CHOICES = [
		(DWARF, 'Dwarf'),
		(GNOME, 'Gnome'),
		(HUMAN, 'Human'),
		(NIGHT_ELF, 'Night Elf'),
		(ORC, 'Orc'),
		(TAUREN, 'Tauren'),
		(TROLL, 'Troll'),
		(UNDEAD, 'Undead'),
	]

	name = models.CharField(
		max_length=100,
		unique=True,
	)
	cls = models.CharField(max_length=2, choices=CLS_CHOICES)
	race = models.CharField(max_length=2, choices=RACE_CHOICES)
	items = models.ManyToManyField('Item', through='Loot')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Zone(models.Model):
	name = models.CharField(
		max_length=100,
		unique=True,
	)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Boss(models.Model):
	zone = models.ForeignKey(
		Zone,
		on_delete=models.CASCADE,
	)
	name = models.CharField(
		max_length=100,
	)

	def __str__(self):
		if self.name == 'Trash':
			return 'Trash ({})'.format(self.zone)
		return self.name

	class Meta:
		verbose_name = 'boss'
		verbose_name_plural = 'bosses'
		unique_together = ['zone', 'name']

class Raid(models.Model):
	zone = models.ForeignKey(
		Zone,
		on_delete=models.CASCADE,
	)
	reset = models.IntegerField()
	start = models.DateTimeField()
	end = models.DateTimeField()

	def __str__(self):
		return '{} (Reset {})'.format(self.zone, self.reset)

	def ordered_loot(self):
                return self.loot_set.order_by('boss__id', 'character')

	def uninstanced_ordered_loot(self):
                return self.loot_set.filter(instance=None).order_by('boss__id', 'character')

	class Meta:
		ordering = ['zone', 'reset']
		unique_together = ['zone', 'reset']

class Instance(models.Model):
	raid = models.ForeignKey(
		Raid,
		on_delete=models.CASCADE,
	)
	name = models.CharField(
		max_length=100,
	)
	characters = models.ManyToManyField(Character)
	scheduled_start = models.DateTimeField()

	def ordered_characters(self):
                return self.characters.order_by('cls', 'name')

	def __str__(self):
		return '{} → {}'.format(self.name, self.raid)

	def ordered_loot(self):
                return self.loot_set.order_by('boss__id', 'character')

	class Meta:
		ordering = ['raid', 'name']
		unique_together = ['raid', 'name']

class Item(models.Model):
	POOR = 'P'
	COMMON = 'C'
	UNCOMMON = 'U'
	RARE = 'R'
	EPIC = 'E'
	LEGENDARY = 'L'
	ARTIFACT = 'A'
	QUALITY_CHOICES = [
		(POOR, 'Poor'),
		(COMMON, 'Common'),
		(UNCOMMON, 'Uncommon'),
		(RARE, 'Rare'),
		(EPIC, 'Epic'),
		(LEGENDARY, 'Legendary'),
		(ARTIFACT, 'Artifact'),
	]

	name = models.CharField(
		max_length=100,
	)
	quality = models.CharField(max_length=1, choices=QUALITY_CHOICES)
	classicdb_id = models.IntegerField()

	def __str__(self):
		if self.classicdb_id == 18563:
			return 'Bindings of the Windseeker (Left)'
		elif self.classicdb_id == 18564:
			return 'Bindings of the Windseeker (Right)'
		return self.name

	def get_url(self):
		return 'https://classicdb.ch/?item={}'.format(self.classicdb_id)

	def ordered_loot(self):
                return self.loot_set.order_by('instance__scheduled_start', 'character')

	class Meta:
		ordering = ['name']

class Loot(models.Model):
	character = models.ForeignKey(
		Character,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	item = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
	)
	raid = models.ForeignKey(
		Raid,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	instance = models.ForeignKey(
		Instance,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	boss = models.ForeignKey(
		Boss,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)

	def __str__(self):
		return '{} → {}'.format(self.item, self.character)

	class Meta:
		verbose_name = 'loot'
		verbose_name_plural = 'loot'
		ordering = ['character', 'item']

class LootAdmin(admin.ModelAdmin):
	list_display = ('item', 'character', 'instance', 'raid', 'boss')

class Member(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	main_character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return '{} ({})'.format(self.main_character, self.user)

	class Meta:
		ordering = ['main_character']

class Alt(models.Model):
	member = models.ForeignKey(
		Member,
		on_delete=models.CASCADE,
	)
	character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return '{} ({})'.format(self.character, self.member.main_character)

class Note(models.Model):
	character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)
	text = models.TextField()

	def __str__(self):
		return '{}'.format(self.character)

	class Meta:
		ordering = ['character']
