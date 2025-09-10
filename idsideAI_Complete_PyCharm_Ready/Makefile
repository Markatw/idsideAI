
NS ?= idecide

deploy-eso:
	kubectl apply -f k8s/eso-aws-secret-store.yaml
	kubectl apply -f k8s/external-secret-neo4j.yaml -n $(NS)

patch-backend:
	kubectl patch deploy/idecide-backend -n $(NS) --patch-file k8s/backend-deploy.patch.yaml

apply-sa:
	kubectl apply -f k8s/backend-serviceaccount.yaml -n $(NS)

deploy-secrets-and-patch: deploy-eso apply-sa patch-backend
	@echo 'Secrets wired and backend patched.'


perf-k6:
	k6 run perf/k6_api_test.js

deploy-secrets-and-patch:
	kubectl apply -f k8s/eso-aws-secret-store.yaml
	kubectl apply -f k8s/external-secret-neo4j.yaml
	kubectl apply -f k8s/backend-serviceaccount.yaml
	kubectl patch deploy/idecide-backend --patch-file k8s/backend-deploy.patch.yaml

