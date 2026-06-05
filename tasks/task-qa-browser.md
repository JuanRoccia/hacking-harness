# Tareas Específicas: QA-BROWSER (Security Validation)

## Objetivo Principal
Validar que la aplicación objetivo sea segura desde la perspectiva del
navegador, detectando vulnerabilidades XSS, CSRF, y problemas de
configuración de seguridad antes de cerrar el pentesting.

---

## TASK-QA-001 — XSS Reflected Test

Verificar vulnerabilidades de XSS reflejado en parámetros GET/POST.

### Pasos
1. Abrir `${APP_URL}` en viewport desktop 1280px
2. Identificar formularios y parámetros GET
3. Inyectar payload `<script>alert('XSS-TEST-001')</script>`
4. Verificar si el payload se ejecuta en el navegador
5. Screenshot del resultado
6. Probar alternativas: `<img src=x onerror=alert(1)>`, `<svg onload=alert(1)>`

### Checkpoints
- [ ] Payloads básicos no ejecutados
- [ ] Caracteres especiales escapados/sanitizados
- [ ] Content-Type correcto (text/html vs application/json)
- [ ] Screenshot de cada test tomado

---

## TASK-QA-002 — XSS Stored Test

Verificar vulnerabilidades de XSS almacenado en formularios persistentes.

### Pasos
1. Ir a formularios que persisten datos (comentarios, perfiles, reseñas)
2. Completar con payload: `<script>alert('XSS-STORED')</script>`
3. Screenshot del formulario antes de enviar
4. Enviar y recargar la página
5. Verificar si el payload se ejecuta al cargar
6. Screenshot del resultado

### Checkpoints
- [ ] Payloads no se almacenan sin sanitizar
- [ ] Datos persistidos se escapan al renderizar
- [ ] No hay XSS almacenado detectable

---

## TASK-QA-003 — CSRF Test

Verificar protección CSRF en formularios críticos.

### Pasos
1. Identificar formularios críticos (login, cambio password, transferencias)
2. Verificar presencia de token CSRF en el formulario
3. Intentar enviar formulario sin token
4. Intentar enviar con token modificado
5. Verificar header `SameSite` en cookies de sesión

### Checkpoints
- [ ] Tokens CSRF presentes en formularios críticos
- [ ] Tokens CSRF validados server-side
- [ ] Cookies SameSite configuradas (Lax o Strict)
- [ ] Origin/Referer headers validados

---

## TASK-QA-004 — Security Headers

Verificar configuración de headers de seguridad HTTP.

### Pasos
1. Ejecutar desde terminal: `curl -sI ${APP_URL}`
2. Verificar headers de seguridad presentes

### Headers a verificar
```bash
curl -sI https://target.com | grep -iE "strict-transport-security|x-frame-options|x-content-type-options|content-security-policy|referrer-policy|permissions-policy"
```

### Checkpoints
- [ ] Strict-Transport-Security presente (HSTS)
- [ ] X-Frame-Options: DENY o SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] Content-Security-Policy configurada
- [ ] Referrer-Policy configurada

---

## TASK-QA-005 — Cookie Security

Verificar configuración de cookies de sesión.

### Pasos
1. Login en la aplicación
2. Capturar cookie de sesión desde DevTools
3. Verificar flags de seguridad

### Checkpoints
- [ ] HttpOnly flag presente (no accesible via JS)
- [ ] Secure flag presente (solo HTTPS)
- [ ] SameSite configurado (Lax o Strict)
- [ ] Path scope apropiado
- [ ] Expiración razonable

---

## TASK-QA-006 — Clickjacking Test

Verificar protección contra clickjacking.

### Pasos
1. Crear HTML de prueba:
```html
<html>
<body>
  <iframe src="${APP_URL}" width="500" height="500"></iframe>
</body>
</html>
```
2. Verificar si la página se carga en el iframe

### Checkpoints
- [ ] X-Frame-Options: DENY o SAMEORIGIN presente
- [ ] O CSP frame-ancestors configurado
- [ ] Página no cargable en iframe desde otro origen

---

## TASK-QA-007 — Regression Security Smoke Test

Prueba rápida post-deploy para verificar que no se introdujeron regresiones
de seguridad.

### Pasos
1. Verificar headers de seguridad → recordatorio
2. Login con credenciales de prueba
3. Verificar cookie flags
4. Probar XSS básico en formulario de búsqueda
5. Logout → verificar sesión destruida

### Criterio de PASS/FAIL
- PASS: todas las verificaciones pasan
- FAIL: cualquier header faltante, XSS sin sanitizar, o cookie insegura

---

## Formato de Reporte

Usar el formato definido en `agents/07-qa-browser.md` (sección "Formato de reporte").
Incluir security score, screenshots, y pasos de reproducción para cada hallazgo.

---

*Última actualización: Junio 2026*
