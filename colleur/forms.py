#-*- coding: utf-8 -*-
from django import forms
from accueil.models import Colleur, Note, Semaine, Programme, Eleve, Creneau, Matiere, Groupe
from django.db.models import Q
from datetime import date, timedelta
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError

class ColleurConnexionForm(forms.Form):
	def __init__(self,matiere, *args, **kwargs):
		super().__init__(*args, **kwargs)
		query=Colleur.objects.filter(matieres=matiere,user__is_active=True).order_by('user__last_name','user__first_name')
		self.fields['colleur'] = forms.ModelChoiceField(label="Colleur",queryset=query, empty_label=None)
		self.fields['password'] = forms.CharField(label="Mot de passe",widget=forms.PasswordInput)

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields=['semaine','jour','heure','note','commentaire','rattrapee','date_colle']
		widgets = {'date_colle':SelectDateWidget(years=[date.today().year+i-1 for i in range(10)])}

		def clean(self):
			"""Vérifie que le colleur n'a pas déjà 3 notes sur ce créneau et qu'il n'a pas déjà collé l'élève cette semaine dans cette matière"""
			colleur = self.instance.colleur
			if not self.cleaned_data['rattrapee']:
				self.cleaned_data['date_colle']=self.instance.cleaned_data['semaine'].lundi+timedelta(days=int(self.cleaned_data['jour']))
			nbNotesColleur=Note.objects.filter(date_colle=self.cleaned_data['date_colle'],colleur=self.cleaned_data['colleur'],heure=self.cleaned_data['heure'])
			if self.instance.pk: # si c'est une modification, on ne prend pas en compte la colle courante
				nbNotesColleur = nbNotesColleur.exclude(pk=self.instance.pk)
			nbNotesColleur=nbNotesColleur.count()
			if nbNotesColleur>=3:
				raise ValidationError('Vous avez déjà 3 notes sur ce créneau')
			nbNotesEleve=Note.objects.filter(semaine=self.cleaned_data['semaine'],matiere=self.cleaned_data['matiere'],colleur=self.cleaned_data['colleur'],eleve=self.cleaned_data['eleve']).count()
			if nbNotesEleve !=0 and self.cleaned_data['eleve']:
				raise ValidationError('Vous avez déjà collé cet élève dans cette matière cette semaine')


class NoteGroupeForm(forms.Form):
	def __init__(self, groupe, matiere, colleur, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.groupe=groupe
		self.matiere=matiere
		self.colleur=colleur
		LISTE_HEURE=[(i,"{}h{:02d}".format(i//4,15*(i%4))) for i in range(28,88)]
		LISTE_JOUR=enumerate(["lundi","mardi","mercredi","jeudi","vendredi","samedi"])
		LISTE_NOTE=[('',"---"),(21,"n.n"),(22,"Abs")]
		LISTE_NOTE.extend(zip(range(21),range(21)))
		LISTE_NOTE_NULL=[('',"---"),(21,"n.n")]
		nbeleves = groupe.groupeeleve.count()
		self.fields['semaine']=forms.ModelChoiceField(label="Semaine",queryset=Semaine.objects.all(), empty_label=None)
		self.fields['jour']=forms.ChoiceField(label="Jour",choices=LISTE_JOUR)
		self.fields['heure']=forms.ChoiceField(label="Heure",choices=LISTE_HEURE)
		self.fields['rattrapee']=forms.BooleanField(required=False)
		self.fields['date_colle']=forms.DateField(label="date de rattrapage",widget=SelectDateWidget(years=[date.today().year+i-1 for i in range(10)]),initial=date.today)
		self.fields['note0']=forms.ChoiceField(label="Note",choices=LISTE_NOTE,required=False)
		self.fields['commentaire0']=forms.CharField(label="Commentaire(facultatif)",widget=forms.Textarea,required=False)
		self.fields['note1']=forms.ChoiceField(label="Note",choices=LISTE_NOTE if nbeleves>=2 else LISTE_NOTE_NULL,required=False)
		self.fields['commentaire1']=forms.CharField(label="Commentaire(facultatif)",widget=forms.Textarea,required=False)
		self.fields['note2']=forms.ChoiceField(label="Note",choices=LISTE_NOTE if nbeleves>=3 else LISTE_NOTE_NULL,required=False)
		self.fields['commentaire2']=forms.CharField(label="Commentaire(facultatif)",widget=forms.Textarea,required=False)

	def clean(self):
		"""Vérifie que le colleur n'aura au final pas plus de 3 notes sur ce créneau et qu'il n'a pas déjà collé un des élève cette semaine dans cette matière"""
		eleves=self.groupe.groupeeleve.all()
		if not self.cleaned_data['rattrapee']:
				self.cleaned_data['date_colle']=self.cleaned_data['semaine'].lundi+timedelta(days=int(self.cleaned_data['jour']))
		nbNotesColleur=Note.objects.filter(date_colle=self.cleaned_data['date_colle'],colleur=self.colleur,heure=self.cleaned_data['heure']).count()
		if nbNotesColleur !=0:
			raise ValidationError("Vous avez déjà des notes sur ce créneau horaire")
		nbNotesEleve=Note.objects.filter(semaine=self.cleaned_data['semaine'],matiere=self.matiere,colleur=self.colleur,eleve__in=eleves).exists()
		if nbNotesEleve:
			raise ValidationError("Vous avez déjà noté un des élèves cette semaine dans cette matière")

	def save(self):
		"""sauvegarde en base de données les notes dont la valeur n'est pas None"""
		eleves=list(self.groupe.groupeeleve.all())
		eleves+=[None]*(3-len(eleves))
		notes=[Note(colleur=self.colleur,matiere=self.matiere,semaine=self.cleaned_data['semaine'],date_colle=self.cleaned_data['date_colle'],rattrapee=self.cleaned_data['rattrapee']\
				,jour=self.cleaned_data['jour'],note=self.cleaned_data['note{}'.format(i)],eleve=eleve,classe=self.groupe.classe,heure=self.cleaned_data['heure']\
				,commentaire=self.cleaned_data['commentaire{}'.format(i)] if eleve is not None else None) for i,eleve in enumerate(eleves) if self.cleaned_data['note{}'.format(i)]]
		Note.objects.bulk_create(notes) # on sauvegarde toutes les notes en une seule requête

			
class ProgrammeForm(forms.ModelForm):
	class Meta:
		model = Programme
		fields=['semaine','titre','detail','fichier']

class GroupeForm(forms.Form):
	def __init__(self,classe,groupe, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.groupe=groupe
		self.classe=classe
		if not groupe:
			query=Eleve.objects.filter(groupe__isnull=True,classe=classe).select_related('user')
		else:
			query=Eleve.objects.filter(classe=classe).filter(Q(groupe__isnull=True)|Q(groupe=groupe)).select_related('user')
		self.fields['nom'] = forms.CharField(label="nom")
		self.fields['eleve0'] = forms.ModelChoiceField(label="Premier élève",queryset=query,empty_label="Élève fictif",required=True)
		self.fields['eleve1'] = forms.ModelChoiceField(label="Deuxième élève",queryset=query,empty_label="Élève fictif",required=False)
		self.fields['eleve2'] = forms.ModelChoiceField(label="Troisième élève",queryset=query,empty_label="Élève fictif",required=False)

	def clean_nom(self):
		"""Validation du champ nom (unicité pour une classe donnée)"""
		data = self.cleaned_data['nom']
		query = Groupe.objects.filter(nom=data,classe=self.classe)
		if self.groupe: # si c'est une modification, on exclut de la requête le groupe en question
			query=query.exclude(pk=self.groupe.pk)
		if query.exists():
			raise ValidationError(
    		"le nom %(value)s est déjà pris",
    		code='uniqueness violation',
    		params={'value': data},
			)
		return data

	def clean(self):
		"""validation du formulaire. S'il y a deux fois le même élève (non fictif) on lève une ValidationError"""
		eleves = [self.cleaned_data['eleve{}'.format(i)] for i in range(3) if 'eleve{}'.format(i) in self.cleaned_data and self.cleaned_data['eleve{}'.format(i)]]
		if len(eleves) > len(set(eleves)): # s'il y a doublon
			raise ValidationError("Un élève ne peut apparaître qu'une fois dans un groupe",code="uniqueness violation")

	def save(self):
		"""sauvegarde en base de données les données du formulaire"""
		if self.groupe: # dans le cas d'une modification
			groupe=self.groupe
			Eleve.objects.filter(groupe=groupe).update(groupe=None) # on efface les groupes des -anciens- élèves du groupe
			Groupe.objects.filter(pk=groupe.pk).update(nom=self.cleaned_data['nom']) # on met à jour le nom du groupe
		else: # sinon on crée un nouveau groupe
			groupe=Groupe(nom=self.cleaned_data['nom'],classe=self.classe)
			groupe.save()
		Eleve.objects.filter(pk__in=[self.cleaned_data['eleve{}'.format(i)].pk for i in range(3) if self.cleaned_data['eleve{}'.format(i)] is not None]).update(groupe=groupe) # maj des groupes

class CreneauForm(forms.ModelForm):
	class Meta:
		model = Creneau
		fields = ['jour','heure','salle']

class SemaineForm(forms.Form):
	try:
		query=Semaine.objects.order_by('lundi')
		semin=forms.ModelChoiceField(queryset=query, empty_label=None,initial=query[0])
		semax=forms.ModelChoiceField(queryset=query, empty_label=None,initial=query[query.count()-1])
	except Exception:
		semin=forms.ModelChoiceField(queryset=Semaine.objects.none(), empty_label=None)
		semax=forms.ModelChoiceField(queryset=Semaine.objects.none(), empty_label=None)

class ColleForm(forms.Form):
	def __init__(self,classe, *args, **kwargs):
		super().__init__(*args, **kwargs)
		query1=Matiere.objects.all()
		query2=Colleur.objects.none()
		query3=Groupe.objects.filter(classe=classe).order_by('nom')
		try:
			self.fields['matiere']=forms.ModelChoiceField(queryset=query1,empty_label=None,initial=query1[0])
		except Exception:
			self.fields['matiere']=forms.ModelChoiceField(queryset=query1,empty_label=None)
		self.fields['colleur']=forms.ModelChoiceField(queryset=query2,empty_label=None)
		try:
			self.fields['groupe']=forms.ModelChoiceField(queryset=query3,empty_label=None,initial=query3[0])
		except Exception:
			self.fields['groupe']=forms.ModelChoiceField(queryset=query3,empty_label=None)
		DUREE=[(1,"1 semaine")]+list(zip(range(2,31),["{} semaines".format(i) for i in range (2,31)]))
		PERMUTATION=[(i,"de {} en {}".format(i,i)) for i in range(1,21)]
		FREQUENCE=[(i,"une semaine sur {}".format(i)) for i in (1,2,3,4,8)]
		self.fields['duree']=forms.ChoiceField(label="Durée",choices=DUREE)
		self.fields['frequence']=forms.ChoiceField(label="Fréquence",choices=FREQUENCE)
		self.fields['permutation']=forms.ChoiceField(label="Permutation des groupes",choices=PERMUTATION)

class EleveForm(forms.Form):
	def __init__(self,classe,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['eleve'] = forms.ModelChoiceField(label = "Élève",queryset=Eleve.objects.filter(classe=classe))




	