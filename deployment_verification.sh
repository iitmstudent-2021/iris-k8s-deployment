
# ================================================================
# KUBERNETES DEPLOYMENT VERIFICATION GUIDE
# ================================================================

# 1. Get GKE cluster credentials
gcloud container clusters get-credentials iris-cluster --zone=us-central1-a

# 2. Check all pods are running (should show 2 pods)
kubectl get pods
# Expected output:
# NAME                              READY   STATUS    RESTARTS   AGE
# iris-classifier-xxxxxxxx-xxxxx    1/1     Running   0          2m
# iris-classifier-xxxxxxxx-xxxxx    1/1     Running   0          2m

# 3. Check deployment status
kubectl get deployments
# Expected output:
# NAME              READY   UP-TO-DATE   AVAILABLE   AGE
# iris-classifier   2/2     2            2           5m

# 4. Check service and get EXTERNAL-IP
kubectl get services iris-api-service
# Expected output:
# NAME               TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
# iris-api-service   LoadBalancer   10.x.x.x      34.x.x.x        80:xxxxx/TCP   5m

# 5. Describe deployment (detailed info)
kubectl describe deployment iris-classifier

# 6. Check pod logs (replace POD_NAME with actual pod name)
kubectl logs POD_NAME

# 7. Check logs for all pods with label app=iris-api
kubectl logs -l app=iris-api --tail=50

# 8. Get detailed pod information
kubectl get pods -l app=iris-api -o wide

# 9. Check pod events
kubectl get events --sort-by='.lastTimestamp' | grep iris

# 10. Test pod health (exec into pod)
kubectl exec -it POD_NAME -- /bin/bash

# ================================================================
# TROUBLESHOOTING COMMANDS
# ================================================================

# Check if pods are failing
kubectl get pods | grep -v Running

# Get pod error details
kubectl describe pod POD_NAME

# Check resource usage
kubectl top pods
kubectl top nodes

# Restart deployment (if needed)
kubectl rollout restart deployment iris-classifier

# Check rollout status
kubectl rollout status deployment iris-classifier

# View deployment history
kubectl rollout history deployment iris-classifier

# Scale deployment manually
kubectl scale deployment iris-classifier --replicas=3

# ================================================================
# CLEANUP COMMANDS (USE WITH CAUTION!)
# ================================================================

# Delete service (removes LoadBalancer)
# kubectl delete service iris-api-service

# Delete deployment (removes all pods)
# kubectl delete deployment iris-classifier

# Delete entire cluster (DELETES EVERYTHING!)
# gcloud container clusters delete iris-cluster --zone=us-central1-a
