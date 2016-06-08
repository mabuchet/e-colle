#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = [
url(r'^(\d+)$', views.connec,name="login_colleur"),
url(r'^action$', views.action,name="action_colleur"),
url(r'^action/note/(\d+)$', views.note,name="note_colleur"),
url(r'^action/note/eleve/(\d+)/(\d+)$', views.noteEleve,name="noteeleve_colleur"),
url(r'^action/note/groupe/(\d+)$', views.noteGroupe,name="notegroupe_colleur"),
url(r'^action/note/modifier/(\d+)$', views.noteModif,name="notemodif_colleur"),
url(r'^action/note/supprimer/(\d+)$', views.noteSuppr,name="notesuppr_colleur"),
url(r'^action/resultat/(\d+)$', views.resultat,name="resultat_colleur"),
url(r'^action/resultat/(\d+)/(\d+)/(\d+)$', views.resultat2,name="resultat2_colleur"),
url(r'^action/resultat/csv/(\d+)/(\d+)/(\d+)$', views.resultatcsv,name="resultatcsv_colleur"),
url(r'^action/programme/(\d+)$', views.programme,name="programme_colleur"),
url(r'^action/programme/modifier/(\d+)$', views.programmeModif,name="programmemodif_colleur"),
url(r'^action/programme/supprimer/(\d+)$', views.programmeSuppr,name="programmesuppr_colleur"),
url(r'^action/groupe/(\d+)$', views.groupe,name="groupe_colleur"),
url(r'^action/groupe/supprimer/(\d+)$', views.groupeSuppr,name="groupesuppr_colleur"),
url(r'^action/groupe/modifier/(\d+)$', views.groupeModif,name="groupemodif_colleur"),
url(r'^action/eleves/(\d+)$', views.eleves,name="eleves_colleur"),
url(r'^action/colloscope/(\d+)$', views.colloscope,name="colloscope_colleur"),
url(r'^action/colloscope/(\d+)/(\d+)/(\d+)$', views.colloscope2,name="colloscope2_colleur"),
url(r'^action/colloscope/pdf/(\d+)/(\d+)/(\d+)$', views.colloscopePdf,name="colloscopepdf_colleur"),
url(r'^action/colloscope/modifier/(\d+)/(\d+)/(\d+)$', views.colloscopeModif,name="colloscopemodif_colleur"),
url(r'^action/creneau/modifier/(\d+)/(\d+)/(\d+)$', views.creneauModif,name="creneaumodif_colleur"),
url(r'^action/creneau/supprimer/(\d+)/(\d+)/(\d+)$', views.creneauSuppr,name="creneausuppr_colleur"),
url(r'^action/creneau/dupliquer/(\d+)/(\d+)/(\d+)$', views.creneauDupli,name="creneaudupli_colleur"),
url(r'^action/colloscope/ajax/(\d+)/(\d+)/(\d+)/(\d+|semaine)/(\d+|creneau)$', views.ajaxcolloscope,name="ajax_colleur"),
url(r'^action/colloscope/ajax/eleve/(\d+)/(\d+)/(\d+)/(\d+|semaine)/(\d+|creneau)/(\w{2,3})$', views.ajaxcolloscopeeleve,name="ajax_colleur_eleve"),
url(r'^action/colloscope/ajax/compat/(\d+)$', views.ajaxcompat,name="ajaxcompat_colleur"),
url(r'^action/colloscope/ajax/majcolleur/(\d+|matiere)/(\d+)$', views.ajaxmajcolleur,name="ajaxmaj_colleur"),
url(r'^action/colloscope/ajax/effacer/(\d+|semaine)/(\d+|creneau)$', views.ajaxcolloscopeeffacer,name="ajaxeffacer_colleur"),
url(r'^action/colloscope/ajax/multi/(\d+|matiere)/(\d+|kolleur)/(\d+|groupe)/(\d+|eleve)/(\d+|semaine)/(\d+|creneau)/([1-9]{1}|[1-2]{1}[0-9]{1}|30|duree)/(1|2|3|4|8|frequence)/([1-9]{1}|1[0-9]{1}|20|permu)$', views.ajaxcolloscopemulti,name="ajaxmulti_colleur"),
url(r'^action/colloscope/ajax/multi/confirm/(\d+|matiere)/(\d+|kolleur)/(\d+|groupe)/(\d+|eleve)/(\d+|semaine)/(\d+|creneau)/([1-9]{1}|[1-2]{1}[0-9]{1}|30|duree)/(1|2|3|4|8|frequence)/([1-9]{1}|1[0-9]{1}|20|permu)$', views.ajaxcolloscopemulticonfirm,name="ajaxmulticonfirm_colleur"),
url(r'^action/agenda$', views.agenda,name="agenda_colleur"),
url(r'^action/note/colle/(\d+)$', views.colleNote,name="collenote_colleur"),
url(r'^action/note/colleeleve/(\d+)$', views.colleNoteEleve,name="collenoteeleve_colleur"),
url(r'^action/decompte$', views.decompte,name="decompte_colleur"),
url(r'^action/changemat/(\d+)$', views.changemat,name="changemat_colleur"),
url(r'^action/ects/matieres/(\d+)$', views.ectsmatieres,name="ects_matieres"),
url(r'^action/ects/matiere/modif/(\d+)$', views.ectsmatieremodif,name="ects_matiere_modif"),
url(r'^action/ects/matiere/suppr/(\d+)$', views.ectsmatieresuppr,name="ects_matiere_suppr"),
url(r'^action/ects/notes/(\d+)$', views.ectsnotes,name="ects_notes"),
]