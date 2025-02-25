# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Club(models.Model):
    _name = 'competicion.club'
    _description = 'Gestión de Club'

    name = fields.Char(string='Nombre del Club:', required=True)
    ciudad = fields.Char(string='Ciudad:')
    pabellon = fields.Char(string='Nombre del Pabellón:')
    equipo_ids = fields.One2many('competicion.equipo', 'club_id', string='Equipos:')  # Relación con Equipo


class Equipo(models.Model):
    _name = 'competicion.equipo'
    _description = 'Gestión de Equipos'

    name = fields.Char(string='Nombre del Equipo:', required=True)
    entrenador = fields.Char(string='Entrenador:', required=True)    
    club_id = fields.Many2one('competicion.club', string='Club:')
    jugador_ids = fields.One2many('competicion.jugador', 'equipo_id', string='Jugadores')  # Relación con Jugador
    altura_media = fields.Float(string='Altura Media', compute='_compute_altura_media', store=True)  # Campo calculado

    @api.depends('jugador_ids.altura')  # Dependencia para recalcular cuando cambie la altura de los jugadores
    def _compute_altura_media(self):
        for equipo in self:
            if equipo.jugador_ids:  # Si hay jugadores en el equipo
                alturas = [jugador.altura for jugador in equipo.jugador_ids if jugador.altura]  # Filtra alturas válidas
                equipo.altura_media = sum(alturas) / len(alturas) if alturas else 0.0  # Calcula la media
            else:
                equipo.altura_media = 0.0  # Si no hay jugadores, la altura media es 0


class Jugador(models.Model):
    _name = 'competicion.jugador'
    _description = 'Gestión de Jugadores'

    name = fields.Char(string='Nombre del Jugador:', required=True)
    posicion = fields.Char(string='Posición:')
    altura = fields.Float(string='Altura (m):')
    numero = fields.Integer(string='Número:')
    equipo_id = fields.Many2one('competicion.equipo', string='Equipo')