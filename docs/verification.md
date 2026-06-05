# Verificación — Cómo demostrar que el hallazgo es válido

> Regla de oro: **el agente no dice "es vulnerable", lo demuestra**.
> Todo hallazgo termina con evidencia ejecutable, no con afirmaciones.

## Niveles de verificación

### Nivel 1 — Verificación de estructura (obligatorio)

El harness debe pasar `./init.sh` sin errores:

```bash
bash init.sh
```

Debe terminar con:
```
[OK]    Harness verificado correctamente.
```

### Nivel 2 — Validación de archivos JSON (obligatorio para config)

Todo archivo `.json` debe ser válido:

```bash
python3 -c "import json; json.load(open('feature_list.json'))"
```

`feature_list.json` debe cumplir:
- Tiene array `features` con al menos un elemento.
- Cada feature tiene campos `id`, `name`, `status`.
- Máximo 1 feature en estado `in_progress`.
- Estados válidos: `pending`, `in_progress`, `done`, `blocked`.

### Nivel 3 — Validación de hallazgos de seguridad (crítico)

Cada hallazgo reportado debe tener:

- [ ] Descripción clara de la vulnerabilidad
- [ ] Pasos para reproducir (reproducibles por otro agente)
- [ ] Prueba de concepto (PoC) funcional
- [ ] Clasificación CVSS (Critical/High/Medium/Low)
- [ ] Evidencia (screenshot, log, video, request/response)
- [ ] Recomendación de remediación

### Nivel 4 — Verificación de herramientas de hacking

El harness puede verificar herramientas disponibles:

```bash
# Verificar nmap
nmap --version

# Verificar curl
curl --version

# Verificar python3
python3 --version
```

## Anti-patrones (no hacer)

- ❌ "El puerto 80 está abierto, debería ser explotable." → demostrar con PoC.
- ❌ "Ejecuté un exploit y funcionó." → mostrar evidencia (screenshot, output).
- ❌ Reportar vulnerabilidad sin pasos de reproducción.
- ❌ Marcar feature como `done` sin pasar `./init.sh`.
- ❌ Editar `progress/history.md` entradas anteriores. → solo append al final.

## Verificación final antes de cerrar sesión

```bash
./init.sh           # debe terminar con [OK]
```

Si `./init.sh` está rojo, **no** marques nada como `done`. Anota el bloqueo
en `progress/current.md` con estado `blocked` en `feature_list.json`.

## Checklist de cierre de sesión

- [ ] `./init.sh` pasa verde.
- [ ] Feature completada marcada como `done` en `feature_list.json`.
- [ ] Hallazgos documentados con PoC y evidencia.
- [ ] Resumen de sesión añadido al final de `progress/history.md`.
- [ ] `progress/current.md` vaciado (dejar solo plantilla).
- [ ] No quedan archivos temporales, payloads, ni credenciales.
- [ ] No hay TODOs sin contexto en el código/documentos.
