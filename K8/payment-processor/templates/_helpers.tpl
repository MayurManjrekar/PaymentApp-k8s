{{- define "processor.name" -}}
payment-processor
{{- end }}

{{- define "processor.fullname" -}}
{{ include "processor.name" . }}
{{- end }}

{{- define "processor.labels" -}}
app: {{ include "processor.name" . }}
{{- end }}