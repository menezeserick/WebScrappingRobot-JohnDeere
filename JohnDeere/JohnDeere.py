# -*- coding: utf-8 -*-
"""
Created on WED Feb 12 10:07

@author: C30622B
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from tkinter.scrolledtext import ScrolledText
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup


class DealerLocatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("John Deere Dealer Locator")

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        # Configuração do estilo para o cabeçalho sem bordas e com centralização
        self.style.configure('Header.TLabel',
                             font=('Helvetica', 18, 'bold'),
                             foreground='#333333',
                             anchor='center',
                             relief='flat',
                             borderwidth=0)
        # Configuração do estilo para o status (processamento) sem bordas e com centralização
        self.style.configure('Status.TLabel',
                             font=('Helvetica', 10),
                             foreground='#555555',
                             anchor='center',
                             relief='flat',
                             borderwidth=0)
        self.style.configure('TButton',
                             font=('Helvetica', 10),
                             padding=5)

        
        self.listadecidades = [
            'Buenos Aires - Buenos Aires F.D. - ARGENTINA',
            'Córdoba - Cordoba - ARGENTINA',
            'Tucumán - Tucuman - ARGENTINA',
            'Salta - Salta - ARGENTINA',
            'Rosario - Santa Fe - ARGENTINA',
            'Mar del Plata - Buenos Aires - ARGENTINA',
            'Santa Fe - Santa Fe - ARGENTINA',
            'Corrientes - Corrientes - ARGENTINA',
            'Posadas - Misiones - ARGENTINA',
            'Bahía Blanca - Buenos Aires - ARGENTINA',
            'La Rioja - La Rioja - ARGENTINA',
            'Santiago del Estero - Santiago del Estero - ARGENTINA',
            'Santa Rosa - La Pampa - ARGENTINA',
            'San Salvador de Jujuy - Jujuy - ARGENTINA',
            'San Luis - San Luis - ARGENTINA',
            'San Juan - San Juan - ARGENTINA',
            'Catamarca - Catamarca - ARGENTINA',
            'Río Gallegos - Santa Cruz - ARGENTINA',
            'Paraná - Entre Rios - ARGENTINA',
            'Neuquén - Neuquen - ARGENTINA',
            'Mendoza - Mendoza - ARGENTINA',
            'Ushuaia - Tierra del Fuego - ARGENTINA',
            'La Plata - Buenos Aires - ARGENTINA',
            'Formosa - Formosa - ARGENTINA',
            'Resistencia - Chaco - ARGENTINA',
            'Bariloche - Rio Negro - ARGENTINA',
            'San Rafael - Mendoza - ARGENTINA',
            'Río Cuarto - Cordoba - ARGENTINA',
            'Rawson - Chubut - ARGENTINA',
            'Viedma - Rio Negro - ARGENTINA',
            'Trelew - Chubut - ARGENTINA',
            'Concordia - Entre Rios - ARGENTINA',
            'Tandil - Buenos Aires - ARGENTINA',
            'Quilmes - Buenos Aires - ARGENTINA',
            'Comodoro Rivadavia - Chubut - ARGENTINA',
            'Villa Mercedes - San Luis - ARGENTINA',
            'San Miguel - Buenos Aires - ARGENTINA',
            'Orán - Salta - ARGENTINA',
            'San Nicolás de los Arroyos - Buenos Aires - ARGENTINA',
            'Río Grande - Tierra del Fuego - ARGENTINA',
            'Rafaela - Santa Fe - ARGENTINA',
            'Puerto Madryn - Chubut - ARGENTINA',
            'Presidencia Roque Sáenz Peña - Chaco - ARGENTINA',
            'Olavarría - Buenos Aires - ARGENTINA',
            'Villa Carlos Paz - Cordoba - ARGENTINA',
            'Venado Tuerto - Santa Fe - ARGENTINA',
            'Morón - Buenos Aires - ARGENTINA',
            'Merlo - Buenos Aires - ARGENTINA',
            'Luján - Buenos Aires - ARGENTINA',
            'Gualeguaychú - Entre Rios - ARGENTINA',
            'Concepción del Uruguay - Entre Rios - ARGENTINA',
            'Castelar - Buenos Aires - ARGENTINA',
            'Belgrano - Buenos Aires F.D. - ARGENTINA',
            'Zárate - Buenos Aires - ARGENTINA',
            'Villa Lugano - Buenos Aires F.D. - ARGENTINA',
            'San Antonio de Padua - Buenos Aires - ARGENTINA',
            'Puerto Iguazú - Misiones - ARGENTINA',
            'Cipolletti - Rio Negro - ARGENTINA',
            'Junín - Buenos Aires - ARGENTINA',
            'General Roca - Rio Negro - ARGENTINA',
            'Balvanera - Buenos Aires F.D. - ARGENTINA',
            'Santo Tomé - Santa Fe - ARGENTINA',
            'San Martín - Mendoza - ARGENTINA',
            'San Francisco - Cordoba - ARGENTINA',
            'Río Tercero - Cordoba - ARGENTINA',
            'Pergamino - Buenos Aires - ARGENTINA',
            'Villa María - Cordoba - ARGENTINA',
            'Tartagal - Salta - ARGENTINA',
            'Oberá - Misiones - ARGENTINA',
            'Necochea - Buenos Aires - ARGENTINA',
            'Mercedes - Buenos Aires - ARGENTINA',
            'Los Polvorines - Buenos Aires - ARGENTINA',
            'Ituzaingó - Corrientes - ARGENTINA',
            'Goya - Corrientes - ARGENTINA',
            'El Palomar - Buenos Aires - ARGENTINA',
            'Don Torcuato - Buenos Aires - ARGENTINA',
            'Campana - Buenos Aires - ARGENTINA',
            'Berazategui - Buenos Aires - ARGENTINA',
            'Bella Vista - Buenos Aires - ARGENTINA',
            'Barranqueras - Chaco - ARGENTINA',
            'Barracas - Buenos Aires F.D. - ARGENTINA',
            'Azul - Buenos Aires - ARGENTINA',
            'Reconquista - Santa Fe - ARGENTINA',
            'Puerto Eldorado - Misiones - ARGENTINA',
            'Pilar - Buenos Aires - ARGENTINA',
            'El Calafate - Santa Cruz - ARGENTINA',
            'Gobernador Gálvez - Santa Fe - ARGENTINA',
            'General Pico - La Pampa - ARGENTINA',
            'Esquel - Chubut - ARGENTINA',
            'Caleta Olivia - Santa Cruz - ARGENTINA',
            'Colonia Ayuí - Entre Rios - ARGENTINA',
            'Lincoln - Buenos Aires - ARGENTINA',
            'Libertador General San Martín - Jujuy - ARGENTINA',
            'Las Parejas - Santa Fe - ARGENTINA',
            'Las Lomitas - Formosa - ARGENTINA',
            'Las Breñas - Chaco - ARGENTINA',
            'La Quiaca - Jujuy - ARGENTINA',
            'Colonia Lapin - Buenos Aires - ARGENTINA',
            'La Falda - Cordoba - ARGENTINA',
            'San Pedro de Jujuy - Jujuy - ARGENTINA',
            'San Martín de los Andes - Neuquen - ARGENTINA',
            'San Carlos Centro - Santa Fe - ARGENTINA',
            'Rufino - Santa Fe - ARGENTINA',
            'Roldán - Santa Fe - ARGENTINA',
            'Río Segundo - Cordoba - ARGENTINA',
            'Río Mayo - Chubut - ARGENTINA',
            'Río Ceballos - Cordoba - ARGENTINA',
            'Recreo - Catamarca - ARGENTINA',
            'Quitilipi - Chaco - ARGENTINA',
            'Punta Alta - Buenos Aires - ARGENTINA',
            'Puerto Deseado - Santa Cruz - ARGENTINA',
            'Plottier - Neuquen - ARGENTINA',
            'Plaza Huincul - Neuquen - ARGENTINA',
            'Pilar - Cordoba - ARGENTINA',
            'Pico Truncado - Santa Cruz - ARGENTINA',
            'Pérez - Santa Fe - ARGENTINA',
            'Palpalá - Jujuy - ARGENTINA',
            'Oncativo - Cordoba - ARGENTINA',
            'Nueve de Julio - Buenos Aires - ARGENTINA',
            'Morteros - Cordoba - ARGENTINA',
            'Merlo - San Luis - ARGENTINA',
            'Machagai - Chaco - ARGENTINA',
            'Zapala - Neuquen - ARGENTINA',
            'Yerba Buena - Tucuman - ARGENTINA',
            'Villa Regina - Rio Negro - ARGENTINA',
            'Villa Dolores - Cordoba - ARGENTINA',
            'Villa Constitución - Santa Fe - ARGENTINA',
            'Villa Ángela - Chaco - ARGENTINA',
            'Villa Allende - Cordoba - ARGENTINA',
            'Victoria - Entre Rios - ARGENTINA',
            'Unquillo - Cordoba - ARGENTINA',
            'Tres Arroyos - Buenos Aires - ARGENTINA',
            'Termas de Río Hondo - Santiago del Estero - ARGENTINA',
            'Tafí Viejo - Tucuman - ARGENTINA',
            'Sunchales - Santa Fe - ARGENTINA',
            'Muñiz - Buenos Aires - ARGENTINA',
            'Mercedes - Corrientes - ARGENTINA',
            'Haedo - Buenos Aires - ARGENTINA',
            'Jardín América - Misiones - ARGENTINA',
            'Hurlingham - Buenos Aires - ARGENTINA',
            'Gualeguay - Entre Rios - ARGENTINA',
            'Gobernador Virasoro - Corrientes - ARGENTINA',
            'General Pacheco - Buenos Aires - ARGENTINA',
            'General José de San Martín - Chaco - ARGENTINA',
            'Garupá - Misiones - ARGENTINA',
            'Fontana - Chaco - ARGENTINA',
            'Esquina - Corrientes - ARGENTINA',
            'El Colorado - Formosa - ARGENTINA',
            'Dos de Mayo - Misiones - ARGENTINA',
            'Dolores - Buenos Aires - ARGENTINA',
            'Curuzú Cuatiá - Corrientes - ARGENTINA',
            'Text corpus - Misiones - ARGENTINA',
            'Colegiales - Buenos Aires F.D. - ARGENTINA',
            'Chajarí - Entre Rios - ARGENTINA',
            'Campo Ramón - Misiones - ARGENTINA',
            'Boedo - Buenos Aires F.D. - ARGENTINA',
            'Balcarce - Buenos Aires - ARGENTINA',
            'Avellaneda - Santa Fe - ARGENTINA',
            'Aristóbulo del Valle - Misiones - ARGENTINA',
            'Colonia Wanda - Misiones - ARGENTINA',
            'Villa Ocampo - Santa Fe - ARGENTINA',
            'Villaguay - Entre Rios - ARGENTINA',
            'Villa Gesell - Buenos Aires - ARGENTINA',
            'Villa de Mayo - Buenos Aires - ARGENTINA',
            'Veinticinco de Mayo - Misiones - ARGENTINA',
            'Tortuguitas - Buenos Aires - ARGENTINA',
            'Tigre - Buenos Aires - ARGENTINA',
            'San Vicente - Misiones - ARGENTINA',
            'Santos Lugares - Buenos Aires - ARGENTINA',
            'Santa Elena - Entre Rios - ARGENTINA',
            'San Pedro - Buenos Aires - ARGENTINA',
            'San Lorenzo - Corrientes - ARGENTINA',
            'San Isidro - Buenos Aires - ARGENTINA',
            'San Clemente del Tuyú - Buenos Aires - ARGENTINA',
            'Retiro - Buenos Aires F.D. - ARGENTINA',
            'Pontevedra - Buenos Aires - ARGENTINA',
            'Paso de los Libres - Corrientes - ARGENTINA',
            'Pampa del Indio - Chaco - ARGENTINA',
            'El Quebrachal - Salta - ARGENTINA',
            'El Bolsón - Rio Negro - ARGENTINA',
            'Cutral-Có - Neuquen - ARGENTINA',
            'Cruz del Eje - Cordoba - ARGENTINA',
            'Crespo - Entre Rios - ARGENTINA',
            'Coronel Suárez - Buenos Aires - ARGENTINA',
            'Cinco Saltos - Rio Negro - ARGENTINA',
            'Chos Malal - Neuquen - ARGENTINA',
            'Chivilcoy - Buenos Aires - ARGENTINA',
            'Chilecito - La Rioja - ARGENTINA',
            'Charata - Chaco - ARGENTINA',
            'Chacabuco - Buenos Aires - ARGENTINA',
            'Joaquín V. González - Salta - ARGENTINA',
            'Jesús María - Cordoba - ARGENTINA',
            'Hernando - Cordoba - ARGENTINA',
            'Granadero Baigorria - Santa Fe - ARGENTINA',
            'General Mosconi - Salta - ARGENTINA',
            'Gálvez - Santa Fe - ARGENTINA',
            'Funes - Santa Fe - ARGENTINA',
            'Fray Luis A. Beltrán - Santa Fe - ARGENTINA',
            'Fraile Pintado - Jujuy - ARGENTINA',
            'Firmat - Santa Fe - ARGENTINA',
            'Famaillá - Tucuman - ARGENTINA',
            'Esperanza - Santa Fe - ARGENTINA',
            'Embarcación - Salta - ARGENTINA',
            'Embalse - Cordoba - ARGENTINA',
            'El Trébol - Santa Fe - ARGENTINA',
            'Ceres - Santa Fe - ARGENTINA',
            'Centenario - Neuquen - ARGENTINA',
            'Caucete - San Juan - ARGENTINA',
            'Catriel - Rio Negro - ARGENTINA',
            'Juan José Castelli - Chaco - ARGENTINA',
            'Casilda - Santa Fe - ARGENTINA',
            'Carcarañá - Santa Fe - ARGENTINA',
            'Capitán Bermúdez - Santa Fe - ARGENTINA',
            'Cañada de Gómez - Santa Fe - ARGENTINA',
            'Cafayate - Salta - ARGENTINA',
            'Bell Ville - Cordoba - ARGENTINA',
            'Arroyo Seco - Santa Fe - ARGENTINA',
            'Arroyito - Cordoba - ARGENTINA',
            'Arrecifes - Buenos Aires - ARGENTINA',
            'Armstrong - Santa Fe - ARGENTINA',
            'Arauco - La Rioja - ARGENTINA',
            'Alta Gracia - Cordoba - ARGENTINA',
            'Allen - Rio Negro - ARGENTINA',
            'Alderetes - Tucuman - ARGENTINA',
            'Albardón - San Juan - ARGENTINA',
            'Aguilares - Tucuman - ARGENTINA',
            'Villa Santa Rita - Buenos Aires F.D. - ARGENTINA',
            'Adrogué - Buenos Aires - ARGENTINA',
            'José C. Paz - Buenos Aires - ARGENTINA',
            'Ingeniero Pablo Nogués - Buenos Aires - ARGENTINA',
            'Villa Sarmiento - Buenos Aires - ARGENTINA',
            'Campo de Mayo - Buenos Aires - ARGENTINA',
            'Cariló - Buenos Aires - ARGENTINA',
            'La Punta - San Luis - ARGENTINA',
            'Moreno - Buenos Aires - ARGENTINA',
            'Los Menucos - Rio Negro - ARGENTINA',
            'Los Juríes - Santiago del Estero - ARGENTINA',
            'Los Frentones - Chaco - ARGENTINA',
            'Los Cocos - Cordoba - ARGENTINA',
            'Los Antiguos - Santa Cruz - ARGENTINA',
            'Los Altos - Catamarca - ARGENTINA',
            'Lonquimay - La Pampa - ARGENTINA',
            'Londres - Catamarca - ARGENTINA',
            'Las Rosas - Santa Fe - ARGENTINA',
            'Las Ovejas - Neuquen - ARGENTINA',
            'Las Lajitas - Salta - ARGENTINA',
            'Las Heras - Santa Cruz - ARGENTINA',
            'Puerta de San José - Catamarca - ARGENTINA',
            'La Mendieta - Jujuy - ARGENTINA',
            'La Maruja - La Pampa - ARGENTINA',
            'Lamarque - Rio Negro - ARGENTINA',
            'Laguna Paiva - Santa Fe - ARGENTINA',
            'Lago Puelo - Chubut - ARGENTINA',
            'Santa Rosa de Tastil - Salta - ARGENTINA',
            'Santa Rosa de Calamuchita - Cordoba - ARGENTINA',
            'Jovita - Cordoba - ARGENTINA',
            'Santa Lucía - San Juan - ARGENTINA',
            'San Justo - Santa Fe - ARGENTINA',
            'San José de Jáchal - San Juan - ARGENTINA',
            'San Jorge - Santa Fe - ARGENTINA',
            'San Cristóbal - Santa Fe - ARGENTINA',
            'San Bernardo - Chaco - ARGENTINA',
            'San Benito - Entre Rios - ARGENTINA',
            'San Antonio Oeste - Rio Negro - ARGENTINA',
            'San Antonio - Catamarca - ARGENTINA',
            'Samuhú - Chaco - ARGENTINA',
            'Río Pico - Chubut - ARGENTINA',
            'Rancul - La Pampa - ARGENTINA',
            'Rada Tilly - Chubut - ARGENTINA',
            'Alfredo Demarchi - Buenos Aires - ARGENTINA',
            'Quimilí - Santiago del Estero - ARGENTINA',
            'Puerta de Corral Quemado - Catamarca - ARGENTINA',
            'Salvador Mazza - Salta - ARGENTINA',
            'Pozo del Tigre - Formosa - ARGENTINA',
            'Pomán - Catamarca - ARGENTINA',
            'Pocito - San Juan - ARGENTINA',
            'Perito Moreno - Santa Cruz - ARGENTINA',
            'Pascanas - Cordoba - ARGENTINA',
            'Pampa de los Guanacos - Santiago del Estero - ARGENTINA',
            'Palma Sola - Jujuy - ARGENTINA',
            'Oro Verde - Entre Rios - ARGENTINA',
            'Oliva - Cordoba - ARGENTINA',
            'Nono - Cordoba - ARGENTINA',
            'Naschel - San Luis - ARGENTINA',
            'Napenay - Chaco - ARGENTINA',
            'Mutquin - Catamarca - ARGENTINA',
            'Monteros - Tucuman - ARGENTINA',
            'Monte Buey - Cordoba - ARGENTINA',
            'Miramar - Cordoba - ARGENTINA',
            'Mina Clavero - Cordoba - ARGENTINA',
            'Miguel Riglos - La Pampa - ARGENTINA',
            'Mariano Moreno - Neuquen - ARGENTINA',
            'Marcos Juárez - Cordoba - ARGENTINA',
            'Malvinas Argentinas - Cordoba - ARGENTINA',
            'Mainqué - Rio Negro - ARGENTINA',
            'Maimará - Jujuy - ARGENTINA',
            'Luján - San Luis - ARGENTINA',
            'Los Varela - Catamarca - ARGENTINA',
            'Yacimientos Río Turbio - Santa Cruz - ARGENTINA',
            'Winifreda - La Pampa - ARGENTINA',
            'Wenceslao Escalante - Cordoba - ARGENTINA',
            'Vista Alegre Norte - Neuquen - ARGENTINA',
            'Villa Urquiza - Entre Rios - ARGENTINA',
            'Villa Paula de Sarmiento - San Juan - ARGENTINA',
            'Villa Nueva - Cordoba - ARGENTINA',
            'Villa La Angostura - Neuquen - ARGENTINA',
            'Villa Giardino - Cordoba - ARGENTINA',
            'Villa General Mitre - Santiago del Estero - ARGENTINA',
            'Villa General Belgrano - Cordoba - ARGENTINA',
            'Villa del Dique - Cordoba - ARGENTINA',
            'Villa Cañás - Santa Fe - ARGENTINA',
            'Villa Bustos - La Rioja - ARGENTINA',
            'Villa Berthet - Chaco - ARGENTINA',
            'Vicuña Mackenna - Cordoba - ARGENTINA',
            'Viale - Entre Rios - ARGENTINA',
            'Vera - Santa Fe - ARGENTINA',
            '28 de Noviembre - Santa Cruz - ARGENTINA',
            'Valle Hermoso - Cordoba - ARGENTINA',
            'Uriburu - La Pampa - ARGENTINA',
            'Unión - San Luis - ARGENTINA',
            'Trevelin - Chubut - ARGENTINA',
            'Tres Isletas - Chaco - ARGENTINA',
            'Tres Algarrobos - Buenos Aires - ARGENTINA',
            'Totoras - Santa Fe - ARGENTINA',
            'Tostado - Santa Fe - ARGENTINA',
            'Tintina - Santiago del Estero - ARGENTINA',
            'Tinogasta - Catamarca - ARGENTINA',
            'Tilisarao - San Luis - ARGENTINA',
            'Telén - La Pampa - ARGENTINA',
            'Taco Pozo - Chaco - ARGENTINA',
            'Seguí - Entre Rios - ARGENTINA',
            'Saturnino María Laspiur - Cordoba - ARGENTINA',
            'Nueve de Julio - Corrientes - ARGENTINA',
            'Monte Caseros - Corrientes - ARGENTINA',
            'Montecarlo - Misiones - ARGENTINA',
            'Mojón Grande - Misiones - ARGENTINA',
            'Mártires - Misiones - ARGENTINA',
            'Malvinas Sur - Corrientes - ARGENTINA',
            'Maciá - Entre Rios - ARGENTINA',
            'Lucas González - Entre Rios - ARGENTINA',
            'Los Helechos - Misiones - ARGENTINA',
            'Los Charrúas - Entre Rios - ARGENTINA',
            'Loreto - Misiones - ARGENTINA',
            'La Verde - Chaco - ARGENTINA',
            'Las Garcitas - Chaco - ARGENTINA',
            'Larroque - Entre Rios - ARGENTINA',
            'La Paz - Entre Rios - ARGENTINA',
            'Lapachito - Chaco - ARGENTINA',
            'Lanús - Buenos Aires - ARGENTINA',
            'La Leonesa - Chaco - ARGENTINA',
            'Laguna Limpia - Chaco - ARGENTINA',
            'La Escondida - Chaco - ARGENTINA',
            'La Eduvigis - Chaco - ARGENTINA',
            'Isidro Casanova - Buenos Aires - ARGENTINA',
            'Ibarreta - Formosa - ARGENTINA',
            'Herrera - Entre Rios - ARGENTINA',
            'Herradura - Formosa - ARGENTINA',
            'Hasenkamp - Entre Rios - ARGENTINA',
            'Guaraní - Misiones - ARGENTINA',
            'Gobernador Roca - Misiones - ARGENTINA',
            'Gobernador Mansilla - Entre Rios - ARGENTINA',
            'Gobernador Juan E. Martínez - Corrientes - ARGENTINA',
            'General Vedia - Chaco - ARGENTINA',
            'General Galarza - Entre Rios - ARGENTINA',
            'General Campos - Entre Rios - ARGENTINA',
            'General Alvear - Misiones - ARGENTINA',
            'Garuhapé - Misiones - ARGENTINA',
            'Florentino Ameghino - Misiones - ARGENTINA',
            'Federal - Entre Rios - ARGENTINA',
            'Federación - Entre Rios - ARGENTINA',
            'El Soberbio - Misiones - ARGENTINA',
            'Colonia El Curundú - Chaco - ARGENTINA',
            'El Alcázar - Misiones - ARGENTINA',
            'Dos Arroyos - Misiones - ARGENTINA',
            'Villa Domínguez - Entre Rios - ARGENTINA',
            'Colonias Unidas - Chaco - ARGENTINA',
            'Colonia Benítez - Chaco - ARGENTINA',
            'Colonia Aurora - Misiones - ARGENTINA',
            'Clorinda - Formosa - ARGENTINA',
            'Ciervo Petiso - Chaco - ARGENTINA',
            'Chavarría - Corrientes - ARGENTINA',
            'Cerro Corá - Misiones - ARGENTINA',
            'Cerro Azul - Misiones - ARGENTINA',
            'Ceibas - Entre Rios - ARGENTINA',
            'Iguazu Falls - Misiones - ARGENTINA',
            'Caseros - Entre Rios - ARGENTINA',
            'Caraguatay - Misiones - ARGENTINA',
            'Capitán Solari - Chaco - ARGENTINA',
            'Capioví - Misiones - ARGENTINA',
            'Candelaria - Misiones - ARGENTINA',
            'Campo Viera - Misiones - ARGENTINA',
            'Campo Grande - Misiones - ARGENTINA',
            'Burzaco - Buenos Aires - ARGENTINA',
            'Bovril - Entre Rios - ARGENTINA',
            'Bonpland - Corrientes - ARGENTINA',
            'Bernardo de Irigoyen - Misiones - ARGENTINA',
            'Basail - Chaco - ARGENTINA',
            'Banfield - Buenos Aires - ARGENTINA',
            'Azara - Misiones - ARGENTINA',
            'Arroyo del Medio - Misiones - ARGENTINA',
            'Almafuerte - Misiones - ARGENTINA',
            'Aldea San Antonio - Entre Rios - ARGENTINA',
            'Yapeyú - Corrientes - ARGENTINA',
            'Villa Ortúzar - Buenos Aires F.D. - ARGENTINA',
            'María Grande - Entre Rios - ARGENTINA',
            'Villa Mantero - Entre Rios - ARGENTINA',
            'Villa Hernandarias - Entre Rios - ARGENTINA',
            'Villa Elisa - Entre Rios - ARGENTINA',
            'Villa del Rosario - Entre Rios - ARGENTINA',
            'Urdinarrain - Entre Rios - ARGENTINA',
            'Ubajay - Entre Rios - ARGENTINA',
            'Tres Capones - Misiones - ARGENTINA',
            'Tacuarendí - Santa Fe - ARGENTINA',
            'Sauce de Luna - Entre Rios - ARGENTINA',
            'Santo Tomé - Corrientes - ARGENTINA',
            'Santo Pipó - Misiones - ARGENTINA',
            'Santa Rosa - Corrientes - ARGENTINA',
            'Santa María - Misiones - ARGENTINA',
            'Santa Lucía - Corrientes - ARGENTINA',
            'Santa Ana - Entre Rios - ARGENTINA',
            'San Salvador - Entre Rios - ARGENTINA',
            'San Pedro - Misiones - ARGENTINA',
            'San Luis del Palmar - Corrientes - ARGENTINA',
            'San José de Feliciano - Entre Rios - ARGENTINA',
            'San José - Misiones - ARGENTINA',
            'San Javier - Santa Fe - ARGENTINA',
            'San Carlos - Corrientes - ARGENTINA',
            'Saladas - Corrientes - ARGENTINA',
            'Ruiz de Montoya - Misiones - ARGENTINA',
            'Rosario del Tala - Entre Rios - ARGENTINA',
            'Puerto Vilelas - Chaco - ARGENTINA',
            'Puerto Rico - Misiones - ARGENTINA',
            'Puerto Piray - Misiones - ARGENTINA',
            'Puerto Libertad - Misiones - ARGENTINA',
            'Puerto Leoni - Misiones - ARGENTINA',
            'Puerto Ibicuy - Entre Rios - ARGENTINA',
            'Puerto Esperanza - Misiones - ARGENTINA',
            'Puerto Bermejo - Chaco - ARGENTINA',
            'Pronunciamiento - Entre Rios - ARGENTINA',
            'Presidencia Roca - Chaco - ARGENTINA',
            'Presidencia de la Plaza - Chaco - ARGENTINA',
            'Pirané - Formosa - ARGENTINA',
            'Gobernador López - Misiones - ARGENTINA',
            'Pedro R. Fernández - Corrientes - ARGENTINA',
            'Panambí - Misiones - ARGENTINA',
            'Pampa Almirón - Chaco - ARGENTINA',
            'El Maitén - Chubut - ARGENTINA',
            'El Galpón - Salta - ARGENTINA',
            'El Aguilar - Jujuy - ARGENTINA',
            'Dolavón - Chubut - ARGENTINA',
            'Diamante - Entre Rios - ARGENTINA',
            'Deán Funes - Cordoba - ARGENTINA',
            'Darwin - Rio Negro - ARGENTINA',
            'Dalmacio Vélez - Cordoba - ARGENTINA',
            'Cosquín - Cordoba - ARGENTINA',
            'Corzuela - Chaco - ARGENTINA',
            'Corral de Bustos - Cordoba - ARGENTINA',
            'Coronel Du Graty - Chaco - ARGENTINA',
            'Coronel Dorrego - Buenos Aires - ARGENTINA',
            'Coronel Belisle - Rio Negro - ARGENTINA',
            'Coronda - Santa Fe - ARGENTINA',
            'Concepción del Bermejo - Chaco - ARGENTINA',
            'Comandante Luis Piedrabuena - Santa Cruz - ARGENTINA',
            'Comallo - Rio Negro - ARGENTINA',
            'Colonia Dora - Santiago del Estero - ARGENTINA',
            'Colonia Barón - La Pampa - ARGENTINA',
            'Clodomira - Santiago del Estero - ARGENTINA',
            'Chorotis - Chaco - ARGENTINA',
            'Chimpay - Rio Negro - ARGENTINA',
            'Chimbas - San Juan - ARGENTINA',
            'Chichinales - Rio Negro - ARGENTINA',
            'Chamical - La Rioja - ARGENTINA',
            'Cervantes - Rio Negro - ARGENTINA',
            'La Cumbre - Cordoba - ARGENTINA',
            'La Clotilde - Chaco - ARGENTINA',
            'La Carlota - Cordoba - ARGENTINA',
            'La Calera - Cordoba - ARGENTINA',
            'Laboulaye - Cordoba - ARGENTINA',
            'Justo Daract - San Luis - ARGENTINA',
            'Junín de los Andes - Neuquen - ARGENTINA',
            'Jacinto Aráuz - La Pampa - ARGENTINA',
            'Ingeniero Luis A. Huergo - Rio Negro - ARGENTINA',
            'Ingeniero Luiggi - La Pampa - ARGENTINA',
            'Ingeniero Jacobacci - Rio Negro - ARGENTINA',
            'Ingeniero Guillermo N. Juárez - Formosa - ARGENTINA',
            'Icaño - Catamarca - ARGENTINA',
            'Humahuaca - Jujuy - ARGENTINA',
            'Huinca Renancó - Cordoba - ARGENTINA',
            'Huillapima - Catamarca - ARGENTINA',
            'Hualfín - Catamarca - ARGENTINA',
            'El Hoyo - Chubut - ARGENTINA',
            'Gobernador Costa - Chubut - ARGENTINA',
            'General Villegas - Buenos Aires - ARGENTINA',
            'General San Martín - La Pampa - ARGENTINA',
            'Villa General Ramírez - Entre Rios - ARGENTINA',
            'General Pinedo - Chaco - ARGENTINA',
            'General Manuel J. Campos - La Pampa - ARGENTINA',
            'General Fernández Oro - Rio Negro - ARGENTINA',
            'General Enrique Godoy - Rio Negro - ARGENTINA',
            'General Cabrera - Cordoba - ARGENTINA',
            'General Acha - La Pampa - ARGENTINA',
            'Gancedo - Chaco - ARGENTINA',
            'Fray Luis Beltrán - Rio Negro - ARGENTINA',
            'Fiambalá - Catamarca - ARGENTINA',
            'Estanislao del Campo - Formosa - ARGENTINA',
            'Embajador Martini - La Pampa - ARGENTINA',
            'Castro Barros - La Rioja - ARGENTINA',
            'Capilla del Monte - Cordoba - ARGENTINA',
            'Capayán - Catamarca - ARGENTINA',
            'Candelaria - San Luis - ARGENTINA',
            'Campo Quijano - Salta - ARGENTINA',
            'Campo Largo - Chaco - ARGENTINA',
            'Calingasta - San Juan - ARGENTINA',
            'Calilegua - Jujuy - ARGENTINA',
            'Caleufú - La Pampa - ARGENTINA',
            'Caimancito - Jujuy - ARGENTINA',
            'Buta Ranquil - Neuquen - ARGENTINA',
            'Brinkmann - Cordoba - ARGENTINA',
            'Bernardo Larroudé - La Pampa - ARGENTINA',
            'Beltrán - Santiago del Estero - ARGENTINA',
            'Bella Vista - Tucuman - ARGENTINA',
            'Barrancas - Neuquen - ARGENTINA',
            'Avia Terai - Chaco - ARGENTINA',
            'Arias - Cordoba - ARGENTINA',
            'Aranguren - Entre Rios - ARGENTINA',
            'Apolinario Saravia - Salta - ARGENTINA',
            'Anguil - La Pampa - ARGENTINA',
            'Andalgalá - Catamarca - ARGENTINA',
            'Añatuya - Santiago del Estero - ARGENTINA',
            'Alta Italia - La Pampa - ARGENTINA',
            'Alpachiri - La Pampa - ARGENTINA',
            'Almafuerte - Cordoba - ARGENTINA',
            'Yacimientos Río Turbio - Santa Cruz - ARGENTINA',
            'Avellaneda - Buenos Aires - ARGENTINA',
            'Gato Colorado - Santa Fe - ARGENTINA',
            'La Adela - La Pampa - ARGENTINA',
            'El Sauzalito - Formosa - ARGENTINA',
            'Pueblo General Belgrano - Entre Rios - ARGENTINA',
            'La Cumbrecita - Cordoba - ARGENTINA',
            'Costa del Este - Buenos Aires - ARGENTINA',
            'Las Grutas - Rio Negro - ARGENTINA',
            'Nordelta - Buenos Aires - ARGENTINA',
            'Carapachay - Buenos Aires - ARGENTINA',
            'Villa Martelli - Buenos Aires - ARGENTINA',
            'Florida Oeste - Buenos Aires - ARGENTINA',
            'Villa Adelina - Buenos Aires - ARGENTINA',
            'Villa Río Bermejito - Chaco - ARGENTINA',
            'Los Molles - San Luis - ARGENTINA',
            'Los Molinos - La Rioja - ARGENTINA',
            'Los Miches - Neuquen - ARGENTINA',
            'Los Corrales - Catamarca - ARGENTINA',
            'Los Cóndores - Cordoba - ARGENTINA',
            'Los Cipreses - Chubut - ARGENTINA',
            'Los Catutos - Neuquen - ARGENTINA',
            'Los Castillos - Catamarca - ARGENTINA',
            'Los Cajones - San Luis - ARGENTINA',
            'Los Blancos - Salta - ARGENTINA',
            'Los Ángeles - Catamarca - ARGENTINA',
            'Loro Huasi - Catamarca - ARGENTINA',
            'López - Santa Fe - ARGENTINA',
            'Loncopué - Neuquen - ARGENTINA',
            'Loma Blanca - La Rioja - ARGENTINA',
            'Líbano - Buenos Aires - ARGENTINA',
            'Leones - Cordoba - ARGENTINA',
            'León - Jujuy - ARGENTINA',
            'Leandro N. Alem - Buenos Aires - ARGENTINA',
            'Leandro N. Alem - San Luis - ARGENTINA',
            'La Viña - Catamarca - ARGENTINA',
            'Lavalle - Santiago del Estero - ARGENTINA',
            'Lavaisse - San Luis - ARGENTINA',
            'La Unión - Salta - ARGENTINA',
            'La Trinidad - Tucuman - ARGENTINA',
            'La Tosca - Mendoza - ARGENTINA',
            'La Toma - San Luis - ARGENTINA',
            'Las Varillas - Cordoba - ARGENTINA',
            'Las Tejas - Catamarca - ARGENTINA',
            'Las Tejas - Santiago del Estero - ARGENTINA',
            'Las Paredes - Mendoza - ARGENTINA',
            'Las Mojarras - Catamarca - ARGENTINA',
            'Las Lajas - Neuquen - ARGENTINA',
            'Las Lagunas - San Luis - ARGENTINA',
            'Las Juntas - Catamarca - ARGENTINA',
            'Las Juntas - Catamarca - ARGENTINA',
            'La Silleta - Salta - ARGENTINA',
            'Las Higueras - Cordoba - ARGENTINA',
            'Las Cuevas - Entre Rios - ARGENTINA',
            'Las Chacras - San Luis - ARGENTINA',
            'Las Cejas - Tucuman - ARGENTINA',
            'Las Cañas - Catamarca - ARGENTINA',
            'Las Bayas - Rio Negro - ARGENTINA',
            'Las Aguadas - San Luis - ARGENTINA',
            'Las Acequias - Cordoba - ARGENTINA',
            'La Ramadita - Catamarca - ARGENTINA',
            'La Puntilla - Catamarca - ARGENTINA',
            'La Punilla - San Luis - ARGENTINA',
            'La Paz - Cordoba - ARGENTINA',
            'La Pampa - Cordoba - ARGENTINA',
            'La Merced - Salta - ARGENTINA',
            'La Maroma - San Luis - ARGENTINA',
            'La Majada - San Luis - ARGENTINA',
            'La Majada - Catamarca - ARGENTINA',
            'La Lobería - Rio Negro - ARGENTINA',
            'La Humada - La Pampa - ARGENTINA',
            'La Hoyada - Catamarca - ARGENTINA',
            'Laguna Yema - Formosa - ARGENTINA',
            'Laguna Blanca - Rio Negro - ARGENTINA',
            'La Guardia - Catamarca - ARGENTINA',
            'Lago Blanco - Chubut - ARGENTINA',
            'La Gloria - La Pampa - ARGENTINA',
            'La Florida - Tucuman - ARGENTINA',
            'Lafinur - San Luis - ARGENTINA',
            'La Emilia - Buenos Aires - ARGENTINA',
            'Sastre - Santa Fe - ARGENTINA',
            'Sarmiento - Chubut - ARGENTINA',
            'Santurce - Santa Fe - ARGENTINA',
            'Santo Tomás - Neuquen - ARGENTINA',
            'Santo Domingo - La Rioja - ARGENTINA',
            'Santa Teresa - La Pampa - ARGENTINA',
            'Santa Sylvina - Chaco - ARGENTINA',
            'Santa Rosa de Río Primero - Cordoba - ARGENTINA',
            'Santa Rosa de los Pastos Grandes - Salta - ARGENTINA',
            'Santa Rosa de Leales - Tucuman - ARGENTINA',
            'Santa Rosa del Conlara - San Luis - ARGENTINA',
            'Santa Rosa - Santa Fe - ARGENTINA',
            'Santa Rosa - Catamarca - ARGENTINA',
            'Santa Rosa - Catamarca - ARGENTINA',
            'Santa Rosa - Salta - ARGENTINA',
            'Santa Rosa - Salta - ARGENTINA',
            'Santa María de Punilla - Cordoba - ARGENTINA',
            'Santa María - Salta - ARGENTINA',
            'Santa Isabel - La Pampa - ARGENTINA',
            'Santa Florentina - La Rioja - ARGENTINA',
            'Santa Cruz - Catamarca - ARGENTINA',
            'Santa Cruz - La Rioja - ARGENTINA',
            'Santa Clara - La Rioja - ARGENTINA',
            'Santa Clara - Jujuy - ARGENTINA',
            'Santa Ana - Jujuy - ARGENTINA',
            'San Sebastián - Tierra del Fuego - ARGENTINA',
            'San Pedro de Colalao - Tucuman - ARGENTINA',
            'San Pedro - Catamarca - ARGENTINA',
            'San Pedro - La Rioja - ARGENTINA',
            'San Pedro de Guasayán - Santiago del Estero - ARGENTINA',
            'San Pablo - San Luis - ARGENTINA',
            'San Pablo - Catamarca - ARGENTINA',
            'San Nicolás - La Rioja - ARGENTINA',
            'San Miguel - La Rioja - ARGENTINA',
            'San Miguel - Catamarca - ARGENTINA',
            'Villa General San Martín - San Juan - ARGENTINA',
            'San Martín - Catamarca - ARGENTINA',
            'San Lorenzo - Salta - ARGENTINA',
            'San Juan - Salta - ARGENTINA',
            'San José - Catamarca - ARGENTINA',
            'San Javier - Rio Negro - ARGENTINA',
            'San Javier - Cordoba - ARGENTINA',
            'San Isidro - Salta - ARGENTINA',
            'San Jerónimo - San Luis - ARGENTINA',
            'San Francisco del Monte de Oro - San Luis - ARGENTINA',
            'San Francisco del Chañar - Cordoba - ARGENTINA',
            'San Fernando - Catamarca - ARGENTINA',
            'San Carlos - Mendoza - ARGENTINA',
            'San Carlos Minas - Cordoba - ARGENTINA',
            'San Antonio de los Cobres - Salta - ARGENTINA',
            'San Antonio de Litín - Cordoba - ARGENTINA',
            'San Antonio - Catamarca - ARGENTINA',
            'San Agustín - Cordoba - ARGENTINA',
            'San Agustín - Salta - ARGENTINA',
            'Salsacate - Cordoba - ARGENTINA',
            'Salicas - La Rioja - ARGENTINA',
            'Villa Salavina - Santiago del Estero - ARGENTINA',
            'Saladillo - San Luis - ARGENTINA',
            'Sachayoj - Santiago del Estero - ARGENTINA',
            'Rucanelo - La Pampa - ARGENTINA',
            'Colana - Catamarca - ARGENTINA',
            'Rivera - Buenos Aires - ARGENTINA',
            'Río Villegas - Rio Negro - ARGENTINA',
            'Río Seco - Tucuman - ARGENTINA',
            'Río Piedras - Salta - ARGENTINA',
            'Río Muerto - Chaco - ARGENTINA',
            'Río del Valle - Salta - ARGENTINA',
            'Río Chico - Rio Negro - ARGENTINA',
            'Rinconadillas - Jujuy - ARGENTINA',
            'Rincón - Catamarca - ARGENTINA',
            'Renca - San Luis - ARGENTINA',
            'Relmo - La Pampa - ARGENTINA',
            'Recreo - Santa Fe - ARGENTINA',
            'Realicó - La Pampa - ARGENTINA',
            'Real del Padre - Mendoza - ARGENTINA',
            'Ramón M. Castro - Neuquen - ARGENTINA',
            'Ramblones - Catamarca - ARGENTINA',
            'Quirós - Catamarca - ARGENTINA',
            'Quilino - Cordoba - ARGENTINA',
            'Quili Malal - Neuquen - ARGENTINA',
            'Quetrequén - La Pampa - ARGENTINA',
            'Quemú Quemú - La Pampa - ARGENTINA',
            'Quehué - La Pampa - ARGENTINA',
            'Quebracho Herrado - Cordoba - ARGENTINA',
            'Purmamarca - Jujuy - ARGENTINA',
            'Punta de Vacas - Mendoza - ARGENTINA',
            'Punta de los Llanos - La Rioja - ARGENTINA',
            'Punta Delgada - Chubut - ARGENTINA',
            'Punta de Balasto - Catamarca - ARGENTINA',
            'Pumahuasi - Jujuy - ARGENTINA',
            'Puiggari - Entre Rios - ARGENTINA',
            'Puesto del Marqués - Jujuy - ARGENTINA',
            'Puerto Santa Cruz - Santa Cruz - ARGENTINA',
            'Puerto San Julián - Santa Cruz - ARGENTINA',
            'Puerto Rawson - Chubut - ARGENTINA',
            'Puerto Pirámides - Chubut - ARGENTINA',
            'Puerto Blest - Rio Negro - ARGENTINA',
            'Puerto Belgrano - Buenos Aires - ARGENTINA',
            'Punta Bandera - Santa Cruz - ARGENTINA',
            'Puente del Inca - Mendoza - ARGENTINA',
            'Puelén - La Pampa - ARGENTINA',
            'Pueblo Brugo - Entre Rios - ARGENTINA',
            'Primero de Mayo - Mendoza - ARGENTINA',
            'Pozo Herrera - Santiago del Estero - ARGENTINA',
            'Pozo de Piedra - Catamarca - ARGENTINA',
            'Potrerillos - Mendoza - ARGENTINA',
            'Potrerillo - San Luis - ARGENTINA',
            'Pontaut - Buenos Aires - ARGENTINA',
            'Pomona - Rio Negro - ARGENTINA',
            'Pluma de Pato - Salta - ARGENTINA',
            'Plaza Vieja - La Rioja - ARGENTINA',
            'Plaza Luxardo - Cordoba - ARGENTINA',
            'Pituil - La Rioja - ARGENTINA',
            'Piquirenda - Salta - ARGENTINA',
            'Piquete Cabado - Salta - ARGENTINA',
            'Piñero - Santa Fe - ARGENTINA',
            'Pilcaniyeu - Rio Negro - ARGENTINA',
            'Piedra del Águila - Neuquen - ARGENTINA',
            'Picún Leufú - Neuquen - ARGENTINA',
            'Pichi Mahuida - Rio Negro - ARGENTINA',
            'Pichi Huinca - La Pampa - ARGENTINA',
            'Pichanal - Salta - ARGENTINA',
            'Perú - La Pampa - ARGENTINA',
            'Perico - Jujuy - ARGENTINA',
            'Pehuajó - Buenos Aires - ARGENTINA',
            'Payogasta - Salta - ARGENTINA',
            'Pavón - Santa Fe - ARGENTINA',
            'Paso Grande - San Luis - ARGENTINA',
            'Paso Flores - Rio Negro - ARGENTINA',
            'Paso de la Arena - Entre Rios - ARGENTINA',
            'Pasco - Cordoba - ARGENTINA',
            'Parera - La Pampa - ARGENTINA',
            'Pampa del Infierno - Chaco - ARGENTINA',
            'Pampa Blanca - Jujuy - ARGENTINA',
            'Palo Negro - Santiago del Estero - ARGENTINA',
            'Palo Labrado - Catamarca - ARGENTINA',
            'Palo Blanco - Catamarca - ARGENTINA',
            'Pagancillo - La Rioja - ARGENTINA',
            'Padre Lozano - Salta - ARGENTINA',
            'Olpas - La Rioja - ARGENTINA',
            'Oliveros - Santa Fe - ARGENTINA',
            'Olaroz Chico - Jujuy - ARGENTINA',
            'Ojeda - La Pampa - ARGENTINA',
            'Nueve de Julio - San Juan - ARGENTINA',
            'Nueva Galia - San Luis - ARGENTINA',
            'Nueva Francia - Santiago del Estero - ARGENTINA',
            'Nuestra Señora de Talavera - Salta - ARGENTINA',
            'Nonogasta - La Rioja - ARGENTINA',
            'Ñirihuau - Rio Negro - ARGENTINA',
            'Nazareno - Salta - ARGENTINA',
            'Navia - San Luis - ARGENTINA',
            'Napalpí - Chaco - ARGENTINA',
            'Naicó - La Pampa - ARGENTINA',
            'Nahuel Niyeu - Rio Negro - ARGENTINA',
            'Nahuel Mapá - San Luis - ARGENTINA',
            'Ñacuñán - Mendoza - ARGENTINA',
            'Nacate - La Rioja - ARGENTINA',
            'Mosmota - San Luis - ARGENTINA',
            'Monte Potrero - Catamarca - ARGENTINA',
            'Monte Nievas - La Pampa - ARGENTINA',
            'Monte Maíz - Cordoba - ARGENTINA',
            'Monte Dinero - Santa Cruz - ARGENTINA',
            'Montecristo - Cordoba - ARGENTINA',
            'Monte Comán - Mendoza - ARGENTINA',
            'Moisés Ville - Santa Fe - ARGENTINA',
            'Misión Chaqueña - Salta - ARGENTINA',
            'Miranda - La Rioja - ARGENTINA',
            'Miraflores - Catamarca - ARGENTINA',
            'Ministro Ramos Mexía - Rio Negro - ARGENTINA',
            'Mina Pirquitas - Jujuy - ARGENTINA',
            'Miguel Cané - La Pampa - ARGENTINA',
            'Metileo - La Pampa - ARGENTINA',
            'Metán Viejo - Salta - ARGENTINA',
            'Mesón de Fierro - Chaco - ARGENTINA',
            'Colonia Merou - Entre Rios - ARGENTINA',
            'Mencué - Rio Negro - ARGENTINA',
            'Medanitos - Catamarca - ARGENTINA',
            'Mayor Buratovich - Buenos Aires - ARGENTINA',
            'Juan F. Salaberry - Buenos Aires - ARGENTINA',
            'Mauricio Mayer - La Pampa - ARGENTINA',
            'Mattaldi - Cordoba - ARGENTINA',
            'María Juana - Santa Fe - ARGENTINA',
            'Margarita - Santa Fe - ARGENTINA',
            'Maquinchao - Rio Negro - ARGENTINA',
            'Manantiales - Catamarca - ARGENTINA',
            'Malligasta - La Rioja - ARGENTINA',
            'Malbrán - Santiago del Estero - ARGENTINA',
            'Malargüe - Mendoza - ARGENTINA',
            'Villa Mailín - Santiago del Estero - ARGENTINA',
            'Maciel - Santa Fe - ARGENTINA',
            'Machigasta - La Rioja - ARGENTINA',
            'Macapillo - Salta - ARGENTINA',
            'Macachín - La Pampa - ARGENTINA',
            'Luracatao - Salta - ARGENTINA',
            'Lunlunta - Mendoza - ARGENTINA',
            'Luis Palacios - Santa Fe - ARGENTINA',
            'Luis Burela - Salta - ARGENTINA',
            'Lugones - Santiago del Estero - ARGENTINA',
            'Luan Toro - La Pampa - ARGENTINA',
            'Loventué - La Pampa - ARGENTINA',
            'Los Telares - Santiago del Estero - ARGENTINA',
            'Los Sarmientos - La Rioja - ARGENTINA',
            'Los Robles - La Rioja - ARGENTINA',
            'Los Ralos - Tucuman - ARGENTINA',
            'Los Quirquinchos - Santa Fe - ARGENTINA',
            'Los Pirpintos - Santiago del Estero - ARGENTINA',
            'Los Palacios - La Rioja - ARGENTINA',
            'Los Núñez - Santiago del Estero - ARGENTINA',
            'Zuberbühler - Chaco - ARGENTINA',
            'Zavalla - Santa Fe - ARGENTINA',
            'Zaparinqui - Chaco - ARGENTINA',
            'Zanjitas - San Luis - ARGENTINA',
            'Yavi Chico - Jujuy - ARGENTINA',
            'Yavi - Jujuy - ARGENTINA',
            'Yacuy - Salta - ARGENTINA',
            'Wheelwright - Santa Fe - ARGENTINA',
            'Weisburd - Santiago del Estero - ARGENTINA',
            'Volcán - Jujuy - ARGENTINA',
            'Villa Vil - Catamarca - ARGENTINA',
            'Villa Tulumba - Cordoba - ARGENTINA',
            'Villa Traful - Neuquen - ARGENTINA',
            'Villa Santa Rita de Catuna - La Rioja - ARGENTINA',
            'Villa Río Hondo - Santiago del Estero - ARGENTINA',
            'Villa Reynolds - San Luis - ARGENTINA',
            'Villa Ojo de Agua - Santiago del Estero - ARGENTINA',
            'Villa Nougues - Tucuman - ARGENTINA',
            'Villa Mirasol - La Pampa - ARGENTINA',
            'Villa Mazán - La Rioja - ARGENTINA',
            'Villa Mascardi - Rio Negro - ARGENTINA',
            'Villa de las Rosas - Cordoba - ARGENTINA',
            'Villa Larca - San Luis - ARGENTINA',
            'Villa Huidobro - Cordoba - ARGENTINA',
            'Villa El Chocón - Neuquen - ARGENTINA',
            'Villa Dolores - Catamarca - ARGENTINA',
            'Villa de Praga - San Luis - ARGENTINA',
            'Villa del Totoral - Cordoba - ARGENTINA',
            'Villa del Carmen - San Luis - ARGENTINA',
            'Villa de la Quebrada - San Luis - ARGENTINA',
            'Villa Cura Brochero - Cordoba - ARGENTINA',
            'Villa Concepción del Tío - Cordoba - ARGENTINA',
            'Chañar Ladeado - Santa Fe - ARGENTINA',
            'Villa Atamisqui - Santiago del Estero - ARGENTINA',
            'Villa Amelia - Santa Fe - ARGENTINA',
            'Vilismán - Catamarca - ARGENTINA',
            'Vilelas - Santiago del Estero - ARGENTINA',
            'Victorica - La Pampa - ARGENTINA',
            'Colonia Vichigasta - La Rioja - ARGENTINA',
            'Viamonte - Cordoba - ARGENTINA',
            'Vértiz - La Pampa - ARGENTINA',
            'Ventura Pampa - Santiago del Estero - ARGENTINA',
            'Venados Grandes - Chaco - ARGENTINA',
            'Veinticinco de Mayo - La Pampa - ARGENTINA',
            'Varvarco - Neuquen - ARGENTINA',
            'Valcheta - Rio Negro - ARGENTINA',
            'Uspallata - Mendoza - ARGENTINA',
            'Urundel - Salta - ARGENTINA',
            'Uranga - Santa Fe - ARGENTINA',
            'Unanué - La Pampa - ARGENTINA',
            'Umberto I - Santa Fe - ARGENTINA',
            'Tuyubil - La Rioja - ARGENTINA',
            'Tucumanao - Catamarca - ARGENTINA',
            'Tricao Malal - Neuquen - ARGENTINA',
            'Tres Sargentos - Buenos Aires - ARGENTINA',
            'Tres Lagos - Santa Cruz - ARGENTINA',
            'Tres Cruces - Jujuy - ARGENTINA',
            'Trenel - La Pampa - ARGENTINA',
            'Trebolares - La Pampa - ARGENTINA',
            'El Trapiche - San Luis - ARGENTINA',
            'Tranquitas - Tucuman - ARGENTINA',
            'Trancas - Tucuman - ARGENTINA',
            'Tolombón - Salta - ARGENTINA',
            'Tolloche - Salta - ARGENTINA',
            'Tolar Grande - Salta - ARGENTINA',
            'Tobantirenda - Salta - ARGENTINA',
            'Tío Pozo - Santiago del Estero - ARGENTINA',
            'Timote - Buenos Aires - ARGENTINA',
            'Tilimuqui - La Rioja - ARGENTINA',
            'Tilcara - Jujuy - ARGENTINA',
            'Ticino - Cordoba - ARGENTINA',
            'Theobald - Santa Fe - ARGENTINA',
            'Tezanos Pinto - Entre Rios - ARGENTINA',
            'Teodelina - Santa Fe - ARGENTINA',
            'Teniente General E. Frías - Rio Negro - ARGENTINA',
            'Tatón - Catamarca - ARGENTINA',
            'Taquimilán - Neuquen - ARGENTINA',
            'Tapso - Santiago del Estero - ARGENTINA',
            'Tanti - Cordoba - ARGENTINA',
            'Talita - San Luis - ARGENTINA',
            'Talapampa - Salta - ARGENTINA',
            'Tafí del Valle - Tucuman - ARGENTINA',
            'Suriyaco - La Rioja - ARGENTINA',
            'Suncho Corral - Santiago del Estero - ARGENTINA',
            'Sumampa - Santiago del Estero - ARGENTINA',
            'Sumalao - Catamarca - ARGENTINA',
            'Speluzzi - La Pampa - ARGENTINA',
            'Soldini - Santa Fe - ARGENTINA',
            'Sol de Julio - Santiago del Estero - ARGENTINA',
            'Simoca - Tucuman - ARGENTINA',
            'Siján - Catamarca - ARGENTINA',
            'Sierra Pailemán - Rio Negro - ARGENTINA',
            'Sierra Grande - Rio Negro - ARGENTINA',
            'Sierra de la Ventana - Buenos Aires - ARGENTINA',
            'Sierra Colorada - Rio Negro - ARGENTINA',
            'Serodino - Santa Fe - ARGENTINA',
            'Uquía - Jujuy - ARGENTINA',
            'Seclantás - Salta - ARGENTINA',
            'Sección Gap - Santa Cruz - ARGENTINA',
            'Schaqui - La Rioja - ARGENTINA',
            'Saujil - Catamarca - ARGENTINA',
            'Sauce Viejo - Santa Fe - ARGENTINA',
            'El Jagüel - Buenos Aires - ARGENTINA',
            'Alejandro Petión - Buenos Aires - ARGENTINA',
            'Open Door - Buenos Aires - ARGENTINA',
            'Olivos - Buenos Aires - ARGENTINA',
            'Oliden - Buenos Aires - ARGENTINA',
            'Nuestra Señora del Rosario de Caá Catí - Corrientes - ARGENTINA',
            'Nicanor Molinas - Santa Fe - ARGENTINA',
            'Munro - Buenos Aires - ARGENTINA',
            'Monte Grande - Buenos Aires - ARGENTINA',
            'Monte Chingolo - Buenos Aires - ARGENTINA',
            'Misión Tacaaglé - Formosa - ARGENTINA',
            'Médanos - Entre Rios - ARGENTINA',
            'Mburucuyá - Corrientes - ARGENTINA',
            'Máximo Paz - Buenos Aires - ARGENTINA',
            'Colonia Máximo Castro - Entre Rios - ARGENTINA',
            'Matheu - Buenos Aires - ARGENTINA',
            'Martínez - Buenos Aires - ARGENTINA',
            'Mariano Moreno - Buenos Aires - ARGENTINA',
            'Mariano I. Loza - Corrientes - ARGENTINA',
            'Mariano Acosta - Buenos Aires - ARGENTINA',
            'Margarita Belén - Chaco - ARGENTINA',
            'Mar del Sur - Buenos Aires - ARGENTINA',
            'Mar de Ajó - Buenos Aires - ARGENTINA',
            'Manuel J. Cobo - Buenos Aires - ARGENTINA',
            'Manuel B. Gonnet - Buenos Aires - ARGENTINA',
            'Malabrigo - Santa Fe - ARGENTINA',
            'Makallé - Chaco - ARGENTINA',
            'Villa Lynch - Buenos Aires - ARGENTINA',
            'Luis Guillón - Buenos Aires - ARGENTINA',
            'Lucas Monteverde - Buenos Aires - ARGENTINA',
            'Los Cardales - Buenos Aires - ARGENTINA',
            'Longchamps - Buenos Aires - ARGENTINA',
            'Lomas del Mirador - Buenos Aires - ARGENTINA',
            'Llavallol - Buenos Aires - ARGENTINA',
            'Lima - Buenos Aires - ARGENTINA',
            'Libertad - Buenos Aires - ARGENTINA',
            'Colonia Libertad - Corrientes - ARGENTINA',
            'La Vicuña - Chaco - ARGENTINA',
            'Lavalle - Corrientes - ARGENTINA',
            'Las Toscas - Santa Fe - ARGENTINA',
            'Las Toninas - Buenos Aires - ARGENTINA',
            'Las Palmas - Chaco - ARGENTINA',
            'La Sabana - Chaco - ARGENTINA',
            'Colonia La Marta - Entre Rios - ARGENTINA',
            'Lucila del Mar - Buenos Aires - ARGENTINA',
            'La Lucila - Buenos Aires - ARGENTINA',
            'Laguna Naick-Neck - Formosa - ARGENTINA',
            'Laguna Blanca - Chaco - ARGENTINA',
            'Laguna Blanca - Formosa - ARGENTINA',
            'Laferrere - Buenos Aires - ARGENTINA',
            'La Cruz - Corrientes - ARGENTINA',
            'La Clarita - Entre Rios - ARGENTINA',
            'Jubileo - Entre Rios - ARGENTINA',
            'Colonia Juan B. Cabral - Corrientes - ARGENTINA',
            'José Mármol - Buenos Aires - ARGENTINA',
            'Villa José León Suárez - Buenos Aires - ARGENTINA',
            'Jeppener - Buenos Aires - ARGENTINA',
            'Villa Flandria Sur - Buenos Aires - ARGENTINA',
            'Itatí - Corrientes - ARGENTINA',
            'Itá Ibaté - Corrientes - ARGENTINA',
            'Itacaruaré - Misiones - ARGENTINA',
            'Irazusta - Entre Rios - ARGENTINA',
            'Ingeniero Maschwitz - Buenos Aires - ARGENTINA',
            'Ingeniero Barbet - Chaco - ARGENTINA',
            'Horquilla - Chaco - ARGENTINA',
            'Hipólito Yrigoyen - Misiones - ARGENTINA',
            'Guaviraví - Corrientes - ARGENTINA',
            'Grand Bourg - Buenos Aires - ARGENTINA',
            'González Catán - Buenos Aires - ARGENTINA',
            'Gómez - Buenos Aires - ARGENTINA',
            'Gobernador Udaondo - Buenos Aires - ARGENTINA',
            'Glew - Buenos Aires - ARGENTINA',
            'Gilbert - Entre Rios - ARGENTINA',
            'Gerli - Buenos Aires - ARGENTINA',
            'General Almada - Entre Rios - ARGENTINA',
            'Garín - Buenos Aires - ARGENTINA',
            'Florida - Buenos Aires - ARGENTINA',
            'Felipe Yofré - Corrientes - ARGENTINA',
        ]
        self.listadecidadesBR = ['PARAGOMINAS - PA','REDENÇÃO - PA','MARABÁ - PA','ANANINDEUA - PA','SORRISO - MT','SINOP - MT','LUCAS DO RIO VERDE - MT','NOVA MUTUM - MT','SORRISO - MT','PARANATINGA - MT','TAPURAH - MT','ALTA FLORESTA - MT','MATUPÁ - MT','LUÍS EDUARDO MAGALHÃES - BA','BOM JESUS - PI','BARREIRAS - BA','CORRENTINA - BA','SÃO DESIDÉRIO - BA','FORMOSA DO RIO PRETO - BA','URUÇUÍ - PI','SÃO BORJA - RS','URUGUAIANA - RS','ALEGRETE - RS','SÃO LUIZ GONZAGA - RS','PELOTAS - RS','ITAQUI - RS','SANTA VITÓRIA DO PALMAR - RS','TANGARÁ DA SERRA - MT','CAMPO NOVO DO PARECIS - MT','SAPEZAL - MT','DIAMANTINO - MT','JUARA - MT','SÃO GABRIEL DO OESTE - MS','MARACAJU - MS','CAMPO GRANDE - MS','BARRA DO BUGRES - MT','NOVA MARINGÁ - MT','SIDROLÂNDIA - MS','PONTA PORÃ - MS','AMAMBAI - MS','ELDORADO - MS','BELA VISTA - MS','NOVA ANDRADINA - MS','NAVIRAÍ - MS','MARINGÁ - PR','PARANAVAÍ - PR','SÃO PEDRO DO IVAÍ - PR','RIBEIRÃO PRETO - SP','ARARAQUARA - SP','GUAÍRA - SP','BARRETOS - SP','FRANCA - SP','ORLÂNDIA - SP','ITUVERAVA - SP','MONTE ALTO - SP','BEBEDOURO - SP','ITÁPOLIS - SP','DOURADOS - MS','RIO BRILHANTE - MS','ARAÇATUBA - SP','ANDRADINA - SP','PRESIDENTE PRUDENTE - SP','PENÁPOLIS - SP','AURIFLAMA - SP','DRACENA - SP','ARAUCÁRIA - PR','SÃO MATEUS DO SUL - PR','LAPA - PR','GOIÂNIA - GO','ACREÚNA - GO','URUAÇU - GO','VIANÓPOLIS - GO','JUSSARA - GO','CAMBÉ - PR','CORNÉLIO PROCÓPIO - PR','IVAIPORÃ - PR','APUCARANA - PR','RONDONÓPOLIS - MT','PRIMAVERA DO LESTE - MT','CAMPO VERDE - MT','SONORA - MS','ALTO GARÇAS - MT','CHAPADÃO DO SUL - MS','CHAPADÃO DO CÉU - GO','TRÊS LAGOAS - MS','SÃO JOSÉ DO RIO PRETO - SP','CATANDUVA - SP','JALES - SP','MARÍLIA - SP','TUPÃ - SP','VOTUPORANGA - SP','PASSO FUNDO - RS','ESPUMOSO - RS','ERECHIM - RS','CARAZINHO - RS','TAPEJARA - RS','CASCA - RS','ARROIO DO TIGRE - RS','BALSAS - MA','ALTO PARNAÍBA - MA','IMPERATRIZ - MA','CAMPOS LINDOS - TO','CAMAQUÃ - RS','SÃO LOURENÇO DO SUL - RS','SERTÃO SANTANA - RS','LINHARES - ES','TEIXEIRA DE FREITAS - BA','VENDA NOVA DO IMIGRANTE - ES','EUNÁPOLIS - BA','CASCAVEL - PR','MEDIANEIRA - PR','PALOTINA - PR','ASSIS CHATEAUBRIAND - PR','UMUARAMA - PR','CAMPO MOURÃO - PR','GOIOERÊ - PR','UBIRATÃ - PR','TOLEDO - PR','CIANORTE - PR','MARECHAL CÂNDIDO RONDON - PR','MINEIROS - GO','ALTO TAQUARI - MT','CAIAPÔNIA - GO','PONTA GROSSA - PR','CASTRO - PR','IRATI - PR','ARAPOTI - PR','GUARAPUAVA - PR','PRUDENTÓPOLIS - PR','QUEDAS DO IGUAÇU - PR','BRASÍLIA - DF','CRISTALINA - GO','UNAÍ - MG','FORMOSA - GO','PARACATU - MG','BURITIS - MG','PADRE BERNARDO - GO','GURUPI - TO','GUARAÍ - TO','ARAGUAÍNA - TO','LAGOA DA CONFUSÃO - TO','PORTO NACIONAL - TO','PARAÍSO DO TOCANTINS - TO','PALMAS - TO','UBERLÂNDIA - MG','ARAGUARI - MG','PATROCÍNIO - MG','ITUMBIARA - GO','GOIATUBA - GO','CATALÃO - GO','UBERABA - MG','FRUTAL - MG','PATOS DE MINAS - MG','QUIRINÓPOLIS - GO','ITUIUTABA - MG','SÃO GOTARDO - MG','RIO VERDE - GO','JATAÍ - GO','MONTIVIDIU - GO','TURVO - SC','GRAVATAL - SC','TRÊS CORAÇÕES - MG','PASSOS - MG','LAVRAS - MG','POUSO ALEGRE - MG','ARCOS - MG','SÃO JOÃO DEL REI - MG','BOA ESPERANÇA - MG','CAMPOS NOVOS - SC','RIO DO SUL - SC','SÃO JOAQUIM - SC','FRAIBURGO - SC','VILHENA - RO','PONTES E LACERDA - MT','RIO BRANCO - AC','CÁCERES - MT','ROLIM DE MOURA - RO','ARIQUEMES - RO','BOA VISTA - RR','MACEIÓ - AL','NOSSA SENHORA DO SOCORRO - SE','PARIPIRANGA - BA','VACARIA - RS','CAXIAS DO SUL - RS','LAGOA VERMELHA - RS','ESTRELA - RS','SANANDUVA - RS','MONTENEGRO - RS','QUERÊNCIA - MT','CANARANA - MT','BARRA DO GARÇAS - MT','PORTO ALEGRE DO NORTE - MT','GAÚCHA DO NORTE - MT','HORIZONTINA - RS','TRÊS PASSOS - RS','SANTO ÂNGELO - RS','CRUZ ALTA - RS','IBIRUBÁ - RS','TUPANCIRETÃ - RS','IJUÍ - RS','SARANDI - RS','PALMEIRA DAS MISSÕES - RS','FREDERICO WESTPHALEN - RS','SANTA MARIA - RS','DOM PEDRITO - RS','SÃO GABRIEL - RS','JÚLIO DE CASTILHOS - RS','CACHOEIRA DO SUL - RS','ELDORADO DO SUL - RS','CAPIVARI DO SUL - RS','SANTA CRUZ DO SUL - RS','BAGÉ - RS','CHAPECÓ - SC','SÃO MIGUEL DO OESTE - SC','XANXERÊ - SC','CAMPO ERÊ - SC','ABELARDO LUZ - SC','CASA BRANCA - SP','JAÚ - SP','MOGI MIRIM - SP','LENÇÓIS PAULISTA - SP','ARARAS - SP','MOGI DAS CRUZES - SP','TAUBATÉ - SP','MAFRA - SC','CANOINHAS - SC','GUARAMIRIM - SC','PIRACICABA - SP','ITAPETININGA - SP','ITAPEVA - SP','INDAIATUBA - SP','BRAGANÇA PAULISTA - SP','PIEDADE - SP','REGISTRO - SP','CONTAGEM - MG','MONTES CLAROS - MG','TANGUÁ - RJ','JUIZ DE FORA - MG','GOVERNADOR VALADARES - MG','JANAÚBA - MG','POMPÉU - MG','ASSIS - SP','OURINHOS - SP','AVARÉ - SP','TAQUARITUBA - SP','PARANAPANEMA - SP','RECIFE - PE','BAYEUX - PB','FORTALEZA - CE','PETROLINA - PE','SALVADOR - BA','PATO BRANCO - PR','REALEZA - PR','PALMAS - PR','MANGUEIRINHA - PR','São Paulo, SP','Rio de Janeiro, RJ','Brasília, DF','Salvador, BA','Fortaleza, CE','Belo Horizonte, MG','Manaus, AM','Curitiba, PR','Recife, PE','Goiânia, GO','Belém, PA','Porto Alegre, RS','Guarulhos, SP','Campinas, SP','São Luís, MA','São Gonçalo, RJ','Maceió, AL','Duque de Caxias, RJ','Campo Grande, MS','Natal, RN','Teresina, PI','São Bernardo do Campo, SP','Nova Iguaçu, RJ','João Pessoa, PB','São José dos Campos, SP','Santo André, SP','Ribeirão Preto, SP','Jaboatão dos Guararapes, PE','Osasco, SP','Uberlândia, MG','Sorocaba, SP','Contagem, MG','Aracaju, SE','Feira de Santana, BA','Cuiabá, MT','Joinville, SC','Aparecida de Goiânia, GO','Londrina, PR','Juiz de Fora, MG','Ananindeua, PA','Porto Velho, RO','Serra, ES','Niterói, RJ','Belford Roxo, RJ','Caxias do Sul, RS','Campos dos Goytacazes, RJ','Macapá, AP','Florianópolis, SC','Vila Velha, ES','Mauá, SP','São João de Meriti, RJ','São José do Rio Preto, SP','Mogi das Cruzes, SP','Betim, MG','Santos, SP','Diadema, SP','Maringá, PR','Jundiaí, SP','Campina Grande, PB','Montes Claros, MG','Rio Branco, AC','Piracicaba, SP','Carapicuíba, SP','Boa Vista, RR','Olinda, PE','Anápolis, GO','Cariacica, ES','Bauru, SP','Itaquaquecetuba, SP','São Vicente, SP','Vitória, ES','Caucaia, CE','Caruaru, PE','Blumenau, SC','Franca, SP','Ponta Grossa, PR','Petrolina, PE','Canoas, RS','Pelotas, RS','Vitória da Conquista, BA','Ribeirão das Neves, MG','Uberaba, MG','Paulista, PE','Cascavel, PR','Praia Grande, SP','São José dos Pinhais, PR','Guarujá, SP','Taubaté, SP','Petrópolis, RJ','Limeira, SP','Santarém, PA','Camaçari, BA','Palmas, TO','Suzano, SP','Mossoró, RN','Taboão da Serra, SP','Várzea Grande, MT','Sumaré, SP','Santa Maria, RS','Gravataí, RS','Governador Valadares, MG','Marabá, PA','Juazeiro do Norte, CE','Barueri, SP','Embu das Artes, SP','Volta Redonda, RJ','Ipatinga, MG','Parnamirim, RN','Imperatriz, MA','Foz do Iguaçu, PR','Macaé, RJ','Viamão, RS','São Carlos, SP','Indaiatuba, SP','Cotia, SP','Novo Hamburgo, RS','São José, SC','Magé, RJ','Colombo, PR','Itaboraí, RJ','Sete Lagoas, MG','Americana, SP','Marília, SP','Divinópolis, MG','Itapevi, SP','São Leopoldo, RS','Araraquara, SP','Rio Verde, GO','Jacareí, SP','Rondonópolis, MT','Arapiraca, AL','Hortolândia, SP','Presidente Prudente, SP','Maracanaú, CE','Dourados, MS','Chapecó, SC','Cabo Frio, RJ','Itajaí, SC','Santa Luzia, MG','Juazeiro, BA','Criciúma, SC','Itabuna, BA','Águas Lindas de Goiás, GO','Rio Grande, RS','Alvorada, RS','Cachoeiro de Itapemirim, ES','Sobral, CE','Luziânia, GO','Parauapebas, PA','Cabo de Santo Agostinho, PE','Rio Claro, SP','Angra dos Reis, RJ','Passo Fundo, RS','Castanhal, PA','Lauro de Freitas, BA','Araçatuba, SP','Ferraz de Vasconcelos, SP','Santa Bárbara d Oeste, SP','Nova Friburgo, RJ','Barra Mansa, RJ','Nossa Senhora do Socorro, SE','Teresópolis, RJ','Guarapuava, PR','Araguaína, TO','Ibirité, MG','Jaraguá do Sul, SC','São José de Ribamar, MA','Mesquita, RJ','Francisco Morato, SP','Itapecerica da Serra, SP','Itu, SP','Linhares, ES','Palhoça, SC','Timon, MA','Bragança Paulista, SP','Valparaíso de Goiás, GO','Pindamonhangaba, SP','Poços de Caldas, MG','Caxias, MA','Itapetininga, SP','Nilópolis, RJ','Ilhéus, BA','Maricá, RJ','São Caetano do Sul, SP','Teixeira de Freitas, BA','Camaragibe, PE','Abaetetuba, PA','Lages, SC','Jequié, BA','Barreiras, BA','Paranaguá, PR','Franco da Rocha, SP','Parnaíba, PI','Patos de Minas, MG','Mogi Guaçu, SP','Alagoinhas, BA','Pouso Alegre, MG','Rio das Ostras, RJ','Queimados, RJ','Jaú, SP','Porto Seguro, BA','Botucatu, SP','Araucária, PR','Sinop, MT','Atibaia, SP','Balneário Camboriú, SC','Sapucaia do Sul, RS','Toledo, PR','Teófilo Otoni, MG','Garanhuns, PE','Santana de Parnaíba, SP','Vitória de Santo Antão, PE','Cametá, PA','Barbacena, MG','Santa Rita, PB','Sabará, MG','Varginha, MG','Apucarana, PR','Brusque, SC','Simões Filho, BA','Araras, SP','Itaguaí, RJ','Araruama, RJ','Pinhais, PR','Crato, CE','Campo Largo, PR','Marituba, PA','Resende, RJ','Cubatão, SP','São Mateus, ES','Santa Cruz do Sul, RS','Cachoeirinha, RS','Itapipoca, CE','Valinhos, SP','Maranguape, CE','Ji-Paraná, RO','Conselheiro Lafaiete, MG','São Félix do Xingu, PA','Bragança, PA','Vespasiano, MG','Trindade, GO','Uruguaiana, RS','Sertãozinho, SP','Jandira, SP','Guarapari, ES','Barcarena, PA','Birigui, SP','Ribeirão Pires, SP','Arapongas, PR','Codó, MA','Colatina, ES','Votorantim, SP','Paço do Lumiar, MA','Barretos, SP','Catanduva, SP','Várzea Paulista, SP','Guaratinguetá, SP','Tatuí, SP','Formosa, GO','Caraguatatuba, SP','Três Lagoas, MS','Santana, AP','Bagé, RS','Itatiba, SP','Bento Gonçalves, RS','Itabira, MG','Salto, SP','Almirante Tamandaré, PR','Paulo Afonso, BA','Poá, SP','Araguari, MG','Igarassu, PE','Novo Gama, GO','Ubá, MG','Senador Canedo, GO','Passos, MG','Altamira, PA','Parintins, AM','Tucuruí, PA','Ourinhos, SP','Eunápolis, BA','São Lourenço da Mata, PE','Paragominas, PA','Piraquara, PR','Açailândia, MA','Umuarama, PR','Corumbá, MS','Coronel Fabriciano, MG','Paulínia, SP','Catalão, GO','Muriaé, MG','Santa Cruz do Capibaribe, PE','Ariquemes, RO','Patos, PB','Cambé, PR','Tailândia, PA','Araxá, MG','Erechim, RS','Tubarão, SC','Bacabal, MA','Japeri, RJ','Itumbiara, GO','Ituiutaba, MG','São Pedro da Aldeia, RJ','Lagarto, SE','Assis, SP','Lavras, MG','Tangará da Serra, MT','Leme, SP','Itaperuna, RJ','Breves, PA','Nova Serrana, MG','Iguatu, CE','São Gonçalo do Amarante, RN','Itanhaém, SP','Santo Antônio de Jesus, BA','Caieiras, SP','Itacoatiara, AM','Itaituba, PA','Aracruz, ES','Jataí, GO','Barra do Piraí, RJ','Fazenda Rio Grande, PR','Mairiporã, SP','Abreu e Lima, PE','Vilhena, RO','Guaíba, RS','Manacapuru, AM','Bayeux, PB','Itajubá, MG','Sarandi, PR','Valença, BA','Ipojuca, PE','Itabaiana, SE','Nova Lima, MG','Balsas, MA','Campo Mourão, PR','Votuporanga, SP','Cáceres, MT','Itapeva, SP','Caçapava, SP','Pará de Minas, MG','Itaúna, MG','Mogi Mirim, SP','Paracatu, MG','Ponta Porã, MS','Caratinga, MG','São João da Boa Vista, SP','Caldas Novas, GO','Francisco Beltrão, PR','São Roque, SP','Ubatuba, SP','Patrocínio, MG','Avaré, SP','Sorriso, MT','Manhuaçu, MG','São João del Rei, MG','São Cristóvão, SE','Planaltina, GO','Timóteo, MG','Arujá, SP','Saquarema, RJ','Santa Inês, MA','São Sebastião, SP','Lorena, SP','Cruzeiro do Sul, AC','Paranavaí, PR','Barra do Corda, MA','Quixadá, CE','Luís Eduardo Magalhães, BA','Candeias, BA','Gurupi, TO','Serra Talhada, PE','Cacoal, RO','Coari, AM','Redenção, PA','Campo Limpo Paulista, SP','São Bento do Sul, SC','Guanambi, BA','Araripina, PE','Unaí, MG','Gravatá, PE','Lajeado, RS','Carpina, PE','Ijuí, RS','Pacatuba, CE','Pinheiro, MA','Esteio, RS','Matão, SP','Camboriú, SC','Pato Branco, PR','Cianorte, PR','Seropédica, RJ','Cruzeiro, SP','Cachoeira do Sul, RS','Moju, PA','Três Rios, RJ','Sapiranga, RS','Navegantes, SC','Dias d Ávila, BA','Quixeramobim, CE','Serrinha, BA','Macaíba, RN','Jacobina, BA','Aquiraz, CE','Curvelo, MG','Alfenas, MG','João Monlevade, MG','Goiana, PE','Chapadinha, MA','Três Corações, MG','Senhor do Bonfim, BA','Telêmaco Borba, PR','Ibiúna, SP','Viçosa, MG','Vinhedo, SP','Caçador, SC','Viana, ES','Picos, PI','Russas, CE','Lins, SP','Santo Ângelo, RS','Bebedouro, SP','Jaboticabal, SP','SantAna do Livramento, RS','Canindé, CE','Cajamar, SP','Valença, RJ','Belo Jardim, PE','Pirassununga, SP','Itapetinga, BA','Tianguá, CE','Novo Repartimento, PA','Cataguases, MG','Rio Largo, AL','Crateús, CE','Itapira, SP','Santo Antônio do Descoberto, GO','Concórdia, SC','Aracati, CE','Arcoverde, PE','Ouro Preto, MG','Alegrete, RS','Ceará-Mirim, RN','Santa Rosa, RS','Palmeira dos Índios, AL','Oriximiná, PA','Irecê, BA','Santana do Araguaia, PA','Santa Luzia, MA','Buriticupu, MA','Farroupilha, RS','Cosmópolis, SP','Pacajus, CE','Amparo, SP','Casa Nova, BA','Cascavel, CE','Janaúba, MG','Venâncio Aires, RS','Castro, PR','Cidade Ocidental, GO','Campo Formoso, BA','Rio do Sul, SC','São Sebastião do Paraíso, MG','Santa Izabel do Pará, PA','Esmeraldas, MG','Goianésia, GO','Gaspar, SC','Grajaú, MA','Ouricuri, PE','Sousa, PB','Indaial, SC','Embu-Guaçu, SP','Estância, SE','Bom Jesus da Lapa, BA','Fernandópolis, SP','Capanema, PA','Mococa, SP','Escada, PE','Biguaçu, SC','Lençóis Paulista, SP','Peruíbe, SP','Araranguá, SC','Itapecuru Mirim, MA','Icó, CE','Caicó, RN','Januária, MG','Cabedelo, PB','Formiga, MG','Pesqueira, PE','Horizonte, CE','Brumado, BA','Mineiros, GO','Campo Bom, RS','Conceição do Coité, BA','Rolândia, PR','Camaquã, RS','Vacaria, RS','Breu Branco, PA','Tabatinga, AM','União dos Palmares, AL','Lucas do Rio Verde, MT','Tupã, SP','Itapema, SC','Coroatá, MA','Montenegro, RS','Surubim, PE','Lagoa Santa, MG','Itaberaba, BA','Itamaraju, BA','Pedro Leopoldo, MG','Ipixuna do Pará, PA','Maués, AM','Piripiri, PI','Penedo, AL','Camocim, CE','Tomé-Açu, PA','Penápolis, SP','Palmares, PE','Bertioga, SP','Cruz das Almas, BA','Moreno, PE','Benevides, PA','Igarapé-Miri, PA','Acaraú, CE','Barreirinhas, MA','Batatais, SP','Carazinho, RS','São Gabriel, RS','Portel, PA','Primavera do Leste, MT','Cajazeiras, PB','Morada Nova, CE','Viseu, PA','Itupeva, SP','São Miguel dos Campos, AL','Barra do Garças, MT','Boituva, SP','Salgueiro, PE','Viçosa do Ceará, CE','Bezerros, PE','Barbalha, CE','Irati, PR','Mariana, MG','Euclides da Cunha, BA','Guapimirim, RJ','Cruz Alta, RS','São Borja, RS','Rio Bonito, RJ','Nova Odessa, SP','Santo Amaro, BA','Ibitinga, SP','Floriano, PI','Tefé, AM','Mirassol, SP','Monte Mor, SP','Ponte Nova, MG','Dom Eliseu, PA','Ipirá, BA','Limoeiro do Norte, CE','São Bento do Una, PE','Frutal, MG','Ulianópolis, PA','Jacundá, PA','Cristalina, GO','São Miguel do Guamá, PA','Cachoeiras de Macacu, RJ','Tutóia, MA','Tauá, CE','Guarabira, PB','Buíque, PE','Parobé, RS','Monte Alegre, PA','Açu, RN','Juruti, PA','Sidrolândia, MS','União da Vitória, PR','Jaguariúna, SP','Taquara, RS','Santa Isabel, SP','Taquaritinga, SP','Andradina, SP','Campo Alegre, AL','Coruripe, AL','Alenquer, PA','Três Pontas, MG','Mongaguá, SP','Vargem Grande, MA','Paudalho, PE','Pirapora, MG','Içara, SC','São Francisco, MG','Registro, SP','Mafra, SC','Limoeiro, PE','Porto Ferreira, SP','Canguçu, RS','Trairi, CE','Capivari, SP','Manicoré, AM','Acará, PA','Piedade, SP','Humaitá, AM','Rolim de Moura, RO','São José do Rio Pardo, SP','Naviraí, MS','Olímpia, SP','Congonhas, MG','Granja, CE','Catu, BA','Ibiporã, PR','Boa Viagem, CE','Jaguaquara, BA','Artur Nogueira, SP','Canoinhas, SC','Araci, BA','Nova Andradina, MS','Capitão Poço, PA','Acopiara, CE','Campo Belo, MG','Ribeira do Pombal, BA','Vigia, PA','Eusébio, CE','Barra, BA','Beberibe, CE','Itupiranga, PA','Porto Feliz, SP','Videira, SC','Capão da Canoa, RS','Timbaúba, PE','Porto Nacional, TO','Marechal Cândido Rondon, PR','Inhumas, GO','Santo Estêvão, BA','São Francisco do Sul, SC','Itapajé, CE','Sapé, PB','Vargem Grande Paulista, SP','Leopoldina, MG','Viana, MA','Rondon do Pará, PA','Paracambi, RJ','Prudentópolis, PR','Tobias Barreto, SE','Lagoa da Prata, MG','Óbidos, PA','Campos do Jordão, SP','Delmiro Gouveia, AL','Guaxupé, MG','Marechal Deodoro, AL','São Joaquim da Barra, SP','Itabirito, MG','Alta Floresta, MT','Jaru, RO','Tramandaí, RS','Zé Doca, MA','Paraíso do Tocantins, TO','Palmas, PR','Xanxerê, SC','Caetité, BA','Rio Grande da Serra, SP','Brejo da Madre de Deus, PE','Tucano, BA','Bom Despacho, MG','Jaraguá, GO','Rurópolis, PA','Itararé, SP','Monte Alto, SP','Laranjal do Jari, AP','Lago da Pedra, MA','Nova Venécia, ES','Quirinópolis, GO','Estância Velha, RS','Bocaiúva, MG','Pontal, SP','Macaúbas, BA','Cabreúva, SP','Brejo Santo, CE','Coelho Neto, MA','Santiago, RS','Monte Santo, BA','Jales, SP','Cerquilho, SP','Louveira, SP','Bom Conselho, PE','São Gonçalo do Amarante, CE','Iranduba, AM','Lapa, PR','Mauriti, CE','Pedreira, SP','São Benedito, CE','Aquidauana, MS','Conceição do Araguaia, PA','Cornélio Procópio, PR','Monte Carmelo, MG','Presidente Dutra, MA','Diamantina, MG','Pacajá, PA','Santa Cruz do Rio Pardo, SP','Santana do Ipanema, AL','João Pinheiro, MG','Baião, PA','Ribeirão, PE','Atalaia, AL','Tremembé, SP','Mairinque, SP','Capão Bonito, SP','Maracaju, MS','Barras, PI','Poções, BA','Campo Maior, PI','Dracena, SP','Pederneiras, SP','Mata de São João, BA','Santos Dumont, MG','Xique-Xique, BA','Araioses, MA','Niquelândia, GO','São Mateus do Sul, PR','Medianeira, PR','Guajará-Mirim, RO','Morrinhos, GO','Lábrea, AM','Augusto Corrêa, PA','Osório, RS','Santo Antônio da Platina, PR','Ipiaú, BA','Sirinhaém, PE','São Lourenço, MG','Sena Madureira, AC','Laguna, SC','Livramento de Nossa Senhora, BA','Paraguaçu Paulista, SP','São Gabriel da Cachoeira, AM','Uruará, PA','Pontes e Lacerda, MT','Salto de Pirapora, SP','Porangatu, GO','Nova Mutum, MT','Toritama, PE','São Bento, MA','Serrana, SP','Canela, RS','Mamanguape, PB','Imbituba, SC','Guaramirim, SC','Currais Novos, RN','Xinguara, PA','Caeté, MG','Maragogipe, BA','Barra de São Francisco, ES','União, PI','Mangaratiba, RJ','Garça, SP','Jardinópolis, SP','Espírito Santo do Pinhal, SP','São Sebastião do Passé, BA','Goianira, GO','Paraíba do Sul, RJ','Timbó, SC','Presidente Epitácio, SP','Casimiro de Abreu, RJ','Teotônio Vilela, AL','Marau, RS','Seabra, BA','Campo Verde, MT','Orlândia, SP','Queimadas, PB','São José de Mipibu, RN','Mombaça, CE','Santa Quitéria, CE','Panambi, RS','São Lourenço do Sul, RS','Amontada, CE','Águas Belas, PE','Nova Viçosa, BA','Campina Grande do Sul, PR','Santa Rita do Sapucaí, MG','Pedra Branca, CE','Vera Cruz, BA','Paraty, RJ','Itápolis, SP','Igarapé, MG','Benjamin Constant, AM','Itaberaí, GO','Santo Antônio da Patrulha, RS','Catende, PE','Vargem Grande do Sul, SP','Rosário, MA','Barreiros, PE','Tarauacá, AC','Visconde do Rio Branco, MG','Santo Antônio de Pádua, RJ','Rio Negrinho, SC','São Francisco de Itabapoana, RJ','Paranaíba, MS','Machado, MG','Santa Helena, MA','Tietê, SP','Ipu, CE','Estreito, MA','Santa Maria da Boa Vista, PE','Itabaianinha, SE','Almenara, MG','Tuntum, MA','Itarema, CE','Ituverava, SP','Entre Rios, BA','Mucuri, BA','Oliveira, MG','Bom Jardim, MA','São Mateus do Maranhão, MA','Salinas, MG','Amarante do Maranhão, MA','Eldorado do Sul, RS','Paiçandu, PR','Colinas, MA','Borba, AM','Porto de Moz, PA','Andradas, MG','Novo Horizonte, SP','Remanso, BA','Socorro, SP','Juína, MT','São Manuel, SP','Girau do Ponciano, AL','Guaíra, SP','Charqueadas, RS','Nanuque, MG','Rio Real, BA','Várzea Alegre, CE','Sento Sé, BA','Salinópolis, PA','Guaraciaba do Norte, CE','Dois Vizinhos, PR','Armação dos Búzios, RJ','Uruaçu, GO','Altos, PI','Américo Brasiliense, SP','Simão Dias, SE','São Miguel do Oeste, SC','Goianésia do Pará, PA','Jeremoabo, BA','Promissão, SP','Santa Maria de Jetibá, ES','Muaná, PA','Lajedo, PE','Boa Esperança, MG','Guariba, SP','Brumadinho, MG','Arcos, MG','Curuçá, PA','Machadinho D Oeste, RO','Inhambupe, BA','Santa Maria da Vitória, BA','São Francisco do Conde, BA','Curitibanos, SC','Esperantina, PI','Pitangueiras, SP','Santa Cruz, RN','Buritis, RO','Tucumã, PA','Autazes, AM','Pojuca, BA','Presidente Venceslau, SP','Ouro Branco, MG','Várzea da Palma, MG','Rosário do Sul, RS','Amambai, MS','Jacarezinho, PR','São Paulo de Olivença, AM','Iturama, MG','Pedreiras, MA','Afuá, PA','José de Freitas, PI','Bom Jardim, PE','Jaíba, MG','Igarapé-Açu, PA','Pedro II, PI','Massapê, CE','Torres, RS','São Fidélis, RJ','Santa Helena de Goiás, GO','Colniza, MT','Marataízes, ES','Penalva, MA','Dom Pedrito, RS','Tijucas, SC','Aliança, PE','Rio Pardo, RS','Ipueiras, CE','Bodocó, PE','Bonito, PE','Araquari, SC','Itaitinga, CE','São Gabriel da Palha, ES','Porteirinha, MG','Careiro, AM','Santa Rita, MA','Matozinhos, MG','Capelinha, MG','Pentecoste, CE','Itaqui, RS','São Gonçalo dos Campos, BA','Castelo, ES','Rio Brilhante, MS','São João Batista, SC','Nova Olinda do Norte, AM','Santaluz, BA','Nova Cruz, RN','Afogados da Ingazeira, PE','São Caitano, PE','Amargosa, BA','Esplanada, BA','Agudos, SP','Iperó, SP','Custódia, PE','Bom Jesus do Itabapoana, RJ','Canaã dos Carajás, PA','Portão, RS','Guaratuba, PR','Oeiras, PI','José Bonifácio, SP','Nossa Senhora da Glória, SE','Posse, GO','Igrejinha, RS','Vassouras, RJ','Água Preta, PE','Araçuaí, MG','Pimenta Bueno, RO','Petrolândia, PE','Itambé, PE','Fraiburgo, SC','Brejo, MA','Aguaí, SP','Presidente Figueiredo, AM','Campos Novos, SC','Gramado, RS','Extrema, MG','Aparecida, SP','Barra Bonita, SP','São João da Barra, RJ','Itiúba, BA','Ouro Preto do Oeste, RO','Sertânia, PE','Apodi, RN','Guarantã do Norte, MT','Araguatins, TO','Baturité, CE','São Pedro, SP','Turiaçu, MA','Itapicuru, BA','Marialva, PR','São Gotardo, MG','Colinas do Tocantins, TO','Riacho de Santana, BA','Morro do Chapéu, BA','Porto União, SC','Missão Velha, CE','Além Paraíba, MG','Campo Novo do Parecis, MT','Camamu, BA','Cravinhos, SP','Eirunepé, AM','Bariri, SP','Rio das Pedras, SP','Pilar, AL','Ibaté, SP','Paracuru, CE','Garibaldi, RS','Adamantina, SP','Pilão Arcado, BA','Peixoto de Azevedo, MT','Juara, MT','Ilhabela, SP','Barra do Bugres, MT','João Câmara, RN','Parnarama, MA','Jaguariaíva, PR','Cansanção, BA','Ubajara, CE','Feijó, AC','Poço Redondo, SE','Itamarandiba, MG','Matinhos, PR','São Raimundo Nonato, PI','Curaçá, BA','Piumhi, MG','Jaguaribe, CE','Santana do Paraíso, MG','São Luís do Quitunde, AL','Curralinho, PA','Mandaguari, PR','São Domingos do Maranhão, MA','Santa Cruz das Palmeiras, SP','Itaporanga d Ajuda, SE','Itapemirim, ES','Guanhães, MG','Tanguá, RJ','Boca do Acre, AM','Canguaretama, RN','Cabrobó, PE','Capela, SE','Rio Negro, PR','São Sebastião, AL','Araçoiaba da Serra, SP','Taiobeiras, MG','Estrela, RS','Almeirim, PA','Quedas do Iguaçu, PR','Goiatuba, GO','São Bento, PB','Bom Jesus das Selvas, MA','São José do Belmonte, PE','São José do Egito, PE','Cachoeira do Piriá, PA','Palmeira, PR','Domingos Martins, ES','Padre Bernardo, GO','João Alfredo, PE','São Luís de Montes Belos, GO','Eldorado do Carajás, PA','Matões, MA','Miguel Alves, PI','São Desidério, BA','Descalvado, SP','Jaguaruana, CE','Ouro Fino, MG','Caçapava do Sul, RS','Jaguarari, BA','Coxim, MS','Cachoeira, BA','São Luiz Gonzaga, RS','Braço do Norte, SC','Pomerode, SC','Colíder, MT','Riachão do Jacuípe, BA','Monção, MA','Gurupá, PA','Assis Chateaubriand, PR','Rio Preto da Eva, AM','Cachoeira Paulista, SP','Concórdia do Pará, PA','Palmeira das Missões, RS','Touros, RN','Teutônia, RS','Monteiro, PB','Conceição do Jacuípe, BA','Urbano Santos, MA','Guaíra, PR','Esperança, PB','Carangola, MG','Morro Agudo, SP','Pindaré-Mirim, MA','Guararapes, SP','São Miguel Arcanjo, SP','Osvaldo Cruz, SP','Floresta, PE','Poconé, MT','Ourilândia do Norte, PA','Barrinha, SP','Pombal, PB','Vitória do Mearim, MA','Sarzedo, MG','Paraipaba, CE','Maragogi, AL','Arame, MA','Cururupu, MA','Dois Irmãos, RS','Vicência, PE','Biritiba Mirim, SP','Bela Cruz, CE','Imbituva, PR','Irituia, PA','Penha, SC','Cícero Dantas, BA','Oeiras do Pará, PA','Barão de Cocais, MG','Nazaré da Mata, PE','Santana do Acaraú, CE','Gandu, BA','Rio Branco do Sul, PR','Pinhão, PR','Espigão D Oeste, RO','Três Marias, MG','Brasília de Minas, MG','Nova Russas, CE','Santa Fé do Sul, SP','São José da Tapera, AL','Correntina, BA','Manaquiri, AM','Laranjeiras do Sul, PR','Barreirinha, AM','Paratinga, BA','São Domingos do Capim, PA','Camacan, BA','Ivaiporã, PR','Alto Alegre do Pindaré, MA','Palotina, PR','Exu, PE','Macau, RN','Pompéu, MG','Itatiaia, RJ','Espinosa, MG','Barra do Choça, BA','Medicilândia, PA','São Joaquim de Bicas, MG','Iporá, GO','Vitorino Freire, MA','Parambu, CE','Lavras da Mangabeira, CE','Minas Novas, MG','Santo Antônio do Tauá, PA','Serra do Ramalho, BA','Pires do Rio, GO','Juquitiba, SP','Bandeirantes, PR','Candelária, RS','Ibaiti, PR','Aurora do Pará, PA','Novo Cruzeiro, MG','Santa Bárbara, MG','Frederico Westphalen, RS','Cândido Mota, SP','Mocajuba, PA','Canavieiras, BA','Mateus Leme, MG','Ponta de Pedras, PA','Conceição da Barra, ES','Gameleira, PE','Soledade, RS','Baixo Guandu, ES','Placas, PA','Tracuateua, PA','Confresa, MT','Rio Pardo de Minas, MG','Guaçuí, ES','Iguape, SP','Ipubi, PE','Ruy Barbosa, BA','Raposa, MA','Flores da Cunha, RS','Tabuleiro do Norte, CE','Bagre, PA','Capim Grosso, BA','Glória do Goitá, PE','Afonso Cláudio, ES','Itabela, BA','Nova Mamoré, RO','Catolé do Rocha, PB','Trindade, PE','Jaguaré, ES','Igarapava, SP','Barra dos Coqueiros, SE','Pau dos Ferros, RN','Casa Branca, SP','Sombrio, SC','Arraial do Cabo, RJ','Carmo do Paranaíba, MG','Luís Correia, PI','Pitanga, PR','Careiro da Várzea, AM','Caarapó, MS','Rorainópolis, RR','Joaçaba, SC','Alegre, ES','Mãe do Rio, PA','Sooretama, ES','Jarinu, SP','Bela Vista de Goiás, GO','Canindé de São Francisco, SE','Prainha, PA','Nerópolis, GO','Arari, MA','Carlos Barbosa, RS','Laranjeiras, SE','Piraju, SP','Guararema, SP','Rancharia, SP','Ipixuna, AM','Santa Vitória do Palmar, RS','Propriá, SE','Mirandópolis, SP','Cambuí, MG','Triunfo, RS','Maracanã, PA','Muritiba, BA','Campo Magro, PR','Nova Santa Rita, RS','Anajás, PA','Piraí, RJ','Anchieta, ES','Ibimirim, PE','Serra Negra, SP','Pilar do Sul, SP','Barra Velha, SC','Iúna, ES','Bujaru, PA','Timbiras, MA','Minaçu, GO','Redenção, CE','Irará, BA','Carinhanha, BA','Paripiranga, BA','Limoeiro do Ajuru, PA','Passira, PE','Goioerê, PR','Palmeiras de Goiás, GO','Campo Alegre de Lourdes, BA','Piracuruca, PI','Taquaritinga do Norte, PE','Campos Gerais, MG','Caetés, PE','Humberto de Campos, MA','Xaxim, SC','Buriti, MA','Codajás, AM','Limoeiro de Anadia, AL','Itaperuçu, PR','Cláudio, MG','Novo Oriente, CE','Ituberá, BA','Porto da Folha, SE','Extremoz, RN','Cajati, SP','Tabira, PE','Nazaré, BA','Laranjal Paulista, SP','São Bernardo, MA','Alagoa Grande, PB','Valente, BA','Pedras de Fogo, PB','Miranda do Norte, MA','Baraúna, RN','Santa Rita de Cássia, BA','Marapanim, PA','Iguaba Grande, RJ','Itacaré, BA','Carauari, AM','Santo Antônio do Monte, MG','Murici, AL','Olindina, BA','Três Coroas, RS','Prado, BA','Arapoti, PR','Elói Mendes, MG','Buritizeiro, MG','Conchal, SP','Miranda, MS','Pitangui, MG','Coromandel, MG','Nova Esperança, PR','Conceição das Alagoas, MG','Anapu, PA','Prata, MG','Lagoa Vermelha, RS','Cocal, PI','Santa Cruz Cabrália, BA','Jaciara, MT','Areia Branca, RN','Paty do Alferes, RJ','Mirassol d Oeste, MT','Presidente Tancredo Neves, BA','Traipu, AL','Melgaço, PA','Alexânia, GO','Mantena, MG','Nísia Floresta, RN','Quijingue, BA','São José do Norte, RS','Santa Rita do Passa Quatro, SP','Pirapozinho, SP','Milagres, CE','Lagoa Seca, PB','Barcelos, AM','São Miguel do Iguaçu, PR','Bom Jardim, RJ','Água Azul do Norte, PA','Campos Sales, CE','Marco, CE','Dois Córregos, SP','Tupanatinga, PE','Piracaia, SP','Pontal do Paraná, PR','Boca da Mata, AL','Oiapoque, AP','Nova Prata, RS','Lapão, BA','Jardim, CE','Miracema, RJ','Porto Calvo, AL','Itaí, SP','Icatu, MA','Pombos, PE','Alto Alegre do Maranhão, MA','Pinheiros, ES','Ubatã, BA','Ipameri, GO','Mutum, MG','Caririaçu, CE','São Joaquim, SC','Nova Soure, BA','Juatuba, MG','Ibotirama, BA','Iguaí, BA','Santa Gertrudes, SP','Mandirituba, PR','Vera Cruz, RS','Taquari, RS','Batalha, PI','Boquim, SE','Anajatuba, MA','Forquilhinha, SC','Mundo Novo, BA','São Gabriel do Oeste, MS','Nepomuceno, MG','Reserva, PR','Belo Oriente, MG','Candeias do Jamari, RO','Ilha Solteira, SP','Jaguarão, RS','Itapissuma, PE','Corrente, PI','São Sebastião da Boa Vista, PA','Nossa Senhora das Dores, SE','Santana, BA','Coração de Jesus, MG','Santa Rosa de Viterbo, SP','Aldeias Altas, MA','Santa Helena, PR','Valparaíso, SP','Panelas, PE','Aracoiaba, CE','Sanharó, PE','Martinópolis, SP','Condado, PE','Solânea, PB','São João Nepomuceno, MG','Itaíba, PE','Goianinha, RN','Brasiléia, AC','Francisco Sá, MG','Planalto, BA','Castro Alves, BA','Ilha de Itamaracá, PE','Tamboril, CE','Veranópolis, RS','Sacramento, MG','Pedro Canário, ES','Independência, CE','Canarana, BA','Cajuru, SP','Mimoso do Sul, ES','Astorga, PR','Jardim, MS','Ibatiba, ES','Garrafão do Norte, PA','Guaiúba, CE','Quipapá, PE','Vila Rica, MT','Miguel Calmon, BA','Itinga do Maranhão, MA','Jacutinga, MG','Tanabi, SP','São João dos Patos, MA','Guaraí, TO','Sapezal, MT','Encruzilhada do Sul, RS','Conde, BA','Itapuranga, GO','Tacaratu, PE','Novo Progresso, PA','Maravilha, SC','Aparecida do Taboado, MS','Viçosa, AL','Guaporé, RS','Água Boa, MT','Ocara, CE','São Sebastião do Caí, RS','Pereira Barreto, SP','Novo Aripuanã, AM','Santa Quitéria do Maranhão, MA','Igaci, AL','Turilândia, MA','Lagoa Grande, PE','Formosa do Rio Preto, BA','Governador Nunes Freire, MA','São Domingos do Araguaia, PA','Cedro, CE','Miguel Pereira, RJ','Carandaí, MG','Senador Pompeu, CE','Pirajuí, SP','Luzilândia, PI','Piraí do Sul, PR','São Gonçalo do Sapucaí, MG','Bom Jesus dos Perdões, SP','Queimadas, BA','Jequitinhonha, MG','Macaparana, PE','Soure, PA','Cambará, PR','Capão do Leão, RS','Tupaciguara, MG','Umbaúba, SE','Venda Nova do Imigrante, ES','Santa Luzia do Paruá, MA','Angatuba, SP','Chapadão do Sul, MS','Mata Grande, AL','Iraquara, BA','Bom Jesus de Goiás, GO','Cujubim, RO','Ibiá, MG','Cândido Sales, BA','João Dourado, BA','Bom Jesus, PI','Aimorés, MG','São João da Ponte, MG','Santa Isabel do Rio Negro, AM','Pinheiral, RJ','Pedro do Rosário, MA','Anastácio, MS','Amélia Rodrigues, BA','Monte Aprazível, SP','Ituporanga, SC','Piranhas, AL','Ibiapina, CE','Espera Feliz, MG','Brodowski, SP','Álvares Machado, SP','Pirenópolis, GO','Agrestina, PE','Capivari de Baixo, SC','Santa Maria do Pará, PA','São Geraldo do Araguaia, PA','Buritis, MG','Itaporã, MS','Jucás, CE','Cruz, CE','Canhotinho, PE','Piritiba, BA','Junqueiro, AL','Quissamã, RJ','Itaporanga, PB','Igaraçu do Tietê, SP','Conde, PB','Aurora, CE','Potim, SP','Matriz de Camaragibe, AL','Bela Vista, MS','Ribas do Rio Pardo, MS','Paraopeba, MG','Cordeirópolis, SP','Piracanjuba, GO','Igreja Nova, AL','Sarandi, RS','Itabaiana, PB','Brotas, SP','Pão de Açúcar, AL','Apiaí, SP','Pedra Azul, MG','Carolina, MA','Iaçu, BA','Ivoti, RS','São Jerônimo, RS','Uauá, BA','Iracemápolis, SP','Craíbas, AL','Forquilha, CE','Rio Tinto, PB','Irauçuba, CE','Inhapim, MG','Santo Antônio, RN','Tapejara, RS','Cupira, PE','São Lourenço do Oeste, SC','Colorado, PR','Joaquim Gomes, AL','Tupanciretã, RS','São José da Laje, AL','Três de Maio, RS','Três Passos, RS','Porto Franco, MA','Buriti Bravo, MA','Orobó, PE','Laje, BA','Guabiruba, SC','Bambuí, MG','Carutapera, MA','Monte Sião, MG','Cachoeira do Arari, PA','São José da Lapa, MG','Raul Soares, MG','Salvaterra, PA','Corinto, MG','Poço Verde, SE','Chaves, PA','Caraí, MG','João Lisboa, MA','São Sepé, RS','São João do Paraíso, MG','Santa Teresa, ES','Quatro Barras, PR','Rio Formoso, PE','São Miguel, RN','Santa Terezinha de Itaipu, PR','Assaré, CE','Carambeí, PR','Tamandaré, PE','Ibirapitanga, BA','Matinha, MA','Dom Pedro, MA','Princesa Isabel, PB','Ladário, MS','Belmonte, BA','Santo Antônio de Posse, SP','Inajá, PE','Santo Amaro da Imperatriz, SC','Abaeté, MG','Itaocara, RJ','Conceição de Macabu, RJ','Taquarituba, SP','Itambacuri, MG','Tambaú, SP','Peritoró, MA','Sobradinho, BA','Ivinhema, MS','Pancas, ES','Caculé, BA','Teodoro Sampaio, SP','Balneário Piçarras, SC','Coreaú, CE','Loanda, PR','Garopaba, SC','Urucurituba, AM','Itambé, BA','São João de Pirabas, PA','Senador Guiomard, AC','Bataguassu, MS','São Miguel do Guaporé, RO','Itapaci, GO','Altinho, PE','Alta Floresta D Oeste, RO','Ecoporanga, ES','Conselheiro Pena, MG','Orleans, SC','Tocantinópolis, TO','Capinzal, SC','Amaraji, PE','Areia, PB','Mandaguaçu, PR','Imbé, RS','São João, PE','Manhumirim, MG','Encantado, RS','Medeiros Neto, BA','Quaraí, RS','Barro, CE','Goiás, GO','Flores, PE','Rafael Jambeiro, BA','Pedra, PE','Herval d Oeste, SC','Coração de Maria, BA','Conceição da Feira, BA','Paranatinga, MT','Caridade, CE','Morrinhos, CE','Teofilândia, BA','Carmo do Cajuru, MG','Alcobaça, BA','Monte Alegre, RN','Barreira, CE','Acreúna, GO','Araçariguama, SP','Aripuanã, MT','Riachão das Neves, BA','São Vicente Ferrer, MA','Itaparica, BA','Miguelópolis, SP','Mutuípe, BA','Palmital, SP','Ceres, GO','Feira Grande, AL','Quixeré, CE','Ortigueira, PR','Dianópolis, TO','Feira Nova, PE','Alcântara, MA','Carira, SE','Altônia, PR','Diamantino, MT','Caravelas, BA','Pompéia, SP','Parnamirim, PE','Anagé, BA','Trizidela do Vale, MA','Cantanhede, MA','São Miguel do Araguaia, GO','Bonito, MS','Apuí, AM','Porto Grande, AP','Cassilândia, MS','Caracaraí, RR','Cordeiro, RJ','Nova Alvorada do Sul, MS','Uruburetama, CE','Anicuns, GO','Mari, PB','Caaporã, PB','Oliveira dos Brejinhos, BA','Terenos, MS','São José do Vale do Rio Preto, RJ','Silva Jardim, RJ','Camanducaia, MG','Itapecerica, MG','Palmas de Monte Alto, BA','Lucélia, SP','Piúma, ES','São Francisco de Paula, RS','Hidrolândia, GO','Chã Grande, PE','Colônia Leopoldina, AL','Ibicaraí, BA','Olho d Água das Flores, AL','Itaiópolis, SC','Caxambu, MG','Itatira, CE','Mazagão, AP','Centro Novo do Maranhão, MA','Nova Hartz, RS','Paramirim, BA','Santo Antônio do Içá, AM','Araripe, CE','Canarana, MT','Aquidabã, SE','Uruçuí, PI','São Marcos, RS','Cunha, SP','Monte Santo de Minas, MG','Paraguaçu, MG','Fundão, ES','Boquira, BA','Nova Granada, SP','Pradópolis, SP','Pio XII, MA','Parelhas, RN','Guapiaçu, SP','Santa Maria das Barreiras, PA','Manari, PE','Lagoa de Itaenga, PE','Alto Paraíso, RO','Orós, CE','Vargem Alta, ES','Maracaçumé, MA','Perdões, MG','Porto Belo, SC','Paraibano, MA','Nova Xavantina, MT','Nova Esperança do Piriá, PA','Schroeder, SC','São Joaquim do Monte, PE','Nova Petrópolis, RS','Rolante, RS','Bananeiras, PB','São José da Coroa Grande, PE','Bequimão, MA','Urussanga, SC','Cajueiro, AL','Carmo do Rio Claro, MG','Guará, SP','Canto do Buriti, PI','Jandaia do Sul, PR','Buritirama, BA','Nhamundá, AM','Itaquiraí, MS','Monte Alegre de Minas, MG','Crisópolis, BA','Wenceslau Guimarães, BA','Madre de Deus, BA','Quiterianópolis, CE','Paraisópolis, MG','Santa Bárbara do Pará, PA','São Felipe, BA','Taperoá, BA','Itaobim, MG','Campestre, MG','Paulo Ramos, MA','Siqueira Campos, PR','Mirador, MA','Ubiratã, PR','Anori, AM','Castilho, SP','Serro, MG','Bastos, SP','Butiá, RS','Cruzeiro do Oeste, PR','Nova Olinda do Maranhão, MA','Valença do Piauí, PI','Santo Anastácio, SP','Monte Azul, MG','Alagoa Nova, PB','Guaratinga, BA','Maracás, BA','Costa Rica, MS','Medina, MG','Lambari, MG','Barroso, MG','Arroio do Meio, RS','Santa Bárbara, BA','Engenheiro Coelho, SP','Comodoro, MT','Coronel Vivida, PR','Vertentes, PE','Belém do São Francisco, PE','Governador Mangabeira, BA','Capela do Alto, SP','Catarina, CE','Itatinga, SP','Silvânia, GO','Junqueirópolis, SP','São João Batista, MA','São José do Rio Claro, MT','Piratini, RS','São Simão, GO','São João do Piauí, PI','Barra da Estiva, BA','Vazante, MG','Itapoá, SC','Maraú, BA','Muzambinho, MG','Pindoretama, CE','Riacho das Almas, PE','Araçoiaba, PE','Paulistana, PI','Tibagi, PR','Uruçuca, BA','Caraúbas, RN','Itajuípe, BA','Nova Brasilândia D Oeste, RO','Baixa Grande, BA','Tanhaçu, BA','Itapiúna, CE','Itororó, BA','Cachoeirinha, PE','Ibirubá, RS','Cuité, PB','Pinhalzinho, SC','Araruna, PB','Floresta do Araguaia, PA','Nova Olímpia, MT','São Francisco do Guaporé, RO','Chorozinho, CE','Regente Feijó, SP','São José de Piranhas, PB','Cocalzinho de Goiás, GO','Paranapanema, SP','Água Branca, AL','Riachão, MA','Cândido Mendes, MA','Cantagalo, RJ','Santo Antônio do Sudoeste, PR','Padre Paraíso, MG','Pindobaçu, BA','Jaboticatubas, MG','Aragarças, GO','Abaré, BA','Porto Real do Colégio, AL','Capoeiras, PE','Abadiânia, GO','Envira, AM','Andirá, PR','Jaguaruna, SC','Salgado, SE','Cerqueira César, SP','Taquarana, AL','Hidrolândia, CE','Turmalina, MG','Icapuí, CE','Divino, MG','Lajinha, MG','Atalaia do Norte, AM','Ubaíra, BA','Campos Belos, GO','Rubiataba, GO','Buri, SP','Ipanema, MG','Alpinópolis, MG','Santa Luzia do Pará, PA','Magalhães de Almeida, MA','Umirim, CE','Jijoca de Jericoacoara, CE','Riachão do Dantas, SE','Major Isidoro, AL','Buriti dos Lopes, PI','Miracatu, SP','Bombinhas, SC','Plácido de Castro, AC','Chapada dos Guimarães, MT','Cotriguaçu, MT','Itarantim, BA','Rio Verde de Mato Grosso, MS','Campina Verde, MG','Santa Vitória, MG','Palmeirândia, MA','Castelo do Piauí, PI','Brasnorte, MT','Madalena, CE','Porto Real, RJ','Beruri, AM','Pariquera-Açu, SP','Afrânio, PE','Simonésia, MG','Remígio, PB','Alhandra, PB','Presidente Olegário, MG','Ibicoara, BA','Carnaíba, PE','Olho d Água das Cunhãs, MA','Pastos Bons, MA','Novo Airão, AM','Farias Brito, CE','Morros, MA','Pauini, AM','Wenceslau Braz, PR','Borda da Mata, MG','Itanhém, BA','Cajari, MA','Carmópolis de Minas, MG','Horizontina, RS','Sengés, PR','Xapuri, AC','Varzelândia, MG','Papanduva, SC','Júlio de Castilhos, RS','Antas, BA','Três Barras, SC','Sonora, MS','Chopinzinho, PR','Umburanas, BA','Boa Vista do Ramos, AM','Águas Formosas, MG','Iati, PE','Fátima do Sul, MS','Tejuçuoca, CE','Utinga, BA','Serrita, PE','Aroeiras, PB','Ampére, PR','Baependi, MG','Rio Bananal, ES','Capanema, PR','Jaicós, PI','Formosa da Serra Negra, MA','Pitimbu, PB','Ubaitaba, BA','Quitandinha, PR','Alto Araguaia, MT','Guaranésia, MG','Passagem Franca, MA','Monte Azul Paulista, SP','Una, BA','Trairão, PA','Presidente Médici, RO','Caconde, SP','Conceição, PB','Antonina, PR','Mâncio Lima, AC','Ituaçu, BA','Ibirama, SC','Rodrigues Alves, AC','Presidente Sarney, MA','Caiapônia, GO','Dormentes, PE','Matipó, MG','São José dos Quatro Marcos, MT','Viradouro, SP','Ervália, MG','Carmo, RJ','Pirapora do Bom Jesus, SP','São Raimundo das Mangabeiras, MA','Marechal Thaumaturgo, AC','São Luís Gonzaga do Maranhão, MA','Porciúncula, RJ','Carlos Chagas, MG','Montanha, ES','Barão de Grajaú, MA','Juquiá, SP','Cabaceiras do Paraguaçu, BA','São Gabriel, BA','Jaguaripe, BA','Cocos, BA','Terra Santa, PA','Camocim de São Félix, PE','Tonantins, AM','Macarani, BA','Otacílio Costa, SC','Japaratuba, SE','Neópolis, SE','Cruz Machado, PR','Águas de Lindóia, SP','Picuí, PB','Cariús, CE','Mairi, BA','Itapororoca, PB','São Benedito do Rio Preto, MA','Ribeirópolis, SE','Malacacheta, MG','Alumínio, SP','Pirapemas, MA','Mendes, RJ','Ipaba, MG','Contenda, PR','Bacuri, MA','Boa Vista do Tupim, BA','Pocinhos, PB','São João do Soter, MA','Areia Branca, SE','Rio Claro, RJ','Santo Antônio do Amparo, MG','Nazaré Paulista, SP','Guareí, SP','Porto Acre, AC','Reriutaba, CE','Venturosa, PE','Jussara, GO','Colina, SP','Cariré, CE','Formoso do Araguaia, TO','Cafarnaum, BA','Pio IX, PI','Varjota, CE','Augustinópolis, TO','Epitaciolândia, AC','Manga, MG','Taió, SC','Inhapi, AL','Mundo Novo, MS','Buerarema, BA','Mirangaba, BA','Cantá, RR','São Francisco de Assis, RS','Costa Marques, RO','Solonópole, CE','Governador Edison Lobão, MA','Jucurutu, RN','Arroio Grande, RS','Mirante do Paranapanema, SP','Miracema do Tocantins, TO','Batalha, AL','Sapucaia, RJ','Maraã, AM','Paraibuna, SP','Luz, MG','Ibipeba, BA','Correntes, PE','Estrela de Alagoas, AL','Banabuiú, CE','Rio Maria, PA','Cairu, BA','Juazeirinho, PB','Jaguaretama, CE','Itirapina, SP','Itacarambi, MG','Cesário Lange, SP','Garuva, SC','Cafelândia, PR','Ladainha, MG','Campo do Brito, SE','Ingá, PB','Fronteira, MG','Sítio Novo, MA','Lagoa do Carro, PE','Croatá, CE','Lagoa Formosa, MG','São Caetano de Odivelas, PA','São João do Rio do Peixe, PB','São Vicente Férrer, PE','Regeneração, PI','Indiaroba, SE','Matelândia, PR','Gonçalves Dias, MA','Curionópolis, PA','Rio Pomba, MG','Abelardo Luz, SC','Conchas, SP','Fátima, BA','Arinos, MG','Cristinápolis, SE','Poção de Pedras, MA','Jacupiranga, SP','Messias, AL','Mucajaí, RR','Lagoa da Canoa, AL','Ourém, PA','Conceição do Mato Dentro, MG','Piaçabuçu, AL','Pontalina, GO','Boqueirão, PB']
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = ttk.Label(
            main_frame,
            text="John Deere Dealer Locator",
            style='Header.TLabel',
            anchor="center",
            justify="center"
        )
        header_label.pack(pady=(0, 20))

        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(pady=10)
        logo_label = ttk.Label(
            logo_frame,
            text="🚜",
            font=('Helvetica', 48),
        )
        logo_label.pack()

        self.status_frame = ttk.Frame(main_frame, style="TFrame")
        self.status_frame.pack(fill=tk.X, pady=10)
        self.status_label = ttk.Label(
            self.status_frame,
            text="Pronto para iniciar a extração",
            style='Status.TLabel',
            anchor="center",
            justify="center"
        )
        self.status_label.pack(fill=tk.X)

        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="indeterminate"
        )
        self.progress.pack(pady=10)

        log_frame = ttk.Frame(main_frame, style="TFrame")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 20))
        log_label = ttk.Label(
            log_frame,
            text="Log de Processamento",
            font=('Helvetica', 12, 'bold'),
            anchor="center",
            justify="center"
        )
        log_label.pack(pady=(0, 5))
        self.log_text = ScrolledText(log_frame, height=10, state='disabled', wrap='word',
                                     bg='#f0f0f0', bd=0, relief="flat", highlightthickness=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=10)

        self.argentina_button = ttk.Button(
            button_frame,
            text="Extrair Argentina",
            command=self.start_scraping_argentina_thread,
            padding=(20, 1)
        )
        self.argentina_button.pack(side=tk.LEFT, padx=10)

        self.brasil_button = ttk.Button(
            button_frame,
            text="Extrair Brasil",
            command=self.start_scraping_brasil_thread,
            padding=(20, 1)
        )
        self.brasil_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = ttk.Button(
            button_frame,
            text="Sair",
            command=self.root.quit,
            padding=(20, 1)
        )
        self.exit_button.pack(side=tk.LEFT, padx=10)

    def update_status(self, message):
        """Atualiza a mensagem de status exibida no topo da janela, centralizada."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def append_log(self, message):
        """Adiciona uma nova linha ao log de processamento."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_scraping_argentina_thread(self):
        thread = threading.Thread(target=self.run_scraper_argentina)
        thread.daemon = True
        thread.start()

    def start_scraping_brasil_thread(self):
        thread = threading.Thread(target=self.run_scraper_brasil)
        thread.daemon = True
        thread.start()

    def run_scraper_argentina(self):
        self.argentina_button.config(state='disabled')
        self.brasil_button.config(state='disabled')
        self.progress.start()

        self.update_status("Argentina: Selecionando local para salvar arquivo CSV...")
        output_file = filedialog.asksaveasfilename(
            title="Selecione o local para salvar o arquivo CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not output_file:
            self.reset_ui("Operação cancelada.")
            return

        self.update_status("🇦🇷 Argentina: Selecionando ChromeDriver...")
        driver_path = filedialog.askopenfilename(
            title="Selecione o executável do ChromeDriver",
            filetypes=[("Executável", "*.exe")]
        )
        if not driver_path:
            self.reset_ui("ChromeDriver não selecionado.")
            return

        self.update_status("Argentina: Selecionando Google Chrome (opcional)...")
        chrome_path = filedialog.askopenfilename(
            title="Selecione o executável do Google Chrome (Opcional)",
            filetypes=[("Executável", "*.exe")]
        )

        try:
            self.update_status("🇦🇷 Argentina: Iniciando o navegador...")
            options = webdriver.ChromeOptions()
            if chrome_path:
                options.binary_location = chrome_path
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://dealerlocator.deere.com/servlet/country=BR")
            time.sleep(2)

            unique_entries = set()

            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Dealer", "Endereço 1", "Endereço 2"])

                primeira_cidade = self.listadecidades[0]
                self.update_status(f"Argentina: Processando cidade inicial: {primeira_cidade}")
                self.append_log(f"[Argentina] Iniciando com a cidade: {primeira_cidade}")
                self.process_first_city(driver, primeira_cidade)

                for index, cidade in enumerate(self.listadecidades):
                    self.update_status(f"Processando cidade: {cidade} ({index+1}/{len(self.listadecidades)})")
                    try:
                        self.process_city_argentina(driver, cidade, writer, unique_entries)
                        self.ensure_continue(driver)
                        self.append_log(f"[Argentina] Cidade processada com sucesso: {cidade}")
                    except Exception as e:
                        error_msg = f"[Argentina] Erro ao processar {cidade}: {str(e)}"
                        self.update_status(error_msg)
                        self.append_log(error_msg)
                        continue

                    if (index + 1) % 100 == 0:
                        self.update_status("Reiniciando navegador para evitar travamentos...")
                        driver.quit()
                        time.sleep(2)
                        driver = webdriver.Chrome(service=service, options=options)
                        driver.get("https://dealerlocator.deere.com/servlet/country=BR")
                        time.sleep(2)
                        self.process_first_city(driver, primeira_cidade)

            driver.quit()
            self.reset_ui("Extração Argentina concluída com sucesso!")
            messagebox.showinfo("Sucesso", "A extração Argentina foi concluída com sucesso!")

        except Exception as e:
            self.reset_ui(f"Erro durante a execução: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a execução: {e}")

    def process_first_city(self, driver, cidade):
        entrada = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="google-page-level-search2"]'))
        )
        entrada.clear()
        entrada.send_keys(cidade)

        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
        )
        submit.click()

        tile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="tiles"]//span[text()="Agricultura"]'))
        )
        tile.click()

        findDealer = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary" and text()="Encontrar Concessionários"]'))
        )
        findDealer.click()

    def process_city_argentina(self, driver, cidade, writer, unique_entries):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='list-wrap-background']"))
            )
        except TimeoutException:
            self.update_status(f"Tela travada sem resultados para {cidade}.")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all("div", class_="list-wrap-background")

        if not results:
            self.update_status(f"Nenhum resultado encontrado para {cidade}")
        else:
            for result in results:
                dealer_name_div = result.find("div", class_="dealer-name")
                dealer_name = dealer_name_div.find("h5").text.strip() if dealer_name_div else "Nome não encontrado"

                address_divs = result.find_all("div", class_="address")
                endereco1 = address_divs[0].text.strip() if len(address_divs) > 0 else ""
                endereco2 = address_divs[1].text.strip() if len(address_divs) > 1 else ""
                endereco3 = address_divs[2].text.strip() if len(address_divs) > 2 else ""

                if endereco3:
                    endereco2 = f"{endereco2}, {endereco3}" if endereco2 else endereco3

                entry_key = (dealer_name, endereco1)
                if entry_key not in unique_entries:
                    unique_entries.add(entry_key)
                    writer.writerow([dealer_name, endereco1, endereco2])

        # Prepara a busca para a próxima cidade
        entrada = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='google-page-level-search3']"))
        )
        entrada.clear()
        entrada.send_keys(cidade)

        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
        )
        submit.click()

        # Se não houver informações, tenta novamente
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='list-wrap-background']"))
                )
                break
            except TimeoutException:
                self.update_status(
                    f"Sem informações para {cidade}. Pressionando 'Ir' novamente (tentativa {attempts+1}/{max_attempts})..."
                )
                submit = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
                )
                submit.click()
                attempts += 1

        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='list-wrap-background']"))
            )
        except TimeoutException:
            self.update_status(f"Resultados ainda não carregados para {cidade} após várias tentativas.")

    def ensure_continue(self, driver):
        time.sleep(1)

    def run_scraper_brasil(self):
        self.argentina_button.config(state='disabled')
        self.brasil_button.config(state='disabled')
        self.progress.start()

        self.update_status("Brasil: Selecionando local para salvar arquivo CSV...")
        output_file = filedialog.asksaveasfilename(
            title="Selecione o local para salvar o arquivo CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not output_file:
            self.reset_ui("Operação cancelada.")
            return

        self.update_status("Brasil: Selecionando ChromeDriver...")
        driver_path = filedialog.askopenfilename(
            title="Selecione o executável do ChromeDriver",
            filetypes=[("Executável", "*.exe")]
        )
        if not driver_path:
            self.reset_ui("ChromeDriver não selecionado.")
            return

        self.update_status("Brasil: Selecionando Google Chrome (opcional)...")
        chrome_path = filedialog.askopenfilename(
            title="Selecione o executável do Google Chrome (Opcional)",
            filetypes=[("Executável", "*.exe")]
        )

        try:
            self.update_status("Brasil: Iniciando o navegador...")
            options = webdriver.ChromeOptions()
            if chrome_path:
                options.binary_location = chrome_path
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://dealerlocator.deere.com/servlet/country=BR")
            time.sleep(2)

            entrada = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="google-page-level-search2"]'))
            )
            entrada.clear()
            entrada.send_keys(self.listadecidadesBR[0])

            submit = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
            )
            submit.click()

            tile = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="tiles"]//span[text()="Agricultura"]'))
            )
            tile.click()

            findDealer = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary" and text()="Encontrar Concessionários"]'))
            )
            findDealer.click()

            cnpj_set = set()

            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Dealer", "Endereço 1", "Endereço 2", "CNPJ"])

                for index, cidade in enumerate(self.listadecidadesBR):
                    self.update_status(f"Processando cidade: {cidade} ({index+1}/{len(self.listadecidadesBR)})")
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='list-wrap-background']"))
                        )
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        results = soup.find_all("div", class_="list-wrap-background")
                        if not results:
                            self.update_status(f"Nenhum resultado encontrado para {cidade}")
                            self.append_log(f"[Brasil] Nenhum resultado para: {cidade}")
                            continue

                        for result in results:
                            address_divs = result.find_all("div", class_="address")
                            if len(address_divs) >= 3:
                                endereco1 = address_divs[0].text.strip()
                                endereco2 = f"{address_divs[1].text.strip()} {address_divs[2].text.strip()}"
                            elif len(address_divs) == 2:
                                endereco1 = address_divs[0].text.strip()
                                endereco2 = address_divs[1].text.strip()
                            else:
                                endereco1 = address_divs[0].text.strip() if address_divs else ""
                                endereco2 = ""

                            cnpj_div = result.find("span", string=lambda text: text and "CNPJ" in text)
                            cnpj = cnpj_div.find_next("span").text.strip() if cnpj_div else "CNPJ não encontrado"

                            if cnpj in cnpj_set:
                                continue
                            cnpj_set.add(cnpj)

                            razao_div = result.find("span", string=lambda text: text and "Razão Social" in text)
                            razao_social = razao_div.find_next("span").text.strip() if razao_div else "Razão Social não encontrada"

                            writer.writerow([razao_social, endereco1, endereco2, cnpj])

                        self.append_log(f"[Brasil] Cidade processada com sucesso: {cidade}")

                        entrada = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@id='google-page-level-search3']"))
                        )
                        entrada.clear()
                        entrada.send_keys(cidade)

                        submit = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
                        )
                        submit.click()

                        try:
                            WebDriverWait(driver, 1).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//div[contains(@class, "error-sms") and contains(text(), "Oops!")]')
                                )
                            )
                            self.update_status(f"Erro detectado para {cidade}. Tentando novamente...")
                            retry_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH, '//button[@id="submit-form11" and contains(text(), "Ir")]'))
                            )
                            retry_button.click()
                        except TimeoutException:
                            self.update_status(f"Nenhum erro detectado para {cidade}.")

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='list-wrap-background']"))
                        )

                    except Exception as e:
                        error_msg = f"[Brasil] Erro ao processar a cidade {cidade}: {e}"
                        self.update_status(error_msg)
                        self.append_log(error_msg)
                        continue

                    if (index + 1) % 100 == 0:
                        self.update_status("🇧🇷 Reiniciando navegador para evitar travamentos...")
                        driver.quit()
                        time.sleep(2)
                        driver = webdriver.Chrome(service=service, options=options)
                        driver.get("https://dealerlocator.deere.com/servlet/country=BR")
                        time.sleep(2)
                        entrada = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="google-page-level-search2"]'))
                        )
                        entrada.clear()
                        entrada.send_keys(self.listadecidadesBR[0])
                        
                        submit = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-form11"]'))
                        )
                        submit.click()
                        
                        tile = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//div[@class="tiles"]//span[text()="Agricultura"]'))
                        )
                        tile.click()
                        
                        findDealer = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary" and text()="Encontrar Concessionários"]'))
                        )
                        findDealer.click()

            driver.quit()
            self.reset_ui("Extração Brasil concluída com sucesso!")
            messagebox.showinfo("Sucesso", "A extração Brasil foi concluída com sucesso!")

        except Exception as e:
            self.reset_ui(f"Erro durante a execução: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a execução: {e}")

    def reset_ui(self, status_message):
        self.progress.stop()
        self.argentina_button.config(state='normal')
        self.brasil_button.config(state='normal')
        self.update_status(status_message)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DealerLocatorApp()
    app.run()