PROJECT_ID=your_proj_id

gcloud beta compute --project=$PROJECT_ID instances create dlvm-marketplace-tf-2-3-1-vm-1 
--zone=us-central1-a \
--machine-type=n1-standard-64 \
--subnet=default \
--network-tier=PREMIUM \
--metadata=framework=TensorFlow:2.3,google-logging-enable=0,google-monitoring-enable=0,install-nvidia-driver=True,proxy-mode=project_editors,proxy-url=200c97a00c193e48-dot-us-central1.notebooks.googleusercontent.com,shutdown-script=/opt/deeplearning/bin/shutdown_script.sh,status-config-url=https://runtimeconfig.googleapis.com/v1beta1/projects/kz-2021-267823/configs/dlvm-marketplace-tf-2-3-1-config,status-uptime-deadline=600,status-variable-path=status,title=TensorFlow2.3/Keras.CUDA11.0,version=56 \
--maintenance-policy=TERMINATE \
--service-account=156596422468-compute@developer.gserviceaccount.com \
--scopes=https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/logging.admin,https://www.googleapis.com/auth/monitoring,https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/cloud.useraccounts.readonly,https://www.googleapis.com/auth/cloudruntimeconfig \
--accelerator=type=nvidia-tesla-v100,count=8 \
--tags=deeplearning-vm,dlvm-marketplace-tf-2-3-1-deployment \
--image=tf2-2-3-cu110-v20200912-debian-9 \
--image-project=click-to-deploy-images \
--boot-disk-size=200GB \
--boot-disk-type=pd-ssd \
--boot-disk-device-name=dlvm-marketplace-tf-2-3-1-vm-1 \
--no-shielded-secure-boot \
--shielded-vtpm \
--shielded-integrity-monitoring \
--labels=goog-dm=dlvm-marketplace-tf-2-3-1 \
--reservation-affinity=any