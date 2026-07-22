# bia-iungo-dashboards

Repositorio contenedor de herramientas internas (dashboards, infografías, portales)
para bia restaurants hub / iungo. Desplegado automáticamente en Netlify: cada `git push`
a `main` actualiza el sitio en vivo.

## Estructura

```
/
├── index.html                     ← panel principal (lista de proyectos)
├── compras-directas-bia-qsr/
│   └── index.html                 ← infografía interactiva de Compras Directas
└── (próximos proyectos aquí, cada uno en su propia carpeta)
```

## Cómo agregar un nuevo proyecto

1. Crea una carpeta nueva en la raíz, ej. `dashboard-consumos/`
2. Coloca ahí el `index.html` (o los archivos) de ese proyecto
3. Agrega una tarjeta nueva en `index.html` (raíz) con el link a `./nombre-carpeta/`
4. `git add . && git commit -m "Agrega [nombre del proyecto]" && git push`
5. Netlify vuelve a desplegar solo, en ~30 segundos

## URLs típicas

- Panel general: `https://TU-SITIO.netlify.app/`
- Un proyecto: `https://TU-SITIO.netlify.app/compras-directas-bia-qsr/`
