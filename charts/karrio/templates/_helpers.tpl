{{/*
Expand the name of the chart.
*/}}
{{- define "karrio.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "karrio.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "karrio.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "karrio.labels" -}}
helm.sh/chart: {{ include "karrio.chart" . }}
{{ include "karrio.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "karrio.selectorLabels" -}}
app.kubernetes.io/name: {{ include "karrio.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "karrio.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "karrio.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Server image
*/}}
{{- define "karrio.serverImage" -}}
{{- $tag := default .Chart.AppVersion .Values.image.server.tag }}
{{- printf "%s:%s" .Values.image.server.repository $tag }}
{{- end }}

{{/*
Dashboard image
*/}}
{{- define "karrio.dashboardImage" -}}
{{- $tag := default .Chart.AppVersion .Values.image.dashboard.tag }}
{{- printf "%s:%s" .Values.image.dashboard.repository $tag }}
{{- end }}

{{/*
Secret name — either existing or chart-managed
*/}}
{{- define "karrio.secretName" -}}
{{- if .Values.existingSecret }}
{{- .Values.existingSecret }}
{{- else }}
{{- include "karrio.fullname" . }}
{{- end }}
{{- end }}

{{/*
ConfigMap name
*/}}
{{- define "karrio.configMapName" -}}
{{- include "karrio.fullname" . }}
{{- end }}
