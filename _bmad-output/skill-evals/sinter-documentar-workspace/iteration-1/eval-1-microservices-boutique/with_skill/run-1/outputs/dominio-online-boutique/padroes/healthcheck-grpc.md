---
id: std-healthcheck-grpc
kind: standard
subject: standard:healthcheck-grpc
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/checkoutservice/main.go#L245-L254
    version: 38e7348
    extraction: extracted
---

# Health check padrão gRPC

Todo serviço gRPC do domínio registra o serviço padrão `grpc.health.v1.Health` (`Check`/`Watch`), consumido pelas probes nativas `readinessProbe.grpc`/`livenessProbe.grpc` do Kubernetes — sem sidecar externo de health check. Na maioria dos serviços, `Check` sempre devolve `SERVING` sem de fato testar as dependências (bancos, outros serviços).

## Exemplo
```go
func (cs *checkoutService) Check(ctx context.Context, req *healthpb.HealthCheckRequest) (*healthpb.HealthCheckResponse, error) {
	return &healthpb.HealthCheckResponse{Status: healthpb.HealthCheckResponse_SERVING}, nil
}
```

## Onde se aplica
Todos os serviços gRPC Go/Node/Python/C#/Java do domínio.
