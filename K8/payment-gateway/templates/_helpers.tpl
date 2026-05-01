{{- define "gateway.name" -}}
payment-gateway
{{- end }}

{{- define "gateway.fullname" -}}
{{ include "gateway.name" . }}
{{- end }}

{{- define "gateway.labels" -}}
app: {{ include "gateway.name" . }}
{{- end }}