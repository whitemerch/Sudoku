#!/usr/bin/python3
#-*-coding: utf8-*-

from grid import *
class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        Ces contraintes seront appliquées en appelant la méthode ``reduce_all_domains``.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.table = []
        self.grid = grid
        self.reduce_all_domains()
        #raise NotImplementedError()

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for elt in self.grid.get_empty_pos():
            liste_valeurs_possibles = set()
            ligne = list(self.grid.get_row(elt[0]))
            colonne = list(self.grid.get_col(elt[1]))
            region = list(self.grid.get_region(elt[0] // 3, elt[1] // 3))
            for i in range(1, 10):
                if i not in ligne and i not in colonne and i not in region:
                    liste_valeurs_possibles.add(i)
            self.table.append((elt, liste_valeurs_possibles))
        #raise NotImplementedError()

    def reduce_domains(self, last_i, last_j, last_v):
        """À COMPLÉTER
        Cette méthode devrait être appelée à chaque mise à jour de la grille,
        et élimine la dernière valeur affectée à une case
        pour toutes les autres cases concernées par cette mise à jour (même ligne, même colonne ou même région).
        :param last_i: Numéro de ligne de la dernière case modifiée, entre 0 et 8
        :param last_j: Numéro de colonne de la dernière case modifiée, entre 0 et 8
        :param last_v: Valeur affecté à la dernière case modifiée, entre 1 et 9
        :type last_i: int
        :type last_j: int
        :type last_v: int
        """
        for elt in self.table:
            region_elt = (elt[0][0] // 3, elt[0][1] // 3)
            region = (last_i // 3, last_j // 3)
            if last_v in elt[1] and (elt[0][0] == last_i or elt[0][1] == last_j or (region_elt == region)):
                elt[1].remove(last_v)
        #raise NotImplementedError()

    def commit_one_var(self):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        tuple = ()
        for elt in self.table:
            if len(elt[1]) == 1:
                self.grid.write(elt[0][0], elt[0][1], next(iter(elt[1])))
                tuple = (elt[0][0], elt[0][1], next(iter(elt[1])))
                return tuple
        return None
        #raise NotImplementedError()

    def solve_step(self):
        """À COMPLÉTER
        Cette méthode alterne entre l'affectation de case pour lesquelles il n'y a plus qu'une possibilité
        et l'élimination des nouvelles valeurs impossibles pour les autres cases concernées.
        Elle répète cette alternance tant qu'il reste des cases à remplir,
        et correspond à la résolution de Sudokus dits «simple».
        *Variante avancée: en plus de vérifier s'il ne reste plus qu'une seule possibilité pour une case,
        il est aussi possible de vérifier s'il ne reste plus qu'une seule position valide pour une certaine valeur
        sur chaque ligne, chaque colonne et dans chaque région*
        """
        derniere_poss = -1
        while derniere_poss is not None:
            derniere_poss = self.commit_one_var()
            if derniere_poss is not None:
                self.reduce_domains(derniere_poss[0], derniere_poss[1], derniere_poss[2])
                self.table.remove(((derniere_poss[0], derniere_poss[1]), set()))
                derniere_poss = ()
        #raise NotImplementedError()

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        for element in self.table:
            if element[1] != set():
                return True
            else:
                return False
        #raise NotImplementedError()

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        solution_complete = False
        if not list(self.grid.get_empty_pos()):
            solution_complete = True
        return solution_complete
        #raise NotImplementedError()

    def branch(self):
        """À COMPLÉTER
        Cette méthode sélectionne une variable libre dans la solution partielle actuelle,
        et crée autant de sous-problèmes que d'affectation possible pour cette variable.
        Ces sous-problèmes seront sous la forme de nouvelles instances de solver
        initialisées avec une grille partiellement remplie.
        *Variante avancée: Renvoyez un générateur au lieu d'une liste.*
        *Variante avancée: Un choix judicieux de variable libre,
        ainsi que l'ordre dans lequel les affectations sont testées
        peut fortement améliorer les performances de votre solver.*
        :return: Une liste de sous-problèmes ayant chacun une valeur différente pour la variable choisie
        :rtype: list of SudokuSolver
        """
        liste_sol = []
        tuple_min = ()
        dic_min = {}
        self.table.sort()
        tuple_min = self.table[0][0]
        dic_min = self.table[0][1]
        for i in dic_min:
            grille_en_cours = self.grid.copy()
            grille_en_cours.write(tuple_min[0], tuple_min[1], i)
            sous_probleme = self.__class__(grille_en_cours)
            liste_sol.append(sous_probleme)
        return liste_sol
        #raise NotImplementedError()

    def solve(self):
        """
        Cette méthode implémente la fonction principale de la programmation par contrainte.
        Elle cherche d'abord à affiner au mieux la solution partielle actuelle par un appel à ``solve_step``.
        Si la solution est complète, elle la retourne.
        Si elle est invalide, elle renvoie ``None`` pour indiquer un cul-de-sac dans la recherche de solution
        et déclencher un retour vers la précédente solution valide.
        Sinon, elle crée plusieurs sous-problèmes pour explorer différentes possibilités
        en appelant récursivement ``solve`` sur ces sous-problèmes.
        :return: Une solution pour la grille de Sudoku donnée à l'initialisation du solver
        (ou None si pas de solution)
        :rtype: SudokuGrid or None
        """
        self.solve_step()
        if self.is_solved():
            return self.grid
        elif self.is_valid():
            k = self.branch()
            for elt in k:
                s = elt.solve()
                if s is not None:
                    return s
            return None
        else:
            return None
        #raise NotImplementedError()
