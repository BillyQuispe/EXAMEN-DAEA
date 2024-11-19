// Crear base de datos
db = db.getSiblingDB('MiBaseDeDatos');  // Usar la base de datos MiBaseDeDatos

// Crear colecciones y agregar datos

// Crear la colección de Usuarios
db.createCollection('Usuarios');
db.Usuarios.insertMany([
    { "ID": 1, "Nombre": "John_Perez" },
    { "ID": 2, "Nombre": "Maria_Lopez" },
    { "ID": 3, "Nombre": "Carlos_Garcia" },
    { "ID": 4, "Nombre": "Anna_Torres" },
    { "ID": 5, "Nombre": "Louis_Mendoza" },
    { "ID": 6, "Nombre": "Laura_Fernandez" },
    { "ID": 7, "Nombre": "Peter_Sanchez" },
    { "ID": 8, "Nombre": "Sophia_Ramirez" },
    { "ID": 9, "Nombre": "Daniel_Silva" },
    { "ID": 10, "Nombre": "Helen_Flores" }
]);

// Crear la colección de Skills
db.createCollection('Skills');
db.Skills.insertMany([
    { "ID": 1, "Nombre": "Backend_Programming" },
    { "ID": 2, "Nombre": "Frontend_Programming" },
    { "ID": 3, "Nombre": "Mobile_Programming" },
    { "ID": 4, "Nombre": "Graphic_Design" },
    { "ID": 5, "Nombre": "Project_Management" },
    { "ID": 6, "Nombre": "Service_Management" },
    { "ID": 7, "Nombre": "Data_Analysis" },
    { "ID": 8, "Nombre": "Digital_Marketing" },
    { "ID": 9, "Nombre": "Artificial_Intelligence" },
    { "ID": 10, "Nombre": "Cybersecurity" }
]);

// Crear la colección de UsuarioSkills
db.createCollection('UsuarioSkills');
db.UsuarioSkills.insertMany([
    { "ID": 1, "ID_Usuario": 1, "ID_Skill": 1, "Puntuacion": 95 },
    { "ID": 2, "ID_Usuario": 2, "ID_Skill": 2, "Puntuacion": 88 },
    { "ID": 3, "ID_Usuario": 3, "ID_Skill": 3, "Puntuacion": 92 },
    { "ID": 4, "ID_Usuario": 4, "ID_Skill": 4, "Puntuacion": 90 },
    { "ID": 5, "ID_Usuario": 5, "ID_Skill": 5, "Puntuacion": 96 },
    { "ID": 6, "ID_Usuario": 6, "ID_Skill": 6, "Puntuacion": 89 },
    { "ID": 7, "ID_Usuario": 7, "ID_Skill": 7, "Puntuacion": 91 },
    { "ID": 8, "ID_Usuario": 8, "ID_Skill": 8, "Puntuacion": 85 },
    { "ID": 9, "ID_Usuario": 9, "ID_Skill": 9, "Puntuacion": 93 },
    { "ID": 10, "ID_Usuario": 10, "ID_Skill": 10, "Puntuacion": 87 },
    { "ID": 11, "ID_Usuario": 1, "ID_Skill": 2, "Puntuacion": 80 },
    { "ID": 12, "ID_Usuario": 2, "ID_Skill": 3, "Puntuacion": 76 },
    { "ID": 13, "ID_Usuario": 3, "ID_Skill": 1, "Puntuacion": 78 },
    { "ID": 14, "ID_Usuario": 4, "ID_Skill": 5, "Puntuacion": 83 },
    { "ID": 15, "ID_Usuario": 5, "ID_Skill": 6, "Puntuacion": 75 },
    { "ID": 16, "ID_Usuario": 6, "ID_Skill": 9, "Puntuacion": 90 },
    { "ID": 17, "ID_Usuario": 7, "ID_Skill": 10, "Puntuacion": 82 },
    { "ID": 18, "ID_Usuario": 8, "ID_Skill": 1, "Puntuacion": 88 },
    { "ID": 19, "ID_Usuario": 9, "ID_Skill": 8, "Puntuacion": 86 },
    { "ID": 20, "ID_Usuario": 10, "ID_Skill": 7, "Puntuacion": 79 }
]);
