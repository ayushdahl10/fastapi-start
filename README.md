# Development Setup
* docker compose build
* docker compose up

# Enter inside application container
* docker exec -it app bash
* Cope the sample .evn_sample and create a new file .env

# Run  application
* docker logs -f app

# Navigate inside app folder (cd/app)
* python cmd
  - load base_config
  - load_roles
  - load_permissions
  - update_permissions
  - create_superuser (create superuser required)
  - create_user (optional if required to create admin user)
