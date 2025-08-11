# Deployment of K3s Cluster in Google Cloud

In this lab, We are going to deploy k3s cluster on Google cloud.

## Create a VPC in Google Cloud

1. From console, select `VPC network`
2. `Create VPC network`:
    - `Name`: choose a vpc name, example: `k3s-cluster-vpc`
    - Subnet creation mode: `custom`
    - in Subnets, give a `subnet name`, `region`, `ip stack as IPv4` and IPv4 range, example: `10.0.0.0/16`
    - You can add more subnets in this way

3. Dynamic Routing Mode: `regional`
4. Firewall settings:
    - `Allow ICMP`, `Internal Traffic`, `SSH` and `RDP`
5. submit to create vpc

## Creating VM Instances



## Setting the EC2 Instances

We are going to deploy k3s cluster between three instances:

- One for the master node
- Two for the worker nodes

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k3s-app
  labels:
    app: k3s-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: k3s-app
  template:
    metadata:
      labels:
        app: k3s-app
    spec:
      containers:
        - name: k3s-app
          image: nginx:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: k3s-app-service
  name: k3s-app-service
spec:
  ports:
    - name: "3000-80"
      port: 3000
      protocol: TCP
      targetPort: 80
  selector:
    app: k3s-app
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: k3s-app-ingress
  annotations:
    ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: k3s-app-service
                port:
                  number: 3000
```

## Explanation

- Deployment:
    - The Deployment named k3s-app is updated to use the nginx:latest image.
    - It will create a single replica (replicas: 1) of the Nginx container.

- Service:
    - The Service named k3s-app-service is set to expose port 3000 and maps it to port 80 of the Nginx container.
    - It uses a ClusterIP type service to expose the application internally within the cluster.

- Ingress:
    - The Ingress named k3s-app-ingress is configured to route HTTP traffic to the k3s-app-service on port 3000.
    - The annotation ingress.kubernetes.io/ssl-redirect: "false" indicates that SSL redirection is disabled.
