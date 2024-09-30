# Development Setup
* docker compose build
* docker compose up

# Enter inside application container
* docker exec -it app bash
  
# Run and watch application logs
* docker logs -f app

# Navigate inside app folder
* python cmd
  - load_roles
  - load_permissions
  - update_permissions
  - create_superuser
  - create_user (optional if required to create admin user)
  
