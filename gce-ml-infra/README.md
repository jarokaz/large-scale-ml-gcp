### Provisioning A2 based AI Platform Notebook

```

gcloud compute instances create jk-a2-n1 \
   --project jk-mlops-dev \
   --zone us-central1-c \
   --machine-type a2-highgpu-1g \
   --maintenance-policy TERMINATE --restart-on-failure \
   --image-family tf2-ent-2-3-cu110 \
   --image-project deeplearning-platform-release \
   --boot-disk-size 200GB \
   --metadata "install-nvidia-driver=True,proxy-mode=project_editors" \
   --scopes https://www.googleapis.com/auth/cloud-platform
   
   ```
